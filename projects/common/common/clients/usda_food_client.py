import logging
import requests

logger = logging.getLogger(__name__)

DEFAULT_URL = "https://api.nal.usda.gov/fdc/v1/foods/search"
DEFAULT_TIMEOUT = 5


class USDACalorieClient:
    def __init__(self, api_key: str) -> None:
        self._api_key = api_key

    def get_calories(self, product: str, grams: float) -> float:
        """
        Returns total calories for given product and weight in grams
        """
        logger.info(
            "Request calories for product: %s (%sg)",
            product,
            grams,
        )

        kcal_per_100g = self._get_calories_100g(product)
        total_calories = kcal_per_100g * grams / 100

        logger.info(
            "Calories for %s (%sg): %.2f kcal",
            product,
            grams,
            total_calories,
        )

        return round(total_calories, 2)

    def _get_calories_100g(self, product: str) -> float:
        response = requests.post(
            DEFAULT_URL,
            params={"api_key": self._api_key},
            json={
                "query": product,
                "pageSize": 1,
                "dataType": ["Foundation", "SR Legacy"],
            },
            timeout=DEFAULT_TIMEOUT,
        )

        response.raise_for_status()
        foods = response.json().get("foods")

        if not foods:
            raise RuntimeError(f"Product not found: {product}")

        nutrients = foods[0].get("foodNutrients", [])
        for nutrient in nutrients:
            if (
                nutrient.get("nutrientName") == "Energy"
                and nutrient.get("unitName") == "KCAL"
            ):
                kcal = float(nutrient["value"])
                logger.info(
                    "Received calories for %s: %.2f kcal/100g",
                    product,
                    kcal,
                )
                return kcal

        raise RuntimeError(f"Energy information missing for product: {product}")

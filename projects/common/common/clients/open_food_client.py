import logging
import typing

import openfoodfacts

logger = logging.getLogger(__name__)

DEFAULT_USER_AGENT = "python-hse-calorie-bot/1.0"
CALORIE_MULTIPLIER = 0.23900573614


class OpenFoodFactsClient:
    def __init__(self, user_agent: str | None = None) -> None:
        self._api = openfoodfacts.API(user_agent=user_agent or DEFAULT_USER_AGENT)

    def get_calories_100g(self, product: str) -> float:
        logger.info("Request calories for product: %s", product)

        search_result = self._api.product.text_search(product)

        products = search_result.get("products")
        if not products:
            raise RuntimeError(f"Product not found: {product}")

        product_data = products[0]
        code = product_data.get("code")
        if not code:
            raise RuntimeError(f"Product code missing: {product}")

        data = self._api.product.get(code)

        nutriments = data.get("nutriments") if data else None
        if not nutriments:
            raise RuntimeError(f"Nutritional data missing for product: {product}")

        if "energy-kcal_100g" in nutriments:
            calories = nutriments["energy-kcal_100g"]
        elif "energy_100g" in nutriments:
            calories = nutriments["energy_100g"] * CALORIE_MULTIPLIER
        else:
            raise RuntimeError(f"Energy information missing for product: {product}")

        calories = float(calories)
        logger.info("Calories for %s: %.2f kcal/100g", product, calories)

        return typing.cast(float, calories)

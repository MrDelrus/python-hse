from decimal import Decimal, InvalidOperation

from common.clients import AsyncOpenWeatherClient, USDACalorieClient

# Constants for validation
MIN_WEIGHT = 35
MAX_WEIGHT = 200
MIN_HEIGHT = 140
MAX_HEIGHT = 220
MIN_AGE = 14
MAX_AGE = 60
MIN_DAILY_EXERCISE_TIME = 0
MAX_DAILY_EXERCISE_TIME = 8 * 60
MIN_CITY_LENGTH = 2
MAX_CITY_LENGTH = 20
MIN_CALORIES_GOAL = 1000
MAX_CALORIES_GOAL = 5000


def validate_weight(text: str) -> Decimal:
    try:
        number = Decimal(text)
    except InvalidOperation:
        raise ValueError()

    if not MIN_WEIGHT <= number <= MAX_WEIGHT:
        raise ValueError()

    return number


def validate_height(text: str) -> Decimal:
    try:
        number = Decimal(text)
    except InvalidOperation:
        raise ValueError()

    if not MIN_HEIGHT <= number <= MAX_HEIGHT:
        raise ValueError()

    return number


def validate_age(text: str) -> Decimal:
    try:
        number = Decimal(text)
    except InvalidOperation:
        raise ValueError()

    if not MIN_AGE <= number <= MAX_AGE:
        raise ValueError()

    return number


def validate_daily_exercise_time(text: str) -> Decimal:
    try:
        number = Decimal(text)
    except InvalidOperation:
        raise ValueError()

    if not MIN_DAILY_EXERCISE_TIME <= number <= MAX_DAILY_EXERCISE_TIME:
        raise ValueError()

    return number


def validate_city(text: str) -> str:
    if not MIN_CITY_LENGTH <= len(text) <= MAX_CITY_LENGTH:
        raise ValueError()

    return text


def create_async_weather_client(api_key: str) -> AsyncOpenWeatherClient:
    client = AsyncOpenWeatherClient(api_key)
    return client


def create_async_food_client(api_key: str) -> AsyncOpenWeatherClient:
    client = USDACalorieClient(api_key)
    return client


def validate_calories_goal(text: str) -> Decimal:
    try:
        number = Decimal(text)
    except InvalidOperation:
        raise ValueError()

    if not MIN_CALORIES_GOAL <= number <= MAX_CALORIES_GOAL:
        raise ValueError()

    return number

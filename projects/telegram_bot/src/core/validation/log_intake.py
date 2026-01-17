from decimal import Decimal, InvalidOperation

MIN_WATER_CONSUMED = 0
MAX_WATER_CONSUMED = 4000
MIN_PRODUCT_LENGTH = 2
MAX_PRODUCT_LENGTH = 20
MIN_EATEN_G = 1
MAX_EATEN_G = 1000
MIN_ACTIVITY_TIME_M = 1
MAX_ACTIVITY_TIME_M = 720

def validate_water(text: str) -> Decimal:
    try:
        number = Decimal(text)
    except InvalidOperation:
        raise ValueError()
    
    if not MIN_WATER_CONSUMED <= number <= MAX_WATER_CONSUMED:
        raise ValueError()

    return number

def validate_product_name(text: str) -> str:
    if not MIN_PRODUCT_LENGTH <= len(text) <= MAX_PRODUCT_LENGTH:
        raise ValueError()
    
    return text

def validate_product_g(text: str) -> Decimal:
    try:
        number = Decimal(text)
    except InvalidOperation:
        raise ValueError()

    if not MIN_EATEN_G <= number <= MAX_EATEN_G:
        raise ValueError()
    
    return number

def validate_activity(text: str) -> Decimal:
    args = text.split()
    if len(args) != 2:
        raise ValueError()
    
    try:
        number = Decimal(args[1])
    except InvalidOperation:
        raise ValueError()

    if not MIN_ACTIVITY_TIME_M <= number <= MAX_ACTIVITY_TIME_M:
        raise ValueError()

    return number

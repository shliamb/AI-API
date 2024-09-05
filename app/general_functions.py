from datetime import datetime, timezone, timedelta
import logging

# from config import price


# GET DAY AND TIME
async def day_utcnow(time_correction: str):
    utc_zone = timezone.utc
    a = datetime.now(timezone.utc).replace(tzinfo=utc_zone)
    a = a + timedelta(hours=time_correction)
    day_str = a.strftime("%Y-%m-%d %H:%M:%S")
    day = datetime.strptime(day_str, '%Y-%m-%d %H:%M:%S')
    # print("info: Getting the day and time from the server")
    return day or None

# UNFORMAT TIME
async def unformat_date(date):
    day_now = str(date.strftime("%Y-%m-%d"))
    time_now = float(date.strftime("%H.%M"))
    return day_now, time_now

# Calculation of the cost of used tokens
async def calculation(price, model_version, used_tokens, prompt_tokens):
    one_tok_price = None
    for key, value in price.items():
        if key == model_version:
            one_tok_price = value / 1000000 # Price 1 token to USD
    if one_tok_price == None:
        logging.error(f"The model {model_version} was not found in the price list")
        raise
    all_tokens = used_tokens +  prompt_tokens
    total_price = one_tok_price * all_tokens
    return one_tok_price, all_tokens, total_price

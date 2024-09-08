from datetime import datetime, timezone, timedelta
import logging
from config import price, time_correction
from worker_db import add_statistic, get_user_by_username, update_user_by_username

# from config import price


# GET DAY AND TIME
async def day_utcnow():
    utc_zone = timezone.utc
    a = datetime.now(timezone.utc).replace(tzinfo=utc_zone)
    a = a + timedelta(hours=time_correction)
    day_str = a.strftime("%Y-%m-%d %H:%M:%S")
    day = datetime.strptime(day_str, '%Y-%m-%d %H:%M:%S')
    logging.info("info: Getting the day and time from the server")
    return day or None

# UNFORMAT TIME
async def unformat_date(date):
    day_now = str(date.strftime("%Y-%m-%d"))
    time_now = float(date.strftime("%H.%M"))
    return day_now, time_now


# Calculation of the cost of used tokens
async def calculation(username, model_version, used_tokens):
    one_tok_price = None
    
    for key, value in price.items():
        if key == model_version:
            one_tok_price = value / 1000000 # Price 1 token to USD
            break
        
    if one_tok_price == None:
        print(f"The model {model_version} was not found in the price list")
        logging.error(f"The model {model_version} was not found in the price list")
        one_tok_price = 0.000095 # Sorry..

    total_price = one_tok_price * used_tokens

    # Collecting data
    data_stat = {
        "username_table_stat": username,
        "time": await day_utcnow(),
        "use_model": model_version,
        "sesion_token": used_tokens,
        "price_1_tok": one_tok_price,
        "total_price": total_price,
    }

    # Save statistic data to DB:
    await add_statistic(data_stat)

    # Getting user data
    user_data = await get_user_by_username(username)
    new_money = user_data.money - total_price
    data_money = {"money": new_money}

    # The balance was changed taking into account the expense
    await update_user_by_username(username, data_money)

    return total_price

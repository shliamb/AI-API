from config import LOG_CONFIG_DB, PRICE
import logging
logging.basicConfig(**LOG_CONFIG_DB)
import uuid
from datetime import datetime
from worker_db import read_account_access_id, add_record_stat, read_user, update_user 







# Calculation of the cost of used tokens
async def calculate_token_cost(access_id: uuid, model_version: str, used_tokens: int, input_data: str) -> float:
    """  
    Calculates the cost of OpenAI tokens for the given text and saves it to the database.  
    Returns the cost in USD.  
    """ 
    one_tok_price = None
    
    for key, value in PRICE.items():
        if key == model_version:
            if input_data == "text":
                one_tok_price = value / 1000000 # Price 1 token to USD
                break
            elif input_data == "img":
                one_tok_price = value
                break
            elif input_data == "audio":
                one_tok_price = value # Price 1 min
                break
        
    if one_tok_price == None:
        print(f"The model {model_version} was not found in the price list")
        logging.error(f"The model {model_version} was not found in the price list")
        one_tok_price = 0.000095 # Sorry..


    data_account = await read_account_access_id(access_id)
    user_id = data_account.get("user_id_telegram")
    total_cost = one_tok_price * used_tokens

    data_stat = {
        "user_id": user_id,
        "time": datetime.now(),
        "use_model": model_version,
        "sesion_token": used_tokens,
        "price_1_tok": one_tok_price,
        "total_price": total_cost,
        "access_id": access_id
    }

    if not await add_record_stat(data_stat):
        print("Error: Failed to add statistics using the AI model")
        logging.error("Error: Failed to add statistics using the AI model")

    user_data = await read_user(user_id)
    new_money = user_data.get("money") - total_cost
    data_money = {"user_id": user_id, "money": new_money, "last_visit": datetime.now()}

    if not await update_user(data_money):
        print("Error: Failed to update money using the AI model")
        logging.error("Error: Failed to update money using the AI model")

    return total_cost
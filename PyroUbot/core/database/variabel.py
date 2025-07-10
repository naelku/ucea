from typing import List, Optional, Union
from PyroUbot.core.database import mongodb
from PyroUbot import bot  # Import bot dari PyroUbot
from datetime import datetime

varsdb = mongodb.varsX

async def set_vars(user_id: int, vars_name: str, value: Union[int, str], query: str = "vars"):
    update_data = {"$set": {f"{query}.{vars_name}": value}}
    await varsdb.update_one({"_id": user_id}, update_data, upsert=True)

async def get_vars(user_id: int, vars_name: str, query: str = "vars") -> Optional[Union[int, str]]:
    result = await varsdb.find_one({"_id": user_id})
    return result.get(query, {}).get(vars_name, None) if result else None

async def remove_vars(user_id: int, vars_name: str, query: str = "vars"):
    remove_data = {"$unset": {f"{query}.{vars_name}": ""}}
    await varsdb.update_one({"_id": user_id}, remove_data)

async def all_vars(user_id: int, query: str = "vars") -> Optional[dict]:
    result = await varsdb.find_one({"_id": user_id})
    return result.get(query) if result else None

async def remove_all_vars(user_id: int):
    await varsdb.delete_one({"_id": user_id})

async def get_list_from_vars(user_id: int, vars_name: str, query: str = "vars") -> List[int]:
    vars_data = await get_vars(user_id, vars_name, query)
    return [int(x) for x in str(vars_data).split()] if vars_data else []

async def add_to_vars(user_id: int, vars_name: str, value: int, query: str = "vars"):
    vars_list = await get_list_from_vars(user_id, vars_name, query)
    vars_list.append(value)
    await set_vars(user_id, vars_name, " ".join(map(str, vars_list)), query)

async def remove_from_vars(user_id: int, vars_name: str, value: int, query: str = "vars"):
    vars_list = await get_list_from_vars(user_id, vars_name, query)
    if value in vars_list:
        vars_list.remove(value)
        await set_vars(user_id, vars_name, " ".join(map(str, vars_list)), query)

async def get_pm_id(user_id: int) -> List[int]:
    pm_id = await get_vars(user_id, "PM_PERMIT")
    return [int(x) for x in str(pm_id).split()] if pm_id else []

async def add_pm_id(me_id: int, user_id: int):
    pm_id = await get_vars(me_id, "PM_PERMIT")
    if pm_id:
        user_id = f"{pm_id} {user_id}"
    await set_vars(me_id, "PM_PERMIT", user_id)

async def remove_pm_id(me_id: int, user_id: int):
    pm_id = await get_vars(me_id, "PM_PERMIT")
    if pm_id:
        list_id = [int(x) for x in str(pm_id).split() if x != str(user_id)]
        await set_vars(me_id, "PM_PERMIT", " ".join(map(str, list_id)))
 
 
async def set_status(user_id, status):
    await set_vars(user_id, "WORD_DETECTION_STATUS", status)

async def get_status(user_id):
    status = await get_vars(user_id, "WORD_DETECTION_STATUS")
    return status if status is not None else False

# Fungsi untuk menambahkan user ke daftar free trial di database
async def add_to_free_trial_list(user_id):
    """Add user to free trial list in database"""
    # Pastikan ada spasi di string "FREE_TRIAL_USERS" (bukan "FREE_TRIAL USERS")
    await add_to_vars(bot.me.id, "FREE_TRIAL_USERS", user_id)

# Seller expiration functions
async def set_seles_expiry(user_id: int, expiry_date):
    """Set expiration date for seller"""
    if isinstance(expiry_date, datetime):
        # Convert datetime to string format
        expiry_str = expiry_date.strftime("%Y-%m-%d %H:%M:%S")
    else:
        # Assume it's already a string
        expiry_str = expiry_date
        
    await set_vars(bot.me.id, f"SELES_EXP_{user_id}", expiry_str)

async def get_seles_expiry(user_id: int):
    """Get expiration date for seller"""
    expiry_str = await get_vars(bot.me.id, f"SELES_EXP_{user_id}")
    if expiry_str:
        try:
            # Return as datetime object
            return datetime.strptime(expiry_str, "%Y-%m-%d %H:%M:%S")
        except Exception:
            # Return raw string if parsing fails
            return expiry_str
    return None

async def remove_seles_expiry(user_id: int):
    """Remove expiration data for seller"""
    await remove_vars(bot.me.id, f"SELES_EXP_{user_id}")
    # Also remove permanent flag if exists
    await remove_vars(bot.me.id, f"SELES_PERM_{user_id}")

async def set_permanent_seles(user_id: int):
    """Mark seller as permanent"""
    await set_vars(bot.me.id, f"SELES_PERM_{user_id}", "1")
    # Remove any expiration date if exists
    await remove_vars(bot.me.id, f"SELES_EXP_{user_id}")

async def is_permanent_seles(user_id: int):
    """Check if seller is permanent"""
    perm_flag = await get_vars(bot.me.id, f"SELES_PERM_{user_id}")
    return perm_flag == "1"

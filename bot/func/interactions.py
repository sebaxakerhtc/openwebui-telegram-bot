# >> interactions
import logging
import os
import aiohttp
import json
import sqlite3
from aiogram import types
from aiohttp import ClientTimeout
from asyncio import Lock
from functools import wraps
# from bot.run import load_allowed_ids_from_db
from dotenv import load_dotenv
load_dotenv()
token = os.getenv("TOKEN")
webui_token = os.getenv("WEBUI_TOKEN")
allowed_ids = list(map(int, os.getenv("USER_IDS", "").split(",")))
admin_ids = list(map(int, os.getenv("ADMIN_IDS", "").split(",")))
webui_base_url = os.getenv("WEBUI_BASE_URL")
webui_port = os.getenv("WEBUI_PORT", "3000")
log_level_str = os.getenv("LOG_LEVEL", "DEBUG")
allow_all_users_in_groups = bool(int(os.getenv("ALLOW_ALL_USERS_IN_GROUPS", "0")))
log_levels = list(logging._levelToName.values())
timeout = os.getenv("TIMEOUT", "3000")
if log_level_str not in log_levels:
    log_level = logging.DEBUG
else:
    log_level = logging.getLevelName(log_level_str)
logging.basicConfig(level=log_level)
async def model_list():
    headers = {
        'Authorization': f'Bearer {webui_token}',
        'Accept': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        url = f"http://{webui_base_url}:{webui_port}/api/models"
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data["data"]
            else:
                return []
async def sdmodel_list():
    headers = {
        'Authorization': f'Bearer {webui_token}',
        'Accept': 'application/json'
    }
    async with aiohttp.ClientSession() as session:
        url = f"http://{webui_base_url}:{webui_port}/images/api/v1/models"
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return []
async def generate(payload: dict, modelname: str, prompt: str):
    client_timeout = ClientTimeout(total=int(timeout))
    headers = {
        'Authorization': f'Bearer {webui_token}',
        'Accept': 'application/json'
    }
    async with aiohttp.ClientSession(timeout=client_timeout) as session:
        url = f"http://{webui_base_url}:{webui_port}/api/chat/completions"
        try:
            async with session.post(url, json=payload, headers=headers) as response:
                if response.status != 200:
                    raise aiohttp.ClientResponseError(
                        status=response.status, message=response.reason
                    )
                buffer = b""
                async for chunk in response.content.iter_any():
                    buffer += chunk
                    while b"\n" in buffer:
                        line, buffer = buffer.split(b"\n", 1)
                        line = line.strip()
                        if line: # Decode line as UTF-8 before processing
                            if line.startswith(b"data: "):
                                line = line[len(b"data: "):]
                        
                            if line == b"[DONE]":
                                return

                            try:
                                decoded_line = line.decode("utf-8")
                                json_data = json.loads(decoded_line)
                                yield json_data
                            except UnicodeDecodeError:
                                logging.error(f"Failed to decode line: {line}")
                            except json.JSONDecodeError:
                                logging.error(f"Failed to parse JSON: {decoded_line}")
        except aiohttp.ClientError as e:
            print(f"Error during request: {e}")

def load_allowed_ids_from_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id FROM users")
    user_ids = [row[0] for row in c.fetchall()]
    print(f"users_ids: {user_ids}")
    conn.close()
    return user_ids


def get_all_users_from_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT id, name FROM users")
    users = c.fetchall()
    conn.close()
    return users

def remove_user_from_db(user_id):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    removed = c.rowcount > 0
    conn.commit()
    conn.close()
    if removed:
        allowed_ids = [id for id in allowed_ids if id != user_id]
    return removed

def perms_allowed(func):
    @wraps(func)
    async def wrapper(message: types.Message = None, query: types.CallbackQuery = None):
        user_id = message.from_user.id if message else query.from_user.id
        if user_id in admin_ids or user_id in allowed_ids:
            if message:
                return await func(message)
            elif query:
                return await func(query=query)
        else:
            if message:
                if message and message.chat.type in ["supergroup", "group"]:
                    if allow_all_users_in_groups:
                        return await func(message)
                    return
                await message.answer("Access Denied")
            elif query:
                if message and message.chat.type in ["supergroup", "group"]:
                    return
                await query.answer("Access Denied")

    return wrapper


def perms_admins(func):
    @wraps(func)
    async def wrapper(message: types.Message = None, query: types.CallbackQuery = None):
        user_id = message.from_user.id if message else query.from_user.id
        if user_id in admin_ids:
            if message:
                return await func(message)
            elif query:
                return await func(query=query)
        else:
            if message:
                if message and message.chat.type in ["supergroup", "group"]:
                    return
                await message.answer("Access Denied")
                logging.info(
                    f"[MSG] {message.from_user.first_name} {message.from_user.last_name}({message.from_user.id}) is not allowed to use this bot."
                )
            elif query:
                if message and message.chat.type in ["supergroup", "group"]:
                    return
                await query.answer("Access Denied")
                logging.info(
                    f"[QUERY] {message.from_user.first_name} {message.from_user.last_name}({message.from_user.id}) is not allowed to use this bot."
                )

    return wrapper
class contextLock:
    lock = Lock()

    async def __aenter__(self):
        await self.lock.acquire()

    async def __aexit__(self, exc_type, exc_value, exc_traceback):
        self.lock.release()

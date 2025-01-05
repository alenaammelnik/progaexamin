import asyncio
import datetime
import json
from termcolor import colored
from pynput import keyboard
import aiohttp
import asyncpg

# Флаг для завершения программы
exit_flag = False

WEB_SERVER_URL = "https://rnacentral.org/api/v1/rna/URS000075C825"
DB_CONNECTION_STRING = "postgres://reader:NWDMCE5xdipIjRrp@hh-pgsql-public.ebi.ac.uk:5432/pfmegrnargs"

# Асинхронная функция для отображения времени
async def display_time():
    global exit_flag
    while not exit_flag:
        now = datetime.datetime.now()
        time_str = colored(now.strftime('%H:%M:%S'), 'green')
        date_str = colored(now.strftime('%Y-%m-%d'), 'yellow')
        print(f"\r{date_str} {time_str}", end="")
        await asyncio.sleep(1)

# Функция обработки нажатия клавиш
def on_press(key):
    global exit_flag
    try:
        if key == keyboard.Key.esc:  # Нажатие клавиши Esc
            exit_flag = True
    except Exception as e:
        print(f"Error: {e}")

# Асинхронная функция для HTTP запроса
async def fetch_web_data():
    async with aiohttp.ClientSession() as session:
        async with session.get(WEB_SERVER_URL) as response:
            data = await response.json()
            print("\nWeb Data:")
            print(json.dumps(data, indent=4))
            return data

# Асинхронная функция для запроса к базе данных
async def fetch_db_data():
    conn = await asyncpg.connect(DB_CONNECTION_STRING)
    rows = await conn.fetch("SELECT * FROM rna LIMIT 5;")
    await conn.close()
    print("\nDB Data:")
    for row in rows:
        print(dict(row))
    return rows

# Основная логика программы
async def main():
    global exit_flag
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    # Параллельное выполнение задач
    tasks = asyncio.gather(display_time(), fetch_web_data(), fetch_db_data())
    await tasks

    listener.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated.")
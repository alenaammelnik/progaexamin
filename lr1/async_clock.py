import asyncio
import datetime
from termcolor import colored
from pynput import keyboard

# Флаг для завершения программы
exit_flag = False

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

# Основная логика программы
async def main():
    global exit_flag
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    await display_time()

    listener.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated.")
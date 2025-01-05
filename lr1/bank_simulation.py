import threading
import time

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance
        self.lock = threading.Lock()

    def deposit(self, amount):
        with self.lock:
            print(f"Depositing {amount}... Current Balance: {self.balance}")
            time.sleep(0.1)  # Симуляция задержки операции
            self.balance += amount
            print(f"Deposited {amount}. New Balance: {self.balance}")

    def withdraw(self, amount):
        with self.lock:
            if self.balance >= amount:
                print(f"Withdrawing {amount}... Current Balance: {self.balance}")
                time.sleep(0.1)  # Симуляция задержки операции
                self.balance -= amount
                print(f"Withdrew {amount}. New Balance: {self.balance}")
            else:
                print(f"Failed to withdraw {amount}. Insufficient funds. Current Balance: {self.balance}")

# Пример использования
account = BankAccount(100)

# Функции для потоков
def perform_deposits():
    for _ in range(5):
        account.deposit(50)

def perform_withdrawals():
    for _ in range(5):
        account.withdraw(30)

# Создание потоков
deposit_thread = threading.Thread(target=perform_deposits)
withdraw_thread = threading.Thread(target=perform_withdrawals)

# Запуск потоков
deposit_thread.start()
withdraw_thread.start()

# Ожидание завершения потоков
deposit_thread.join()
withdraw_thread.join()

print(f"Final Balance: {account.balance}")

import auth
from services import finance_service

def main():
    current_user = None
    
    while True:
        if not current_user:
            print("\n===== СИСТЕМА УЧЕТА ФИНАНСОВ =====")
            print("1. Войти в систему")
            print("0. Выход")
            choice = input("Выберите действие: ")
            
            if choice == "1":
                login = input("Логин: ")
                password = input("Пароль: ")
                user = auth.authenticate(login, password)
                if user:
                    current_user = user
                    print(f"\n Успешный вход! Добро пожаловать, {user.login} (Роль: {user.role_name})")
                else:
                    print("\n Неверный логин или пароль!")
            elif choice == "0":
                print("До свидания!")
                break
        else:
            print(f"\n===== Меню ({current_user.role_name}: {current_user.login}) =====")
            
            if current_user.role_name == 'Руководитель':
                print("1. Посмотреть операции")
                print("2. Посмотреть баланс")
                print("3. Изменить данные пользователя")
                print("4. Удалить пользователя")
                print("5. Зарегистрировать нового пользователя")
                print("0. Выйти из аккаунта")
                
                choice = input("Выберите действие: ")
                
                if choice == "1":
                    operations = finance_service.get_history()
                    print("\n--- ИСТОРИЯ ОПЕРАЦИЙ ---")
                    if not operations:
                        print("Операций пока нет.")
                    for op in operations:
                        print(f"[{op.operation_id}] Тип: {op.operation_type} | Сумма: {op.amount} | Описание: {op.description} | Автор: {op.user_login}")
                        
                elif choice == "2":
                    balance = finance_service.get_total_balance()
                    print(f"\n Текущий баланс организации: {balance}")
                    
                elif choice == "3":
                    users = finance_service.get_users_list()
                    print("\nСписок пользователей:")
                    for u in users:
                        print(f"ID: {u[0]} | Логин: {u[1]} | Роль ID: {u[2]}")
                    try:
                        uid = int(input("Введите ID пользователя для изменения пароля: "))
                        new_pass = input("Введите новый пароль: ")
                        finance_service.update_user_credentials(uid, new_pass)
                        print("\n Данные пользователя успешно изменены!")
                    except ValueError:
                        print("\n Ошибка: ID должен быть числом!")
                    except Exception as e:
                        print(f"\n Ошибка: {e}")
                        
                elif choice == "4":
                    users = finance_service.get_users_list()
                    print("\nСписок пользователей:")
                    for u in users:
                        print(f"ID: {u[0]} | Логин: {u[1]}")
                    try:
                        uid = int(input("Введите ID пользователя для удаления: "))
                        if uid == current_user.user_id:
                            print("\n Нельзя удалить собственный аккаунт руководителя!")
                        else:
                            finance_service.remove_user(uid)
                            print("\n Пользователь успешно удален!")
                    except ValueError:
                        print("\n Ошибка: ID должен быть числом!")
                    except Exception as e:
                        print(f"\n Ошибка: {e}")
                        
                elif choice == "5":
                    new_login = input("Логин нового сотрудника: ")
                    new_pass = input("Пароль: ")
                    print("Выберите роль: 1 - Руководитель, 2 - Бухгалтер")
                    try:
                        role_id = int(input("ID роли: "))
                        finance_service.register_new_user(new_login, new_pass, role_id)
                        print("\n Сотрудник успешно зарегистрирован!")
                    except ValueError:
                        print("\n Ошибка: ID роли должен быть числом!")
                    except Exception as e:
                        print(f"\n Ошибка регистрации: {e}")
                        
                elif choice == "0":
                    current_user = None
                    print("\n Вы вышли из аккаунта.")
                else:
                    print("\n Неверный выбор!")

            elif current_user.role_name == 'Бухгалтер':
                print("1. Добавить операцию")
                print("2. Изменить свои данные (пароль)")
                print("3. Посмотреть операции")
                print("4. Посмотреть баланс")
                print("0. Выйти из аккаунта")
                
                choice = input("Выберите действие: ")
                
                if choice == "1":
                    print("\nВыберите тип операции:")
                    print("1. Доход")
                    print("2. Расход")
                    op_choice = input("Ваш выбор (1/2): ")
                    
                    if op_choice == "1":
                        op_type = "Доход"
                    elif op_choice == "2":
                        op_type = "Расход"
                    else:
                        print("\n Ошибка: нужно выбрать 1 или 2!")
                        continue
                        
                    try:
                        amount = float(input("Сумма: "))
                        desc = input("Описание: ")
                        finance_service.add_operation(op_type, amount, desc, current_user.user_id)
                        print("\n Операция успешно добавлена!")
                    except ValueError:
                        print("\n Ошибка: сумма должна быть числом!")
                    except Exception as e:
                        print(f"\n Ошибка: {e}")
                        
                elif choice == "2":
                    new_pass = input("Введите ваш новый пароль: ")
                    try:
                        finance_service.update_user_credentials(current_user.user_id, new_pass)
                        print("\n Ваши данные успешно обновлены!")
                    except Exception as e:
                        print(f"\n Ошибка: {e}")
                        
                elif choice == "3":
                    operations = finance_service.get_history()
                    print("\n--- ИСТОРИЯ ОПЕРАЦИЙ ---")
                    if not operations:
                        print("Операций пока нет.")
                    for op in operations:
                        print(f"[{op.operation_id}] Тип: {op.operation_type} | Сумма: {op.amount} | Описание: {op.description} | Автор: {op.user_login}")
                        
                elif choice == "4":
                    balance = finance_service.get_total_balance()
                    print(f"\n Текущий баланс организации: {balance}")
                    
                elif choice == "0":
                    current_user = None
                    print("\n Вы вышли из аккаунта.")
                else:
                    print("\n Неверный выбор!")

if __name__ == "__main__":
    main()
from repositories import operation_repo, user_repo

def add_operation(operation_type: str, amount: float, description: str, user_id: int):
    if amount <= 0:
        raise Exception("Сумма операции должна быть больше нуля!")
    if not operation_type.strip():
        raise Exception("Тип операции не может быть пустым!")
    operation_repo.create_operation(operation_type, amount, description, user_id)

def get_history():
    return operation_repo.get_all_operations()

def get_total_balance():
    return operation_repo.get_balance()

def register_new_user(login: str, password: str, role_id: int):
    if not login.strip() or not password.strip():
        raise Exception("Логин и пароль не могут быть пустыми!")
    if user_repo.get_by_login(login):
        raise Exception("Пользователь с таким логином уже существует!")
    user_repo.create_user(login, password, role_id)

def update_user_credentials(user_id: int, new_password: str):
    if not new_password.strip():
        raise Exception("Пароль не может быть пустым!")
    user_repo.update_user_password(user_id, new_password)

def remove_user(user_id: int):
    user_repo.delete_user(user_id)

def get_users_list():
    return user_repo.get_all_users()
from repositories import user_repo

def authenticate(login: str, password: str):
    user = user_repo.get_by_login(login)
    if not user or user.password != password:
        return None
    return user
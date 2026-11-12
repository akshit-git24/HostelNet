from .database import get_user

def find_user(username: str):
    print(f"Searching for user: {username}")
    return get_user(username)


if __name__ == "__main__":
    username = input("Enter username: ")
    result = find_user(username)
    print(result)

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(user_password: str) -> str:
    return pwd_context.hash(user_password)

def verify_password(hash: str, user_password: str) -> bool:
    return pwd_context.verify(user_password, hash)


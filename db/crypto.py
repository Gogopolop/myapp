import os
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

_KEY = os.getenv("DB_ENCRYPTION_KEY")
if not _KEY:
    raise RuntimeError(
        "DB_ENCRYPTION_KEY не задан в .env. Сгенерируй его командой:\n"
        "python -c \"from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())\""
    )
_fernet = Fernet(_KEY.encode())


def encrypt(value: str) -> str:
    return _fernet.encrypt(value.encode()).decode()


def decrypt(value: str) -> str:
    return _fernet.decrypt(value.encode()).decode()
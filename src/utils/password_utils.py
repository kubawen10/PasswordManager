import string
import random
from models.utils import create_db
from encrpytion.encryption import decrypt
from models.secret import get_first_secret

def is_proper_master_password(master_password: str) -> bool:
        if len(master_password) < 8:
            return False
        
        lowercase_letters = string.ascii_lowercase
        uppercase_letters = string.ascii_uppercase
        digits = string.digits
        special_chars = string.punctuation

        has_lower = False
        has_upper = False
        has_digit = False
        has_special = False

        for char in master_password:
            if not has_lower and char in lowercase_letters:
                has_lower = True
            elif not has_upper and char in uppercase_letters:
                has_upper = True
            elif not has_digit and char in digits:
                has_digit = True
            elif not has_special and char in special_chars:
                has_special = True

            if has_lower and has_upper and has_digit and has_special:
                return True
        
        return False

def validate_master_password(master_password: str) -> None:
    create_db()
    first_secret = get_first_secret()

    if first_secret is None:
        return True
    else:
        try:
            decrypt(first_secret.secret_bytes, master_password)
            return True
        except:
            return False
        
def generate_password(small_letters: bool, capital_letters: bool, digits: bool, special_chars: bool, length: int) -> str:
    alphabet = ""

    if small_letters:
        alphabet += string.ascii_lowercase

    if capital_letters:
        alphabet += string.ascii_uppercase
    
    if digits:
        alphabet += string.digits

    if special_chars:
        alphabet += string.punctuation

    return "".join(random.choices(alphabet, k=length))

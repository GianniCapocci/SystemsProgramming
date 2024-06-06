import random
import string


def generate_alphanumeric(length: int) -> str:
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choices(chars, k=length))

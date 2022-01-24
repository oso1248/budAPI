import re
from passlib.context import CryptContext
import pendulum as ptime
tz = ptime.timezone('America/Denver')

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def titlecase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda word: word.group(0).capitalize(), s)


def uppercase(s):
    return re.sub(r"[A-Za-z]+('[A-Za-z]+)?", lambda word: word.group(0).upper(), s)


def convert_phone_number(phone):
    return re.sub(r'(\d{3})(\d{3})(\d{4})', r'(\1) \2-\3', phone)


def strip_non_numeric(num):
    return re.sub('[^0-9]', '', num)

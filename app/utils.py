from fastapi import status, HTTPException
from passlib.context import CryptContext
from cachetools import TTLCache
from cryptography.fernet import Fernet
import hashlib
import string
import random
import time


pwd_context = CryptContext(schemes=["bcrypt"], deprecated = 'auto')

cache = TTLCache(maxsize=100, ttl=60)

def hash(password:str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

#OTP
def generate_otp(length=6):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def save_otp(email, otp):
    cache[email] = otp

def verify_otp(email: str, otp:str) -> bool:
    cached_otp = cache.get(email)

    if cached_otp is None:
        raise   HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="OTP expired")
    
    if cached_otp != otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid OTP")
    
    del cache[email]

    return True

key = Fernet.generate_key()
fernet = Fernet(key)

def encrypt(id):
    id = str(id)
    enc_id = fernet.encrypt(id.encode())
    return enc_id

def decrypt(enc_id):
    try:
        id = fernet.decrypt(enc_id).decode()
        return id
    except:
        return None
def uniqueId(id):
    id = str(id)
    return hashlib.sha256(id.encode()).hexdigest()

    

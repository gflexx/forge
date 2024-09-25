import random

from .models import User

def generate_otp():
    key = random.randint(100001, 999999)
    return key

def create_user_otp():
    otp = generate_otp()
    exists = User.objects.filter(otp_code=otp).exists()
    if exists:
        create_user_otp()
    else:
        return otp
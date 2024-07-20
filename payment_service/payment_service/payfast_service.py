import requests
import hashlib
import os
from dotenv import load_dotenv

load_dotenv()

PAYFAST_MERCHANT_ID = os.getenv("PAYFAST_MERCHANT_ID")
PAYFAST_MERCHANT_KEY = os.getenv("PAYFAST_MERCHANT_KEY")
PAYFAST_PASSPHRASE = os.getenv("PAYFAST_PASSPHRASE")
PAYFAST_URL = "https://sandbox.payfast.co.za/eng/process"  # Use sandbox for testing

def generate_signature(data):
    payload = "&".join(f"{key}={value}" for key, value in data.items() if value)
    return hashlib.md5(f"{payload}{PAYFAST_PASSPHRASE}".encode()).hexdigest()

def create_payfast_payment(amount, item_name, order_id):
    data = {
        "merchant_id": PAYFAST_MERCHANT_ID,
        "merchant_key": PAYFAST_MERCHANT_KEY,
        "amount": str(amount),
        "item_name": item_name,
        "custom_str1": str(order_id),
        "return_url": "http://yourwebsite.com/return",
        "cancel_url": "http://yourwebsite.com/cancel",
        "notify_url": "http://yourwebsite.com/notify",
    }
    
    data["signature"] = generate_signature(data)
    
    response = requests.post(PAYFAST_URL, data=data)
    return response.url
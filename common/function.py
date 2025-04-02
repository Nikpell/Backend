import hashlib
import jwt
from config import settings


def encode_handle(request):
    return jwt.decode(
            request.token, request.app.config.SECRET, algorithms=[settings.algorithm.get_secret_value()]
        )

def verify_transaction_signature(data):
    verify_data = (str(data.account_id) + str(data.amount) + str(data.transaction_id) + str(data.user_id)
                      + settings.signature.get_secret_value())
    verify_hash = hashlib.sha256(verify_data.encode()).hexdigest()
    return verify_hash == data.signature

def generate_transaction_sign(data):
    verify_data = (str(data.get("account_id")) + str(data.get("amount"))
                   + str(data.get("transaction_id")) + str(data.get("user_id"))
                   + settings.signature.get_secret_value())
    verify_hash = hashlib.sha256(verify_data.encode()).hexdigest()
    return verify_hash
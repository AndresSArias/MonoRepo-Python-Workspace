from jwt import encode, decode
from typing import Dict

def create_token(data: Dict) ->str:
    token: str = encode(payload= data, key = "secret_key",algorithm = "HS256")
    return token

def validate_token (token:str) -> Dict:
    data: Dict = decode(token, key = "secret_key",algorithms = ["HS256"])
    return data
from jose import JWTError, jwt
from datetime import datetime, timedelta

# Secret key
# algorithm 
# expiration time of the token

SECRET_KEY = "987f98asdfas0f8a90ds7gads6a9sfg"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



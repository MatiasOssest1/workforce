from jose import JWTError, jwt 
from datetime import datetime, timedelta
from .models import TokenData
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .config import settings

oaut2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRETKEY =settings.secret_key
ALGORITHM =settings.algorithm
ACCESS_TOKEN_EXPIRATION_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_enconde = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRATION_MINUTES)
    to_enconde.update({"exp": expire})

    encoded_jwt = jwt.encode(to_enconde, SECRETKEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRETKEY, algorithms=[ALGORITHM])

        user:str = payload.get('user')
        if user is None:
            raise credentials_exception
        token_data = TokenData(user=user, token=token)
    
    except JWTError:
        raise credentials_exception
    
    return token_data
     
def get_current_user(token: str =Depends(oaut2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail=f"Token Expirado",
                                          headers={"WWW-Authenticate": "Bearer"})
    
    return verify_access_token(token, credentials_exception)

 
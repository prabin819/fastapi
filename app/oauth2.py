from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

# algorithm, secret key, expiration time

SECRET_KEY = "secretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()
    
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})   # to_encode["exp"] = expire
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt
    
def verify_access_token(token: str, credentials_exception):
    
    try:
        # Decode the JWT using the same secret and algorithm
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Optional: Extract specific data from payload
        id: int = payload.get("user_id") # type: ignore
        
        if id is None:
            raise credentials_exception
        
        # Optional: You could also validate `exp` manually if needed
        # exp = payload.get("exp")
        # if datetime.utcnow() > datetime.fromtimestamp(exp):
        #     raise credentials_exception
        
        token_data = schemas.TokenData(id=id)
        
    except JWTError:
        raise credentials_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
    # we can pass this as a dependency into any one of our path operations. and when we do that, what its going to do is, its going to take the token from the request automatically, extract the id for us. its going to verify that the token is correct by calling the verify access token. And then its going to extract the id. and then if we want to, we can have it automatically fetch the user from the db and then add it into as a parameter into our path operation function.
    
    

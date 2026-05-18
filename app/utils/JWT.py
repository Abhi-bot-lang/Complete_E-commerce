import os
from datetime import datetime,timedelta
from jose import jwt,JWTError 
from datetime import datetime,timedelta
from fastapi import HTTPException,status
from dotenv import load_dotenv

load_dotenv()


ACCESS_TOKEN_SECRET_KEY=os.getenv("ACCESS_SECRET_KEY")
REFRESH_SECRET_KEY=os.getenv("REFRESH_SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM","HS256")
ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES",30))
REFRESH_TOKEN_EXPIRE_DAYS=int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS",7))


def create_access_token(data:dict):
    to_encode=data.copy()
     ### There is a mistake in the 21 line     
    expire=datetime.utcnow()+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,ACCESS_TOKEN_SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt 

def create_refresh_token(data:dict):
    to_encode=data.copy()
    expire=datetime.utcnow()+timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,REFRESH_SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt 

def verify_token(token:str,is_refresh:bool=False):
    secret=REFRESH_SECRET_KEY if is_refresh else ACCESS_TOKEN_SECRET_KEY 
    try:
        #Just check payload once more       
        payload=jwt.decode(token,secret,algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate":"Bearer"}
            #Bearer->It is a type of authentication token 
        )



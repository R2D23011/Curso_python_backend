from jose import jwt, JWTError
from jwt.exceptions import InvalidTokenError
from passlib.context import CryptContext
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta

ALGORITHM = "HS256"
access_token_duration = 1
SECRET = "fe7dd9f49a194ada0e6fbfd967e628910472d57ba63e104658695fe5e7adc71d"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl='login')

crypt = CryptContext(schemes=["bcrypt"])

class User(BaseModel):
    username: str
    name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db ={
    'mouredev': {
        "username": "mouredev",
        "name": "Brais Moure",
        "email": "mouredev@gmail.com",
        "disabled": False,
        "password": "$2a$12$NDuMvN8jUrDB2mkJGjGk7O0O3ums4m.AmNMn.7DCNJe4Sj.lltW.a"
    },
    'mouredev2': {
        "username": "mouredev2",
        "name": "Brais Moure2",
        "email": "mouredev2@gmail.com",
        "disabled": True,
        "password": "$2a$12$Cl3aXCBHA3ujIwdb0Bg/TOwY7G8l3uUq0qvw4y9nU3MfqBEQmWfZG"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])
    

    
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])
    

    
async def auth_user(token: str = Depends(oauth2)):

    exceptions = HTTPException(
        status_code= status.HTTP_401_UNAUTHORIZED, 
        detail= "Credenciales de autenticacion invalidas", 
        headers={"WWW-Authenticate": "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exceptions
        

    except JWTError:
        raise exceptions
    
    return search_user(username)
        
    
async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(status_code= status.HTTP_400_BAD_REQUEST, 
                            detail= "Usuario inactivo")
    return user

@router.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db =users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=400, detail= "El usuario no es correcto")
    
    user = search_user_db(form.username)


    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=400, detail="La contrasena no es correcta")

    access_token = {"sub": user.username,
                    "exp": datetime.utcnow() + timedelta(minutes=access_token_duration)}
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM) , "token_type": "bearer"}


@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user


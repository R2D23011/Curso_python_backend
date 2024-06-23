from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse


router = APIRouter(tags = ["Users"])

class User(BaseModel):
    id: int
    name: str
    surname: str
    age: int
    email: str

users_list = [User(id= 1, name= "Carlos", surname= "Acevedo", email= "carlitos@gmail.com", age= 23),
              User(id= 2, name= "Arturo", surname= "Ceballos", email= "Arturo@gmail.com", age= 25),
              User(id= 3, name= "Brais", surname= "Moure", email= "Brais@gmail.com", age= 35)]

@router.get('/usersjson')
async def usersjson():
    return [{'name': 'Carlos', 'surname': 'Acevedo',"age":23, 'email':'carlitosaac16@gmail.com'},
           {'name': 'Arturo', 'surname': 'Ceballos',"age": 25, 'email':'Arturo@gmail.com'},
            {'name': 'Brais', 'surname': 'Moure',"age": 35, 'email':'Brais@gmail.com'}]


#
@router.get('/users')
async def users():
    return users_list


#Path
@router.get('/user/{id}')
async def user_id(id: int):
    return search_user(id)
    

# Query
@router.get("/userquery/")
async def user_id(id: int):
    return search_user(id)
    

#Busqueda de usuario
def search_user(id: int):
    user = filter(lambda user: user.id == id, users_list)
    try:
        return list(user)[0]
    except:
        return{"error":"No se ha encontrado el usuario"}

@router.post('/user/', status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
  
    users_list.append(user)
    return user

@router.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if not found:
        return{"message": "No se ha actualizado el usuario"}
    
    return user

@router.delete("/user/{id}")
async def user(id: int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
            return JSONResponse(status_code=200 , content= {"message": "Se ha eliminado el usuario satisfactoriamente"})
            

    if not found:
        return JSONResponse(status_code=404, content={"message":"No se ha eliminado el usuario"})
    
    

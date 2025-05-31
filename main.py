from fastapi import FastAPI
from models import User,Gender,Role
from typing import List
from uuid import uuid4
app=FastAPI() 

db:List[User]=[
     User(id=uuid4(),first_name="Akshit",last_name="Sahore",gender=Gender.male,roles=[Role.admin,Role.user]),
     User(id=uuid4(),first_name="Akshit",last_name="Sahore",gender=Gender.male,roles=[Role.admin,Role.user])
]

@app.get('/')
def root():
    return{"Hello":"Akshit"}  
@app.get('/t') 
def root2(): 
      return {"hello":"world"}

@app.get('/api/v1/users')
async def fetch_users():
    return db;

@app.post('/api/v1/users')
async def register_user(user:User):
     db.append(user)
     return {"id":user.id}       
     
@app.post('/api/v1/users')
def create_user(name: str):
    return {"message": f"User {name} created"}


@app.get('/api/v1/users/{user_id}')
def get_user(user_id: int):
    return {"user_id": user_id}

@app.get('/delete')
def delete_user(user_id:User):
     db.remove(user_id)
import fastapi
from fastapi import Request
import pydantic_models
import config
import database
import copy

api = fastapi.FastAPI()


fake_database = {'users':[
    {
        "id":1,
        "name":"Anna",
        "nick":"Anny42",
        "balance": 15300
     },

    {
        "id":2,
        "name":"Dima",
        "nick":"dimon2319",
        "balance": 160.23
     },
    {
        "id":3,
        "name":"Vladimir",
        "nick":"Vova777",
        "balance": 200.1
     }
    ], }


@api.get('/get_info_by_user_id/{id:int}')
def get_info_by_user_id(id):
    return fake_database['users'][id-1]

@api.get('/get_user_balance_by_id/{id:int}')
def get_user_balance_by_id(id): 
    return fake_database['users'][id-1]['balance']

@api.get('/get_total_balance')
def get_total_balance(): 
    total_balance: float = 0.0
    for user in fake_database['users']:
        total_balance += pydantic_models.User(**user).balance
    return total_balance

@api.get("/users/")
def get_users(skip: int = 0, limit: int = 10):
    return fake_database['users'][skip: skip + limit]

@api.get('/user/{user_id}')
def read_user(user_id: str, query: str | None = None):
    if query: 
        return {'user_id': user_id, 'query': query}
    return {'user_id': user_id}



@api.post('/user/create')
def create_user(user: pydantic_models.User):
    fake_database["users"].append(user)
    return {"User created": user}



@api.put('/user/{user_id}')
def update_user(user_id: int, user: pydantic_models.User = fastapi.Body()):
    for index, u in enumerate(fake_database['users']):
        if u['id'] == user_id:
            fake_database['users'][index] = user 
            return user

@api.delete('/user/{user_id}')
def delete_usesr(user_id: int = fastapi.Path()): 
    for index, u in enumerate(fake_database["users"]): 
        if u['id'] == user_id: 
            old_db = copy.deepcopy(fake_database)
            del fake_database["users"][index]
            return {"old db": old_db, 
                    "new db": fake_database
                    }

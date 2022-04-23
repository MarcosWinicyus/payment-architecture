import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://frontend:4444'],
    allow_methods=['*'],
    allow_headers=['*']
)


class Login(BaseModel):
    taxId: str = Field(...)
    password: str = Field(...)

    class Config:
        extra = 'forbid'


@app.post('/auth')
async def auth(credentials: Login):

    req = requests.get('http://costumer:8002/costumers',
                       json={"search": credentials.dict().get("taxId", " ")})
    costumer = req.json()

    if costumer != []:

        if credentials.dict().get("password", "") == costumer[0]['password']:
            return {
                "status": "authorized",
                "permission": costumer[0]['permission'],
                "cart_id": costumer[0]['cart_id'],
                "costumer_id": costumer[0]['pk'],
            }

        return HTTPException(status_code=401, detail={"status": "unauthorized", "message": "Password does not match!"})

    raise  HTTPException(status_code=401, detail={"status": "unauthorized", "message": "Customer not found!"})

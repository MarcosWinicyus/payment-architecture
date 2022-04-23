from typing import Dict, Optional
from fastapi import FastAPI
from pydantic import ValidationError
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel, Field, Migrator

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://frontend:4444'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-15948.c83.us-east-1-2.ec2.cloud.redislabs.com",
    port=15948,
    password="IcoTLgtPCgY0S5fuakvn91SK1IYxQo1d",
    decode_responses=True
)


class Coustumer(HashModel):
    name: str = Field(index=True)
    taxId: str = Field(index=True)
    password: str
    permission: str
    cart_id: Optional[str]
    
    class Meta:
        database = redis

Migrator().run()

def format(pk: str):
    costumer = Coustumer.get(pk)

    return {
        'id': costumer.pk,
        'name': costumer.name,
        'taxId': costumer.taxId,
        'password': costumer.password,
        "permission": costumer.permission,
        'cart_id': costumer.cart_id,
    }


@app.post('/costumers')
def create(costumer: Dict):
    
    try:
        costumer = Coustumer(
            name=costumer['name'],
            taxId=costumer['taxId'],
            password=costumer['password'],
            permission=costumer['permission'],
        )
    except ValidationError as e:
        raise e
        
    return costumer.save()


@app.get('/costumers/{pk}')
def get(pk: str):
    return Coustumer.get(pk)

@app.patch('/costumers/{pk}')
def edit(data: Coustumer, pk : str):
    

    costumer = Coustumer.get(pk)
    
    data = data.dict()
    
    if data.get('name'):
        costumer.name = data['name'] 
        
    if data.get('taxId'):
        costumer.taxId = data['taxId']
    
    if data.get('permissions'):
        costumer.permissions = data['permissions']
    
    costumer.save()
    
    return Coustumer.get(pk)

@app.get('/costumers')
def find(data: Dict):
    if data.get('search') and data['search'] != '':
        return Coustumer.find(
                  (Coustumer.name == data['search']) |
                  (Coustumer.taxId == data['search'])
              ).all()
              
    return Coustumer.find().all()

@app.post('/costumers/set_shopping_cart/{pk}')
def set_shopping_cart(data: Dict, pk : str):

    costumer = Coustumer.get(pk)
    costumer.cart_id = data['cart_id']
    costumer.save()
    
    return Coustumer.get(pk)
    
@app.delete('/costumers/{pk}')
def delete(pk: str):
    return Coustumer.delete(pk)

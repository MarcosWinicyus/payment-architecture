from typing import Dict
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

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


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get('/products')
def all():
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)

    return {
        'id': product.pk,
        'name': product.name,
        'price': product.price,
        'quantity': product.quantity
    }


@app.post('/products')
def create(product: Product):
    return product.save()


@app.get('/products/{pk}')
def get(pk: str):
    return Product.get(pk)

@app.patch('/products/{pk}')
def edit(data: Product, pk : str):
    

    product = Product.get(pk)
    
    data = data.dict()
    
    if data.get('name'):
        product.name = data['name'] 
        
    if data.get('price'):
        product.price = data['price'] 
        
    if data.get('quantity'):
        product.quantity = data['quantity']
        
    product.save()
    
    return Product.get(pk)


@app.post('/products/subtract_stock/{pk}')
def subtract_stock(data: Dict, pk : str):

    product = Product.get(pk)
    product.quantity = product.quantity - int(data['quantity'])
    product.save()
    
    return Product.get(pk)
    
@app.delete('/products/{pk}')
def delete(pk: str):
    return Product.delete(pk)

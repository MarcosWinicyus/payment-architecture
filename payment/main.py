from typing import Dict, Optional
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests, time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://frontend:4444'],
    allow_methods=['*'],
    allow_headers=['*']
)

# This should be a different database
redis = get_redis_connection(
    host="redis-15948.c83.us-east-1-2.ec2.cloud.redislabs.com",
    port=15948,
    password="IcoTLgtPCgY0S5fuakvn91SK1IYxQo1d",
    decode_responses=True
)


class Order(HashModel):
    product_id: Optional[str]
    name: Optional[str]
    price: Optional[float]
    fee: Optional[float]
    total: Optional[float]
    quantity: Optional[int]
    status: Optional[str] # pending, completed, refunded, 

    class Meta:
        database = redis

@app.get('/orders')
def all():
    return [format(pk) for pk in Order.all_pks()]

def format(pk: str):
    order = Order.get(pk)

    return {
        'id': order.pk,
        'product_id': order.product_id,
        'price': order.price,
        'fee': order.fee,
        'quantity': order.quantity,
        'status' : order.status   
    }
    
@app.get('/orders/{pk}')
def get(pk: str):
    return Order.get(pk)
    
@app.post('/orders')
async def create(request: Request, background_tasks: BackgroundTasks):  # id, quantity

    body = await request.json()

    req = requests.get('http://inventory:8000/products/%s' % body['id'])
    product = req.json()

    order = Order(
        product_id=body['id'],
        product_name=body['name'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()

    background_tasks.add_task(order_completed, order)

    return order

@app.delete('/orders/{pk}')
def delete(pk: str):
    return Order.delete(pk)


# @app.post('/orders/set_status/{pk}')
# def subtract_stock(data: Dict, pk : str):

#     orders = Order.get(pk)
#     orders.status = int(data['status'])
#     orders.save()
    
#     return Order.get(pk)

def order_completed(order: Order):

    # background tasks to process the order 
    
    time.sleep(5)
    order.status = 'completed'
    order.save()
    redis.xadd('order_completed', order.dict(), '*')
    # Criando o evendo com o redis streams, será a forma que o nosso inventario irá consumir a informação

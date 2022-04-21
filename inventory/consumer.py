# from main import redis, Product
import time
import requests
# import redis
from redis_om import get_redis_connection, HashModel, Migrator

# r = redis.Redis(
#     host='redis-15948.c83.us-east-1-2.ec2.cloud.redislabs.com',
#     port=15948, 
#     password='IcoTLgtPCgY0S5fuakvn91SK1IYxQo1d')
    
    
redis = get_redis_connection(
    host="redis-15948.c83.us-east-1-2.ec2.cloud.redislabs.com",
    port=15948,
    password="IcoTLgtPCgY0S5fuakvn91SK1IYxQo1d",
    decode_responses=True
)



# class Product(HashModel):
#     name: str
#     price: float
#     quantity: int

#     class Meta:
#         database = redis
        
key = 'order_completed'
group = 'inventory-group'

try:
    redis.xgroup_create(key, group)
except:
    print('Group already exists!')

while True:
    
    try:
        results = redis.xreadgroup(group, key, {key: '>'}, None)
                
        if results != []:
            for result in results:
                print(results)
                obj = result[1][0][1]
                try:
                    response = requests.post(
                            f"http://inventory:8000/products/subtract_stock/{obj['product_id']}", 
                            json= {"quantity" : obj['quantity'] }
                            )
                    
                    response.raise_for_status()
                    
                    # Por problemas na utilização do redis OM  foi feioto o paleativo acima
                    
                    # print(redis.execute_command('JSON.GET', obj['product_id']))                    
                    # product = Product.get(obj['product_id'])
                    # product.quantity = product.quantity - int(obj['quantity'])
                    # product.save()
                    # print(product)
                except:
                    
                    redis.xadd('refund_order', obj, '*')

    except Exception as e:
        print(str(e))
    time.sleep(2)

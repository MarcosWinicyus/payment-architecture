import time
import streamlit as st
import requests


def get_orders():
    resp = requests.get("http://payment:8001/orders")
    orders = resp.json()    
    return orders

def delete_order(id):
    
    resp = requests.delete(f"http://payment:8001/orders/{id}")
    response = resp.json()
    return response

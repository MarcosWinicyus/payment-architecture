import time
import streamlit as st
import requests

# @st.cache
def get_products():
    resp = requests.get("http://inventory:8000/products")
    products = resp.json()
    return products

# @st.cache
def post_product(payload):
    resp = requests.post("http://inventory:8000/products", json=payload)
    response = resp.json()
    return response

def delete_product(id):
    
    resp = requests.delete(f"http://inventory:8000/products/{id}")
    response = resp.json()
    return response
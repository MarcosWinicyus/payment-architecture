import pandas as pd
import streamlit as st
import requests

def product_form():

    st.title("New Product")
    
    with st.form(key='product_form'):
        name = st.text_input(label='Name:')
        
        col1, col2, col3 = st.columns(3)
    
        price = col1.number_input(label='Price:')
        quantity = col2.number_input(label='Quantity:')
        submit_button = col3.form_submit_button(label='Submit')
    
        if submit_button:
            payload = {
                "name": name,
                "price": float(price),
                "quantity": int(quantity)
            }
            
            resp = requests.post("http://inventory:8000/products", json=payload)
            json = resp.json()
            st.write(json)
            
def list_products():
    st.title("Inventory List")
            
    resp = requests.get("http://inventory:8000/products")
    products = resp.json()
    
    margin, col1, col2, col3, col4 = st.columns([0.2, 1.5, 1, 1, 0.5])
    
    col1.markdown(f'<h1 style="color:#2a628f;font-size:34px;">{"Nome"}</h1>', unsafe_allow_html=True)
    col2.markdown(f'<h1 style="color:#2a628f;font-size:34px;">{"Price"}</h1>', unsafe_allow_html=True)
    col3.markdown(f'<h1 style="color:#2a628f;font-size:34px;">{"Quantity"}</h1>', unsafe_allow_html=True)
        
    for product in products:
       
        
        with st.expander("",expanded=True):
            margin, col1, col2, col3, col4 = st.columns([0.2, 1.5, 1, 1, 0.5])
             
            with col1:
                st.markdown(f'<h2 font-size:28px;">{product["name"]}</h2>', unsafe_allow_html=True)
                st.markdown(" ")   
            with col2:
                st.markdown(f'<h2 font-size:28px;">{product["price"]}</h2>', unsafe_allow_html=True)
                st.markdown(" ")  
            with col3:
                st.markdown(f'<h2 font-size:28px;">{product["quantity"]}</h2>', unsafe_allow_html=True)
           
            with col4:
                st.button("🗑️", key= product["id"]+" "+"delete")
                st.button("📝", key= product["id"]+" "+"edit")

def inventory():
    
    product_form()
    st.markdown("""---""")
    list_products()
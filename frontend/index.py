from itertools import product
from unicodedata import name
import pandas as pd
import streamlit as st
import requests

st.set_page_config(layout="wide")
st.title("Hello World!")

with st.form(key='create_product'):
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
        

resp = requests.get("http://inventory:8000/products")
products = resp.json()
# products = pd.DataFrame(resp.json())
# del products['id']
# st.dataframe(products)

# st.markdown(
#         f"""
#             <style>
#                 section[tabindex="0"].main div.stButton button {{width: 105%;}}
#                 section[tabindex="0"].main div.row-widget.stButton button {{
#                     height: 90px; position: absolute;bottom: 0px;
#                     background: transparent; left: -2.4%; 
#                     border-radius: 8px;}}
#                 section[tabindex="0"].main h2 a {{display:none;}}
#                 section[tabindex="0"].main [data-testid="stHorizontalBlock"]:nth-child(n+3) :last-child[data-testid="column"] {{margin-top: 14px;}}
#             </style>
#         """,
#         unsafe_allow_html=True,
#     )
    
col1, col2, col3 = st.columns(3)

col1.markdown(f'<h1 style="color:#2a628f;font-size:24px;">{"Nome"}</h1>', unsafe_allow_html=True)
col2.markdown(f'<h1 style="color:#2a628f;font-size:24px;">{"Price"}</h1>', unsafe_allow_html=True)
col3.markdown(f'<h1 style="color:#2a628f;font-size:24px;">{"Quantity"}</h1>', unsafe_allow_html=True)
    
for product in products:
   
    
    with st.expander("",expanded=True):
        col1, col2, col3 = st.columns(3)
         
        with col1:
            st.markdown(f'<h2 font-size:35px;">{product["name"]}</h2>', unsafe_allow_html=True)
                
        with col2:
            st.markdown(f'<h2 font-size:35px;">{product["price"]}</h2>', unsafe_allow_html=True)
            
        with col3:
            st.markdown(f'<h2 font-size:35px;">{product["quantity"]}</h2>', unsafe_allow_html=True)
        
        # click = st.button(label="", key=product["id"])
        
        # if click:
        #     print("Abrido")
import streamlit as st
import requests
from src.requests.inventory import get_products, post_product, delete_product

    
def product_form():

    st.title("New Product")
    
    

    with st.form(key='product_form'):
        name = st.text_input(label='Name:')
        
        col1, col2 = st.columns(2)
    
        price = col1.number_input(label='Price:', min_value=1.0)
        quantity = col2.number_input(label='Quantity:', min_value=1)
        
        buff, center, buff = st.columns([1, 0.1, 1])
        submit_button = center.form_submit_button(label='Submit')
    
        if submit_button:
            payload = {
                "name": name,
                "price": float(price),
                "quantity": int(quantity)
            }
            json = post_product(payload)
            st.write(json)
            
def list_products():
    st.title("Inventory List")
            
    with st.spinner('Wait for it...'):

        products = get_products()
        
        margin, col1, col2, col3, col4, buff = st.columns([0.2, 1.5, 1, 1, 0.2, 0.7])
        
        col1.markdown(f'<h1 style="color:#2a628f;font-size:34px;">{"Nome"}</h1>', unsafe_allow_html=True)
        col2.markdown(f'<h1 style="color:#2a628f;font-size:34px;">{"Price"}</h1>', unsafe_allow_html=True)
        col3.markdown(f'<h1 style="color:#2a628f;font-size:34px;">{"Quantity"}</h1>', unsafe_allow_html=True)
        col4.markdown(f'<h2 style="color:#2a628f;font-size:24px;">{"Actions"}</h2>', unsafe_allow_html=True)
        
        for product in products:
            with st.expander("",expanded=True):
                margin, col1, col2, col3, col4, buff = st.columns([0.2, 1.5, 1, 1, 0.2, 0.5])
                 
                with col1:
                    st.markdown(f'<h2 font-size:28px;">{product["name"]}</h2>', unsafe_allow_html=True)
                    st.markdown(" ")   
                with col2:
                    st.markdown(f'<h2 font-size:28px;">{product["price"]}</h2>', unsafe_allow_html=True)
                    st.markdown(" ")  
                with col3:
                    st.markdown(f'<h2 font-size:28px;">{product["quantity"]}</h2>', unsafe_allow_html=True)
                    
                with col4:
                    
                    st.button("📝", key= product["id"]+" "+"edit")
                    
                    delete_btn = st.button("🗑️", key= product["id"]+" "+"delete")
                    
                with buff:
                    if delete_btn:
                        st.error("Do you really,  wanna do this?")
                        st.button("Yes I'm want", on_click = delete_product, args = (product["id"], ))
                        # st.button("Yes I'm want", on_click= delete_product, orgs=(product["id"], )  ):                        
                        st.button("Cancel")
                            
def inventory():
    
    product_form()
    st.markdown("""---""")
    list_products()
    

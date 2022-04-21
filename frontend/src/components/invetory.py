import streamlit as st
import requests
from src.requests.inventory import get_products, post_product, delete_product, patch_product


def new_product():
    st.session_state["product_selected"] = {}
    st.session_state["layout"] = 'new_product'

def edit_product(product):
    
    st.session_state["product_selected"] = product
    st.session_state["layout"] = 'edit_product'

def expander_expanded(id):
    if st.session_state["layout"] == 'edit_product':
        return id == st.session_state["product_selected"].get("id", None)
    return True
    
def product_form():

    st.title("New Product") if st.session_state["product_selected"] == {
    } else st.button("🔙 Insertion", on_click=new_product)
    
    with st.form(key='product_form'):
    
        if st.session_state["product_selected"] != {}:
            st.header(f"📝  {st.session_state['product_selected'].get('name', '')}")
        
        name = st.text_input(
            label='Name:', value=st.session_state["product_selected"].get('name', ''))

        col1, col2 = st.columns(2)

        price = col1.number_input(label='Price:', min_value=1.0,
                                  value=st.session_state["product_selected"].get('price', 1.0), step=1.0)
        quantity = col2.number_input(
            label='Quantity:', min_value=1,  value=st.session_state["product_selected"].get('quantity', 1))

        buff, center, buff = st.columns([1, 0.1, 1])
        submit_button = center.form_submit_button(label='Submit')

        if submit_button:
            payload = {
                "name": name,
                "price": float(price),
                "quantity": int(quantity)
            }
            
            if st.session_state["layout"] == 'new_product':
                json = post_product(payload)
                
            elif st.session_state["layout"] == 'edit_product':
                json = patch_product(st.session_state["product_selected"]["id"], payload)

def list_products():
    st.title("Inventory List")

    with st.spinner('Wait for it...'):

        products = get_products()

        margin, col1, col2, col3, col4, buff = st.columns(
            [0.2, 1.5, 1, 1, 0.2, 0.7])

        col1.markdown(
            f'<h1 style="color:#2a628f;font-size:34px;">{"Nome"}</h1>', unsafe_allow_html=True)
        col2.markdown(
            f'<h1 style="color:#2a628f;font-size:34px;">{"Price"}</h1>', unsafe_allow_html=True)
        col3.markdown(
            f'<h1 style="color:#2a628f;font-size:34px;">{"Quantity"}</h1>', unsafe_allow_html=True)
        col4.markdown(
            f'<h2 style="color:#2a628f;font-size:24px;">{"Actions"}</h2>', unsafe_allow_html=True)

        for product in products:
            with st.expander("", expanded=expander_expanded(product['id'])):
                margin, col1, col2, col3, col4, buff = st.columns(
                    [0.2, 1.5, 1, 1, 0.2, 0.5])

                with col1:
                    st.markdown(
                        f'<h2 font-size:28px;">{product["name"]}</h2>', unsafe_allow_html=True)
                    st.markdown(" ")
                with col2:
                    st.markdown(
                        f'<h2 font-size:28px;">{product["price"]}</h2>', unsafe_allow_html=True)
                    st.markdown(" ")
                with col3:
                    st.markdown(
                        f'<h2 font-size:28px;">{product["quantity"]}</h2>', unsafe_allow_html=True)

                with col4:

                    st.button(
                        "📝", key=f"{product['id']}/edit", on_click=edit_product, args=(product,))

                    delete_btn = st.button("🗑️", key=f"{product['id']}/delete")

                with buff:
                    if delete_btn:
                        st.error("Do you really,  wanna do this?")
                        st.button("Yes I'm want", on_click=delete_product, args=(
                            product["id"], ))
                        st.button("Cancel")


def inventory():

    if not "layout" in st.session_state:
        st.session_state["layout"] = 'new_product'

    if st.session_state["layout"] == 'new_product':

        st.session_state["expanded_list"] = True
        product_form()
        st.markdown("""---""")
        list_products()

    elif st.session_state["layout"] == 'edit_product':

        st.session_state["expanded_list"] = False
        product_form()
        st.markdown("""---""")
        list_products()

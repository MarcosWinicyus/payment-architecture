import streamlit as st
import requests
from src.requests.payment import get_orders, delete_order

def list_orders():
    st.title("Orders List")

    with st.spinner('Wait for it...'):

        orders = get_orders()

        margin, col1, col2, col3, col4, col5, col6, buff = st.columns(
            [0.2, 1.3, 1, 1, 1, 0.8, 0.3, 0.2])
        
        col1.markdown(
            f'<h1 style="color:#2a628f;font-size:24px;">{"Product ID"}</h1>', unsafe_allow_html=True)
        col2.markdown(
            f'<h1 style="color:#2a628f;font-size:24px;">{"Fee"}</h1>', unsafe_allow_html=True)
        col3.markdown(
            f'<h1 style="color:#2a628f;font-size:24px;">{"Quantity"}</h1>', unsafe_allow_html=True)
        col4.markdown(
            f'<h2 style="color:#2a628f;font-size:24px;">{"Price"}</h2>', unsafe_allow_html=True)
        col5.markdown(
            f'<h2 style="color:#2a628f;font-size:24px;">{"Status"}</h2>', unsafe_allow_html=True)
        col6.markdown(
            f'<h2 style="color:#2a628f;font-size:18px;">{"Actions"}</h2>', unsafe_allow_html=True)

        for order in orders:
            
            with st.expander("", expanded=True):
                margin, col1, col2, col3, col4, col5, col6, buff = st.columns(
                    [0.2, 1.3, 1, 1, 1, 0.8, 0.3, 0.2])

                with col1:
                    st.text(order["product_id"])
                    
                with col2:
                    st.markdown(
                        f'<h2 font-size:24px;">{order["fee"]}</h2>', unsafe_allow_html=True)

                with col3:
                    st.markdown(
                        f'<h2 font-size:24px;">{order["quantity"]}</h2>', unsafe_allow_html=True)
                with col4:
                    st.markdown(
                        f'<h2 font-size:24px;">{order["price"]}</h2>', unsafe_allow_html=True)
                with col5:
                    st.error(order["status"]) if order["status"] == "called_off" or order["status"] == "refunded" else ...
                    st.info(order["status"]) if order["status"] == "pending" else ...
                    st.success(f"{order['status']} \n") if order["status"] == "completed" else ...

                with col6:

                    delete_btn = st.button("🗑️", key=f"{order['id']}/delete")

        
                    if delete_btn:
                        st.error("Do you really,  wanna do this?")
                        st.button("Yes I'm want", on_click=delete_order, args=(
                            order["id"], ))
                        st.button("Cancel")


def orders():

    if st.session_state["layout"] == 'list_orders':
        list_orders()

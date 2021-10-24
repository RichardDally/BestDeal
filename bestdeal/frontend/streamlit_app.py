import streamlit as st
from pymongo import MongoClient
from datetime import datetime, timezone
from bestdeal.core.pricedatabase import PriceDatabase


# Backend initialization
mc = MongoClient(st.secrets["MONGODB_CONNECTION_STRING"])
db = PriceDatabase(collection_name="GPU", client=mc)

product_types = db.find_distinct_product_types()
selected_product_type = st.sidebar.selectbox("Product type", product_types)
selected_date = st.sidebar.date_input(label="Date", value=datetime.now(timezone.utc))


for post in db.find_all_posts_by_product_type(selected_product_type, selected_date.strftime("%Y%m%d")):
    st.write(post)

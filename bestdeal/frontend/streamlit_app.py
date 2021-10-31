from typing import List
import streamlit as st
from pymongo import MongoClient
from datetime import datetime, timezone
from bestdeal.core.pricedatabase import PriceDatabase


# Backend initialization
mc = MongoClient(st.secrets["MONGODB_CONNECTION_STRING"])
db = PriceDatabase(collection_name="GPU", client=mc)

# product_types = db.find_distinct_product_types()
selected_date = st.sidebar.date_input(label="Date", value=datetime.now(timezone.utc))
formatted_selected_date = selected_date.strftime("%Y%m%d")

# Find available product
available_product_types: List[str] = db.find_distinct_criteria_by_date("product_type", formatted_selected_date)
if not available_product_types:
    st.error(f"No available records for date [{formatted_selected_date}]")
    st.stop()

# Fill filters
available_sources: List[str] = db.find_distinct_criteria_by_date("source", formatted_selected_date)
available_brands: List[str] = db.find_distinct_criteria_by_date("product_brand", formatted_selected_date)

# Filter selection
selected_product_type = st.sidebar.selectbox("Product type", available_product_types)
selected_source = st.sidebar.selectbox("Source", available_sources)
selected_brand = st.sidebar.selectbox("Brand", available_brands)

search = st.sidebar.button(label="Search")

if search and selected_product_type:
    mongo_cursor = db.find_all_posts_by_product_type(selected_product_type, selected_date.strftime("%Y%m%d"))
    if mongo_cursor.count():
        for post in mongo_cursor:
            st.write(post)
    else:
        st.info(f"Nothing to display for [{selected_product_type}]")
else:
    st.info(f"Select a product type and click on Search")

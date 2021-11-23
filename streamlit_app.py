import pandas as pd
from typing import List
import streamlit as st
from loguru import logger
from pymongo import MongoClient, ASCENDING
from datetime import datetime, timezone, date
from bestdeal.pricedatabase import PriceDatabase
from bestdeal.toolbox import date_range


class Frontend:
    def __init__(self):
        mc = MongoClient(st.secrets["MONGODB_CONNECTION_STRING"])
        self.db = PriceDatabase(collection_name="GPU", client=mc)

    def display_filters(self):
        with st.sidebar.expander(label="Filters", expanded=True):
            self.selected_product_type = st.selectbox("Product type", ["All"] + self.available_product_types)
            self.selected_brand = st.selectbox("Brand", ["All"] + self.available_brands)
            self.selected_source = st.selectbox("Source", ["All"] + self.available_sources)
            self.apply_filters_clicked = st.button(label="Apply filters")
            self.pick_cheapest_clicked = st.button(label="Pick cheapest")

    def find_by_filters(self):
        return self.db.find_all_posts_by_filters(
            datetime_regex=self.formatted_selected_date,
            product_type=self.selected_product_type if self.selected_product_type != "All" else None,
            product_brand=self.selected_brand if self.selected_brand != "All" else None,
            source=self.selected_source if self.selected_source != "All" else None,
        )

    def pick_cheapest_by_filters(self):
        mongo_cursor = self.find_by_filters()
        second_cursor = mongo_cursor.sort("product_price", ASCENDING)
        for post in second_cursor.limit(1):
            return post

    def apply_filters(self):
        mongo_cursor = self.find_by_filters()
        if mongo_cursor.count():
            for post in mongo_cursor:
                st.write(post)
        else:
            st.info(
                f"Nothing to display for [{self.selected_product_type}], "
                f"[{self.selected_brand}] "
                f"and [{self.selected_source}]"
            )



    def display_graph(self):
        self.year = 2021
        # self.start_date = date(year=self.year, month=1, day=1)
        # self.end_date = date(year=self.year, month=12, day=31)
        self.start_date = date(year=self.year, month=11, day=1)
        self.end_date = date(year=self.year, month=11, day=7)
        logger.info('Prepare prices from [{}] to [{}]'.format(self.start_date, self.end_date))

        # dico = {
        #     'LDLC': {"20211101": 1, "20211102": 2},
        #     'TopAchat': {"20211101": 1, "20211102": 2},
        # }

        # dico = {}
        # for product_type in ["3080"]:
        #     dico[product_type] = {}
        #     for single_date in date_range(self.start_date, self.end_date):
        #         current_date = single_date.strftime("%Y%m%d")
        #         all_posts = self.db.find_all_posts_by_filters(
        #             datetime_regex=current_date,
        #             product_type=product_type,
        #         )
        #         logger.info(current_date)
        #         cheapest_post = self.db.find_cheapest_from_cursor(mongo_cursor=all_posts)
        #         if cheapest_post:
        #             dico[product_type][current_date] = cheapest_post["product_price"]
        #
        # st.write(dico)
        # chart_data = pd.DataFrame(dico)
        # st.line_chart(chart_data)

    def main(self):
        self.selected_date = st.sidebar.date_input(label="Date", value=datetime.now(timezone.utc))
        self.formatted_selected_date = self.selected_date.strftime("%Y%m%d")

        # Find available product
        self.available_product_types: List[str] = self.db.find_distinct_criteria_by_date(
            criteria="product_type",
            datetime_regex=self.formatted_selected_date,
        )
        if not self.available_product_types:
            st.error(f"No available records for date [{self.formatted_selected_date}]")
            st.stop()

        # Fill filters
        self.available_sources: List[str] = self.db.find_distinct_criteria_by_date(
            criteria="source",
            datetime_regex=self.formatted_selected_date,
        )
        self.available_brands: List[str] = self.db.find_distinct_criteria_by_date(
            criteria="product_brand",
            datetime_regex=self.formatted_selected_date,
        )
        self.display_filters()

        no_click = True
        if self.pick_cheapest_clicked:
            mongo_post = self.pick_cheapest_by_filters()
            st.write(mongo_post)
            no_click = False
        if self.apply_filters_clicked:
            self.apply_filters()
            no_click = False

        if no_click:
            st.info(f"Select a product type and click on Search")

        self.display_graph()


if __name__ == '__main__':
    frontend = Frontend()
    frontend.main()

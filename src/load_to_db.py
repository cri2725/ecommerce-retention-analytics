import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
user=os.getenv("DB_USER")
password=os.getenv("DB_PASSWORD")
db_name=os.getenv("DB_NAME")

connection_string = f"mysql+pymysql://{user}:{password}@localhost:3306/{db_name}"
engine=create_engine(connection_string)
dizionario={os.path.join("data","olist_customers_dataset.csv"):"customers",
            os.path.join("data","olist_geolocation_dataset.csv"):"geolocation",
            os.path.join("data","olist_order_items_dataset.csv"):"order_items",
            os.path.join("data","olist_order_payments_dataset.csv"):"order_payments",
            os.path.join("data","olist_order_reviews_dataset.csv"):"order_reviews",
            os.path.join("data","olist_orders_dataset.csv"):"orders",
            os.path.join("data","olist_products_dataset.csv"):"products",
            os.path.join("data","olist_sellers_dataset.csv"):"sellers",
            os.path.join("data","product_category_name_translation.csv"):"product_category_name_translation"}

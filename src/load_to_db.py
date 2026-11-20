"""
ETL, estrae i file CSV grezzi del dataset, pulisce i tipi di dato (date e duplicati) e carica su MySQL
"""

import os
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

FILES_TO_TABLES={os.path.join("data", "olist_customers_dataset.csv"):"customers",
            os.path.join("data", "olist_geolocation_dataset.csv"):"geolocation",
            os.path.join("data", "olist_order_items_dataset.csv"):"order_items",
            os.path.join("data", "olist_order_payments_dataset.csv"):"order_payments",
            os.path.join("data", "olist_order_reviews_dataset.csv"):"order_reviews",
            os.path.join("data", "olist_orders_dataset.csv"):"orders",
            os.path.join("data", "olist_products_dataset.csv"):"products",
            os.path.join("data", "olist_sellers_dataset.csv"):"sellers",
            os.path.join("data", "product_category_name_translation.csv"):"product_category_name_translation"}
def get_engine():
    """Carica le variabili dal .env e crea l'engine"""
    load_dotenv()
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    db_name = os.getenv("DB_NAME")
    if not all([user, password, db_name]):
        raise ValueError("credenziali mncanti nel .env")

    connection_string = f"mysql+pymysql://{user}:{password}@localhost:3306/{db_name}"
    return create_engine(connection_string)

def run_etl():
    """Carica le tabelle su MySQL"""
    engine = get_engine()
    try:
        for file_path, table_name in FILES_TO_TABLES.items():
            df=pd.read_csv(file_path)
            for colonna in df.columns:
                if colonna.endswith(("_date", "_timestamp", "_at")):
                    df[colonna]=pd.to_datetime(df[colonna])
            if table_name == "geolocation":
                df=df.drop_duplicates()
            print(f"Caricamento del filepath: {file_path} nella tabella {table_name}.\nCi sono {len(df)} righe")
            df.to_sql(con=engine, name=table_name, if_exists="replace", index=False, chunksize=10000)
    except Exception as e:
        print(f"errore durante le etl: {e}")
        raise
    finally:
        engine.dispose()
        print(f"connessione chiusa")
if __name__ == "__main__":
    run_etl()
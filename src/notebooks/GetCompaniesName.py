# Databricks notebook source
import requests
import os
from src.db.connection import PostgresClient
from src.db.companies import CompanyRepository
from databricks.sdk.runtime import dbutils

for key in ["sec_name", "sec_email", "pg_user", "pg_password", "pg_host"]:
    dbutils.widgets.text(key, "")
os.environ["PG_USER"]     = dbutils.widgets.get("pg_user")
os.environ["PG_PASSWORD"] = dbutils.widgets.get("pg_password")
os.environ["PG_HOST"]     = dbutils.widgets.get("pg_host")
print("creating client...")
client = PostgresClient()
print("connected")
company = CompanyRepository(client=client)

def get_companies():
    name = dbutils.widgets.get("sec_name")
    email = dbutils.widgets.get("sec_email")
    HEADERS = {
        "User-Agent": f"{name} {email}",
        "Accept-Encoding": "gzip, deflate"
        }
    api_url = "https://www.sec.gov/files/company_tickers_exchange.json"
    response = requests.get(api_url, headers=HEADERS, timeout=30)
    response.raise_for_status()
    data = response.json()
    return data.get("data")

def run_pipeline():
    company.create_table()
    list_companies = get_companies()
    company.add_companies(list_companies)

run_pipeline()

from .connection import PostgresClient
from sqlalchemy import text
import pandas as pd


class CompanyRepository:

    def __init__(self,client:PostgresClient):
        self.client = client

    def create_table(self):
        with self.client.engine.begin() as connection:
            connection.execute(
                text(
                    """
                    CREATE TABLE IF NOT EXISTS alphalake.companies
                    (
                        CIK BIGSERIAL PRIMARY KEY,
                        ticker VARCHAR NOT NULL ,
                        company VARCHAR NOT NULL,
                        exchange VARCHAR NOT NULL,
                        updated_at TIMESTAMPTZ DEFAULT Now()
                    )
                    """
                )
            )

    def create_if_missing(self, CIK:int, ticker:str, company: str, exchange: str):
        insert_query = """
                            INSERT INTO alphalake.companies (CIK, ticker,company,exchange, updated_at)
                            VALUES (:CIK, :ticker, :company, :exchange, now())
                            ON CONFLICT (CIK) DO NOTHING;
                            """
        parameters = {"CIK": CIK, "ticker" : ticker, "company" : company, "exchange" : exchange}
        with self.client.engine.begin() as connection:
                connection.execute(text(insert_query), parameters)

    def get_cik(self, company_name: str):
            select_query = """
                SELECT *
                FROM alphalake.companies
                WHERE  company = :company_name
                ORDER BY updated_at DESC
            """
            parameters = {"company_name" : company_name}
            with self.client.engine.connect() as connection:
                result = connection.execute(text(select_query),parameters).mappings()
            return result

    def get_companies(self):
        select_query = """
            SELECT *
            FROM alphalake.companies 
            ORDER BY company ASC
        """
        conversation = []
        with self.client.engine.connect() as connection:
            result = connection.execute(text(select_query)).mappings().all()
            for row in result:
                conversation.append({"CIK":row["CIK"],
                                    "title":row["title"],
                                    "updated_at":row["updated_at"]})
        return conversation

    def add_companies(self, companies: list[dict]):
            insert_query = """
                                INSERT INTO alphalake.companies (CIK, ticker,company,exchange, updated_at)
                                VALUES (:CIK, :ticker, :company, :exchange, now())
                                ON CONFLICT (CIK) DO NOTHING;
                                """
            
            rows = [
            {
                "CIK": c[0],
                "company": c[1],
                "ticker": c[2],
                "exchange": c[3]
            }
            for c in companies if isinstance(c,dict)
            ]
            with self.client.engine.begin() as connection:
                connection.execute(text(insert_query), rows)
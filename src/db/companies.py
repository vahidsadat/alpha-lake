from .connection import PostgresClient
from sqlalchemy import text
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

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
                        CIK BIGINT,
                        ticker VARCHAR NOT NULL ,
                        company VARCHAR NOT NULL,
                        exchange VARCHAR,
                        updated_at TIMESTAMPTZ DEFAULT Now(),
                         PRIMARY KEY(CIK, ticker)
                    )
                    """
                )
            )

    def create_if_missing(self, CIK:int, ticker:str, company: str, exchange: str):
        insert_query = """
                            INSERT INTO alphalake.companies (CIK, ticker,company,exchange, updated_at)
                            VALUES (:CIK, :ticker, :company, :exchange, now())
                            ON CONFLICT (CIK, ticker)
                            DO UPDATE SET
                                company = EXCLUDED.company,
                                exchange = EXCLUDED.exchange,
                                updated_at = NOW()
                            WHERE
                                alphalake.companies.company IS DISTINCT FROM EXCLUDED.company
                                OR
                                alphalake.companies.exchange IS DISTINCT FROM EXCLUDED.exchange;
                                                            
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
                result = connection.execute(text(select_query),parameters).mappings().all()
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
                conversation.append({"cik": row["cik"], "company": row["company"], "updated_at": row["updated_at"]})
        return conversation

    def add_companies(self, companies: list[dict]):
            insert_query = """
                                INSERT INTO alphalake.companies (CIK, ticker,company,exchange, updated_at)
                                VALUES (:CIK, :ticker, :company, :exchange, now())
                                ON CONFLICT (CIK, ticker)
                                DO UPDATE SET
                                    company = EXCLUDED.company,
                                    exchange = EXCLUDED.exchange,
                                    updated_at = NOW()
                                WHERE
                                    alphalake.companies.company IS DISTINCT FROM EXCLUDED.company
                                    OR
                                    alphalake.companies.exchange IS DISTINCT FROM EXCLUDED.exchange;
                                """
            
            rows = [
            {
                "CIK": c[0],
                "company": c[1],
                "ticker": c[2],
                "exchange": c[3]
            }
            for c in companies if isinstance(c,(list,dict))
            ]
            logger.info("Received %d companies for synchronization", len(rows))
            if not rows:
                logger.warning("No companies to insert")
                return
            with self.client.engine.begin() as connection:
                result= connection.execute(text(insert_query), rows)
                inserted = result.rowcount
                logger.info(
                    "Company synchronization completed: "
                    "received=%d, inserted=%d, skipped=%d",
                    len(rows),
                    inserted,
                    len(rows) - inserted
        )
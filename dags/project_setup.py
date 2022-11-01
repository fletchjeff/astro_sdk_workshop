from datetime import datetime
from distutils.command.clean import clean

from airflow.models import DAG
from airflow.decorators import task
from pandas import DataFrame

# Import decorators and classes from the SDK
from astro import sql as aql
from astro.files import File
from astro.sql.table import Table

POSTGRES_CONN_ID = "astro_orders_sqlite"

dag = DAG(
    dag_id="project_setup",
    start_date=datetime(2019, 1, 1),
    schedule_interval="@once",
    catchup=False,
)

with dag:
    @task
    def create_minio_buckets():
        from minio import Minio
        client = Minio("host.docker.internal:9000", "minioadmin", "minioadmin",secure=False)
        if not client.bucket_exists("local-xcom"):
            client.make_bucket("local-xcom")

    create_minio_buckets()

    @aql.run_raw_sql
    def create_customers_table_1():
        return """
        DROP TABLE IF EXISTS customers_table;
        """
    @aql.run_raw_sql
    def create_customers_table_2():
        return """
        CREATE TABLE customers_table (customer_id CHAR(10), customer_name VARCHAR(100), type VARCHAR(10) );
        """
    @aql.run_raw_sql
    def create_customers_table_3():
        return """
        INSERT INTO customers_table (CUSTOMER_ID, CUSTOMER_NAME,TYPE) VALUES     ('CUST1','NAME1','TYPE1'),('CUST2','NAME2','TYPE1'),('CUST3','NAME3','TYPE2');
        """

    @aql.run_raw_sql
    def create_reporing_table_1():
        return """
        DROP TABLE IF EXISTS reporting_table;
        """

    @aql.run_raw_sql
    def create_reporing_table_2():
        return """
        CREATE TABLE reporting_table (
        CUSTOMER_ID CHAR(30), CUSTOMER_NAME VARCHAR(100), ORDER_ID CHAR(10), PURCHASE_DATE VARCHAR(100), AMOUNT FLOAT, TYPE CHAR(10));
        """

    @aql.run_raw_sql
    def create_reporing_table_3():
        return """
        INSERT INTO reporting_table (CUSTOMER_ID, CUSTOMER_NAME, ORDER_ID, PURCHASE_DATE, AMOUNT, TYPE) VALUES
        ('INCORRECT_CUSTOMER_ID','INCORRECT_CUSTOMER_NAME','ORDER2','2/2/2022',200,'TYPE1'),
        ('CUST3','NAME3','ORDER3','3/3/2023',300,'TYPE2'),
        ('CUST4','NAME4','ORDER4','4/4/2022',400,'TYPE2');
        """                        

    create_customers_table_1(conn_id=POSTGRES_CONN_ID) >> \
    create_customers_table_2(conn_id=POSTGRES_CONN_ID) >> \
    create_customers_table_3(conn_id=POSTGRES_CONN_ID)
    create_reporing_table_1(conn_id=POSTGRES_CONN_ID) >> \
    create_reporing_table_2(conn_id=POSTGRES_CONN_ID) >> \
    create_reporing_table_3(conn_id=POSTGRES_CONN_ID)                
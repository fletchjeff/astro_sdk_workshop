from datetime import datetime

from airflow.models import DAG
from pandas import DataFrame

# Import decorators and classes from the SDK
from astro import sql as aql
from astro.files import File
from astro.sql.table import Table

HTTP_FILE_PATH = "https://jfletcher-datasets.s3.eu-central-1.amazonaws.com/astro_demo"
POSTGRES_CONN_ID = "local_postgres"
POSTGRES_ORDERS = "orders_table"
POSTGRES_CUSTOMERS = "customers_table"
POSTGRES_REPORTING = "reporting_table"

# Define an SQL query for our transform step as a Python function using the SDK.
# This function filters out all rows with an amount value less than 150.
@aql.transform
def filter_orders(input_table: Table):
    return "SELECT * FROM {{input_table}} WHERE amount > 150"

# Define an SQL query for our transform step as a Python function using the SDK.
# This function joins two tables into a new table.
@aql.transform
def join_orders_customers(filtered_orders_table: Table, customers_table: Table):
    return """SELECT c.customer_id, customer_name, order_id, purchase_date, amount, type
    FROM {{filtered_orders_table}} f JOIN {{customers_table}} c
    ON f.customer_id = c.customer_id"""

# Define a function for transforming tables to dataframes
@aql.dataframe
def transform_dataframe(df: DataFrame):
    purchase_dates = df.loc[:, "purchase_date"]
    print("purchase dates:", purchase_dates)
    return purchase_dates

# Basic DAG definition. Run the DAG starting January 1st, 2019 on a daily schedule.
dag = DAG(
    dag_id="astro_orders",
    start_date=datetime(2019, 1, 1),
    schedule_interval="@daily",
    catchup=False,
)

with dag:
    # Extract a file with a header from the web into a temporary Table, referenced by the
    # variable `orders_data`
    orders_data = aql.load_file(
        # Data file needs to have a header row. The input and output table can be replaced with any
        # valid file and connection ID.
        input_file=File(
            path=HTTP_FILE_PATH + "/orders_data_header.csv",
        ),
        output_table=Table(conn_id=POSTGRES_CONN_ID),
    )

    # Create a Table object for customer data in the Postgres database
    customers_table = Table(
        name=POSTGRES_CUSTOMERS,
        conn_id=POSTGRES_CONN_ID,
    )

    # Filter the orders data and then join with the customer table,
    # saving the output into a temporary table referenced by the Table instance `joined_data`
    joined_data = join_orders_customers(filter_orders(orders_data), customers_table)

    # Merge the joined data into the reporting table based on the order_id.
    # If there's a conflict in the customer_id or customer_name, then use the ones from
    # the joined data
    # reporting_table = aql.merge(
    #     target_table=Table(
    #         name=POSTGRES_REPORTING,
    #         conn_id=POSTGRES_CONN_ID,
    #     ),
    #     source_table=joined_data,
    #     target_conflict_columns=["order_id"],
    #     columns=["customer_id", "customer_name"],
    #     if_conflicts="ignore",
    # )

    reporting_table = aql.append(
        target_table=Table(
            name=POSTGRES_REPORTING,
            conn_id=POSTGRES_CONN_ID,
        ),
        source_table=joined_data,
    )

    # Transform the reporting table into a dataframe
    purchase_dates = transform_dataframe(reporting_table)

    # Delete temporary and unnamed tables created by `load_file` and `transform`, in this example
    # both `orders_data` and `joined_data`
    aql.cleanup()
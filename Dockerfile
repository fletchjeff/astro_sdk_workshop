FROM quay.io/astronomer/astro-runtime:6.0.3

COPY tmp_sdk_fix/s3.py /usr/local/lib/python3.9/site-packages/astro/files/locations/amazon/s3.py

ENV AIRFLOW_CONN_AWS_DEFAULT='{\
    "conn_type": "aws",\
    "description": "",\
    "login": "minioadmin",\
    "password": "minioadmin",\
    "host": "",\
    "port": null,\
    "schema": "",\
    "extra": "{\"aws_access_key\": \"minioadmin\", \"aws_secret_access_key\": \"minioadmin\", \"endpoint_url\": \"http://host.docker.internal:9000\"}"\
  }'

ENV AIRFLOW_CONN_ASTRO_ORDERS_SQLITE='{\
    "conn_type": "sqlite",\
    "description": "",\
    "login": "",\
    "password": "",\
    "host": "/usr/local/airflow/include/astro_orders.db",\
    "port": null,\
    "schema": "",\
    "extra": ""\
  }'

ENV AIRFLOW__CORE__XCOM_BACKEND=astro.custom_backend.astro_custom_backend.AstroCustomXcomBackend
ENV AIRFLOW__ASTRO_SDK__XCOM_STORAGE_URL='s3://local-xcom' 
ENV AIRFLOW__ASTRO_SDK__XCOM_STORAGE_CONN_ID='aws_default'
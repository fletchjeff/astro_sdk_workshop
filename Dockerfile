FROM quay.io/astronomer/astro-runtime:6.0.3

ENV AIRFLOW__CORE__ENABLE_XCOM_PICKLING=True
# Go Data Fest
## Data Orchestration and Data Lineage with Astronomer

This repo is for the Go Data Fest workshop. This tutorial demonstrates how to write an Extract, Transform, Load (ETL) pipeline on your local machine with the Astro Python SDK. The Astro SDK is maintained by Astronomer and simplifies the pipeline authoring process with native Python functions for common data orchestration use cases.

The pipeline you build in this tutorial will:

* Extract a file into a Snowflake relational table.
* Transform that table.
* Load the transformed table into a reporting table.

The example DAG in this tutorial uses Amazon S3 and Snowflake, but you can replace these with any supported data sources and tables simply by changing connection information.

## Prerequisites
To complete this tutorial, you need:

* [Docker Desktop](https://www.docker.com/) installed.
* The [Astro CLI](https://docs.astronomer.io/astro/cli/get-started)


### Step 1: Get the repo
Clone this repo to your local machine:
```
git clone https://github.com/fletchjeff/astro_sdk_workshop
```

### Step 2: Start `astro`
Start up the local `astro` services.
```
astro dev start
```

### Step 3: Create the Postgres Connection
Create Airflow connections to the local postgres server.
* Open the Airflow UI at http://localhost:8080/
* Go to **Admin > Connections**

Create a new Postgres connection with the following values:

Connection ID: `local_postgres`
Connection type: `Postgres`
Host: `host.docker.local` [Note: If this doesn't work, use the IP address of your local machine]
Schema: *[leave this blank]*
Login: `postgres`
Password: `postgres`
Port: `5432`

### Step 4: Configure Postgres
Open the PGAdmin UI at http://localhost:5050/

Add a new server by right clicking on the Server 

### Step 5: Create the Tables
Open the PGAdmin UI at http://localhost:5050/

CREATE SCHEMA TMP_ASTRO;

SET search_path TO TMP_ASTRO;

CREATE TABLE customers_table (customer_id CHAR(10), customer_name VARCHAR(100), type VARCHAR(10) );

INSERT INTO customers_table (CUSTOMER_ID, CUSTOMER_NAME,TYPE) VALUES     ('CUST1','NAME1','TYPE1'),('CUST2','NAME2','TYPE1'),('CUST3','NAME3','TYPE2');


CREATE TABLE reporting_table (
    CUSTOMER_ID CHAR(30), CUSTOMER_NAME VARCHAR(100), ORDER_ID CHAR(10), PURCHASE_DATE VARCHAR(100), AMOUNT FLOAT, TYPE CHAR(10));

INSERT INTO reporting_table (CUSTOMER_ID, CUSTOMER_NAME, ORDER_ID, PURCHASE_DATE, AMOUNT, TYPE) VALUES
('INCORRECT_CUSTOMER_ID','INCORRECT_CUSTOMER_NAME','ORDER2','2/2/2022',200,'TYPE1'),
('CUST3','NAME3','ORDER3','3/3/2023',300,'TYPE2'),
('CUST4','NAME4','ORDER4','4/4/2022',400,'TYPE2');


Overview
========

Welcome to Astronomer! This project was generated after you ran 'astro dev init' using the Astronomer CLI. This readme describes the contents of the project, as well as how to run Apache Airflow on your local machine.

Project Contents
================

Your Astro project contains the following files and folders:

- dags: This folder contains the Python files for your Airflow DAGs. By default, this directory includes an example DAG that runs every 30 minutes and simply prints the current date. It also includes an empty 'my_custom_function' that you can fill out to execute Python code.
- Dockerfile: This file contains a versioned Astro Runtime Docker image that provides a differentiated Airflow experience. If you want to execute other commands or overrides at runtime, specify them here.
- include: This folder contains any additional files that you want to include as part of your project. It is empty by default.
- packages.txt: Install OS-level packages needed for your project by adding them to this file. It is empty by default.
- requirements.txt: Install Python packages needed for your project by adding them to this file. It is empty by default.
- plugins: Add custom or community plugins for your project to this file. It is empty by default.
- airflow_settings.yaml: Use this local-only file to specify Airflow Connections, Variables, and Pools instead of entering them in the Airflow UI as you develop DAGs in this project.

Deploy Your Project Locally
===========================

1. Start Airflow on your local machine by running 'astro dev start'.

This command will spin up 3 Docker containers on your machine, each for a different Airflow component:

- Postgres: Airflow's Metadata Database
- Webserver: The Airflow component responsible for rendering the Airflow UI
- Scheduler: The Airflow component responsible for monitoring and triggering tasks

2. Verify that all 3 Docker containers were created by running 'docker ps'.

Note: Running 'astro dev start' will start your project with the Airflow Webserver exposed at port 8080 and Postgres exposed at port 5432. If you already have either of those ports allocated, you can either stop your existing Docker containers or change the port.

3. Access the Airflow UI for your local Airflow project. To do so, go to http://localhost:8080/ and log in with 'admin' for both your Username and Password.

You should also be able to access your Postgres Database at 'localhost:5432/postgres'.

Deploy Your Project to Astronomer
=================================

If you have an Astronomer account, pushing code to a Deployment on Astronomer is simple. For deploying instructions, refer to Astronomer documentation: https://docs.astronomer.io/cloud/deploy-code/

Contact
=======

The Astronomer CLI is maintained with love by the Astronomer team. To report a bug or suggest a change, reach out to our support team: https://support.astronomer.io/
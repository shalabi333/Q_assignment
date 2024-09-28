# Use the base Airflow image
FROM apache/airflow:2.5.1-python3.9

# Install dbt using pip
RUN pip install dbt-core dbt-postgres

# Set the working directory to /opt/airflow
WORKDIR /opt/airflow

# Copy over your dags, plugins, and dbt project if necessary
COPY ./dags /opt/airflow/dags
COPY ./plugins /opt/airflow/plugins

# Ensure proper permissions for running dbt
USER airflow

# Real Estate Data Engineering Pipeline

This project implements a robust data pipeline to extract, transform, and analyze real estate data. It leverages Dockerized environments for seamless deployment, Airflow for orchestration, dbt for data transformation, PostgreSQL for data storage, and API crawling to gather real-time real estate data.

## Table of Contents

- [Project Overview](#project-overview)
- [Setup Instructions](#setup-instructions)
- [Tools Used](#tools-used)
- [Data Sources](#data-sources)
- [Project Structure](#project-structure)
- [Key Features](#key-features)
- [Contact](#contact)

## Project Overview

This project showcases a complete **data engineering pipeline** for processing real estate data. The pipeline:
- **Crawls real-time data from APIs** and aggregates it with historical data.
- **Orchestrates ETL processes using Apache Airflow**.
- **Transforms data** using **dbt** to clean and prepare it for analysis.
- **Stores data in PostgreSQL** for efficient querying.
- **Dockerized** for ease of deployment and reproducibility.

## Setup Instructions

### Prerequisites

- **Docker** (for containerized services)
- **Python 3.7+** (for Airflow and dbt)
- **PostgreSQL** (for database management)
- **Tableau** (for data visualization)

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/real-estate-data-pipeline.git](https://github.com/shalabi333/airflow_project.git
cd airflow_project
```

### 2. Set Up Docker

All services (PostgreSQL, Airflow, dbt) are run inside Docker containers.

1. **Start Docker containers** using `docker-compose`:

   ```bash
   docker-compose up --build
   ```
 
This will start the PostgreSQL database, Airflow scheduler, Airflow web server, and dbt for transformations.

### Access services:
- **Airflow UI**: Available at [http://localhost:8080](http://localhost:8080).
- **PostgreSQL**: Accessible via `localhost:5432`.
- **dbt**: Will run within the Airflow tasks inside the Docker containers.


### Part 2: Configure PostgreSQL

### 3. Configure PostgreSQL

1. Access the PostgreSQL database (from the terminal or using pgAdmin) and run the schema to set up the database tables.

 ```sql
   create table public.real_estate_ads
(
    advertisement_number      bigint not null
        primary key,
    user_number               bigint,
    creation_time             timestamp,
    last_update_time          timestamp,
    age_less_than             integer,
    number_of_apartments      integer,
    number_of_bedrooms        integer,
    floor                     integer,
    number_of_kitchens        integer,
    closed                    boolean,
    residential_or_commercial varchar(255),
    property_type             varchar(255),
    driver_room               boolean,
    duplex                    boolean,
    families_or_singles       varchar(50),
    furnished                 boolean,
    number_of_living_rooms    integer,
    maids_room                boolean,
    price_per_meter           numeric(10, 2),
    type_of_advertiser        varchar(255),
    swimming_pool             boolean,
    paid                      boolean,
    price                     numeric(15, 2),
    rental_period             varchar(255),
    number_of_rooms           integer,
    area_dimension            integer,
    street_direction          varchar(50),
    street_width              text,
    for_sale_or_rent          varchar(50),
    number_of_bathrooms       integer,
    latitude                  numeric(10, 6),
    longitude                 numeric(10, 6),
    region_name_ar            varchar(255),
    region_name_en            varchar(255),
    province_name             varchar(255),
    nearest_city_name_ar      varchar(255),
    nearest_city_name_en      varchar(255),
    district_name_ar          varchar(255),
    district_name_en          varchar(255),
    zip_code_no               varchar(10)
);
```

### Part 3: Set Up API Crawling


### 4. Set Up API Crawling

Data is extracted from real estate APIs using Python scripts. The API crawler is set up as an **Airflow DAG**.

- Modify the **API endpoint configurations** in the Airflow DAG located in `airflow/dags/crawl_real_estate.py`.
- Ensure that the API credentials (if required) are set as environment variables in your `.env` file.


### 5. Set Up dbt for Data Transformation

**dbt** is used to transform and model the data stored in PostgreSQL.

1. Install dbt dependencies inside the Docker container:

   ```bash
   docker-compose exec airflow bash
   dbt deps
   ```
   
2. Run dbt models and tests from the Airflow UI or within the container:
   ```bash
   dbt run
   ```

### Part 5: Airflow Orchestration


### 6. Airflow Orchestration

Airflow is used to orchestrate the entire ETL process:

- **DAGs** are defined in `airflow/dags/` for crawling data, transforming it using dbt, and loading it into PostgreSQL.
- Start the DAG in the Airflow UI (`http://localhost:8080`), and monitor the entire process from data extraction to transformation and loading.

## Tools Used

### Data Engineering Tools:

- **Docker**: For containerizing all services (PostgreSQL, Airflow, dbt).
- **Apache Airflow**: To orchestrate the ETL pipeline, manage scheduling, and track task dependencies.
- **dbt (Data Build Tool)**: For data transformations, cleaning, and modeling.
- **PostgreSQL**: Relational database to store and manage the processed real estate data.
- **API Crawling**: Real-time data is fetched from external APIs, using Python for data extraction.

### Python Libraries:

- **pandas**: For data manipulation.
- **requests**: For API calls to fetch real estate data.
- **SQLAlchemy**: For interfacing with PostgreSQL.
- **Airflow**: For orchestrating the pipeline.

## Data Sources

- **API Data**: Real-time real estate data is fetched using a custom API crawler.
- **Historical CSV Data**: Historical property listings are ingested from `realestate_data_2014_2016.csv`.
- **PostgreSQL**: Used for central storage of all processed data, allowing for efficient querying and visualization.


## Project Structure

```plaintext
real-estate-data-pipeline/
├── airflow/                     # Airflow DAGs and configs
│   ├── dags/
│   └── Dockerfile                # Docker config for Airflow
├── db/                          # Database schema and dbt models
│   ├── schema.sql
│   ├── dbt_project.yml           # dbt config file
├── scripts/                     # Python scripts for API crawling
│   ├── crawl_real_estate.py
├── docker-compose.yml            # Docker setup
├── requirements.txt              # Python dependencies
├── README.md                     # Project documentation (this file)
└── .env                          # Environment variables (API keys, DB config)
```

### Part 9: Key Features


## Key Features

### 1. Dockerized Setup

- All services (Airflow, PostgreSQL, dbt) are containerized using Docker, making it easy to spin up the entire pipeline in any environment.

### 2. Airflow-Orchestrated Pipeline

- **Apache Airflow** is used to orchestrate the entire ETL pipeline, managing scheduling, task dependencies, and ensuring data flows from the source API to the database.

### 3. API Data Crawling

- Python scripts are used to **crawl real-time data** from real estate APIs. The data is then stored in PostgreSQL for further analysis.

### 4. Data Transformation with dbt

- **dbt** is used to transform, clean, and model the raw data into a form suitable for analysis and visualization.

### 5. Data Storage in PostgreSQL

- All transformed data is stored in PostgreSQL, ensuring structured and queryable data for analysis and reporting.


## Contact

For any questions or contributions, feel free to reach out:

**Abdulrahman Shalabi :)**  
Email: [ashalabi0014@gmail.com](mailto:ashalabi0014@gmail.com)





import psycopg2
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from datetime import datetime, timedelta
import requests
import logging
import time

# DAG settings
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 13),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

# Create the DAG
dag = DAG(
    'crawl_data_from_api',
    default_args=default_args,
    description='DAG to crawl data using FastAPI with pagination and insert into Postgres',
    schedule_interval=timedelta(days=1),
)
# Function to crawl data from FastAPI and save to PostgreSQL
def crawl_data_from_fastapi():
    logger = logging.getLogger("airflow.task")
    data_list = []
    data_list_batch = []
    page = 1
    
    try:
        while True:
            api_url = f"https://api.dealapp.sa/production/ad?page={page}&sort=-1&sortBy=refreshed.at&city=6009d941950ada00061eeeab&district=5dd490aebc2e91004242e4df,5dd490aebc2e91004242e4e1&limit=10"
            headers = {
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI2NmU0OTkxYjBkMzU4MGM1YmEwMjRjMzEiLCJyb2xlIjoiR1VFU1QiLCJzdGF0dXMiOiJERUFDVElWQVRFRCIsImlhdCI6MTcyNjI1NzQzNX0.RfVZE5o8JPSeI1eBpNXl2cp5Q29r6fp-Lk_r929Dd9A'
            }

            logger.info(f"Fetching data from page {page}")
            response = requests.get(api_url, headers=headers)
            response_data = response.json()
            # Check for rate limit and introduce a delay if needed
            if response.status_code == 429:  # 429 is the HTTP status code for Too Many Requests
                logger.warning("Rate limit hit, waiting before next request...")
                time.sleep(20)
                continue
            # Loop through each item in the response
            for item in response_data['data']:
                filtered_item = {
                        'advertisement_number': item.get('code'),
                        'user_number': None,  
                        'creation_time': item.get('createdAt'),
                        'last_update_time': item.get('updatedAt'),
                        'age_less_than': -1 if item.get('relatedQuestions', {}).get('propertyAgeRange', '0').upper() == 'NEW' else item.get('relatedQuestions', {}).get('propertyAgeRange', '0'),
                        'number_of_apartments': 0,  # Placeholder, not present in the response
                        'number_of_bedrooms': item.get('relatedQuestions', {}).get('roomsNum', 0),
                        'floor': None,  # Placeholder, not present in the response
                        'number_of_kitchens': 0,  # Placeholder, not present in the response
                        'closed': item.get('published'),
                        'residential_or_commercial': ', '.join(item.get('relatedQuestions', {}).get('usageType', [])),
                        'property_type': item.get('propertyType', {}).get('propertyType_ar'),
                        'driver_room':item.get('relatedQuestions', {}).get('hasDriverRoom'),
                        'duplex': None,  # Placeholder, map to a related field if available
                        'families_or_singles': item.get('relatedQuestions', {}).get('accommodationType'),
                        'furnished': item.get('relatedQuestions', {}).get('isFurnished'),
                        'number_of_living_rooms':  item.get('relatedQuestions', {}).get('roomsNum', 0),
                        'maids_room': item.get('relatedQuestions', {}).get('hasMaidRoom'),
                        'price_per_meter': 0,  # Placeholder, can be calculated if price and area are available
                        'type_of_advertiser': item.get('createdBy', {}).get('agentType', 'مسوق'),
                        'swimming_pool': item.get('relatedQuestions', {}).get('hasPool'),
                        'paid': True if item.get('promotion', {}).get('status') == 'PAID' else False,
                        'price': item.get('price'),
                        'rental_period': item.get('rentType'),
                        'number_of_rooms': item.get('relatedQuestions', {}).get('roomsNum', 0),
                        'area_dimension': item.get('area'),
                        'street_direction': ', '.join(item.get('relatedQuestions', {}).get('facing', [])),
                        'street_width': item.get('relatedQuestions', {}).get('streetWidthRange'),
                        'for_sale_or_rent': item.get('purpose'),
                        'number_of_bathrooms': item.get('relatedQuestions', {}).get('toiletsNum'),
                        'latitude': item.get('location', {}).get('value', {}).get('coordinates', [None, None])[1],
                        'longitude': item.get('location', {}).get('value', {}).get('coordinates', [None, None])[0],
                        'region_name_ar': item.get('city', {}).get('name_ar'),
                        'region_name_en': item.get('city', {}).get('name_en'),
                        'province_name': None,  
                        'nearest_city_name_ar': item.get('district', {}).get('name_ar'),
                        'nearest_city_name_en': item.get('district', {}).get('name_en'),
                        'district_name_ar': item.get('district', {}).get('name_ar'),
                        'district_name_en': item.get('district', {}).get('name_en'),
                        'zip_code_no': None  # Placeholder, zip code not available in the response
                    }
                
                # Add the processed item to the data list
                data_list.append(filtered_item)
                data_list_batch.append(filtered_item)
            insert_data_into_postgres(data_list_batch)   
            data_list_batch.clear() 
            # Check if there's a next page
            if not response_data.get('hasNextPage', False):
                logger.info("No more pages to fetch.")
                break
            # Move to the next page
            page += 1

    except Exception as e:
        logger.exception(f"An error occurred: {str(e)}")
        raise

    logger.info(f"Successfully crawled {len(data_list)} items.")
    return data_list


def insert_data_into_postgres(data_list):
    conn = None
    try:
        # Connect to your PostgreSQL database
        conn = psycopg2.connect(
            host="postgres",  # Docker service name or localhost if local
            database="airflow",  # Your PostgreSQL database name
            user="airflow",  # PostgreSQL username
            password="airflow"  # PostgreSQL password
        )
        cur = conn.cursor()

        # Define the insert query with placeholders for each column
        insert_query = """
        INSERT INTO real_estate_ads (
            advertisement_number, user_number, creation_time, last_update_time, age_less_than, 
            number_of_apartments, number_of_bedrooms, floor, number_of_kitchens, closed, 
            residential_or_commercial, property_type, driver_room, duplex, families_or_singles, 
            furnished, number_of_living_rooms, maids_room, price_per_meter, type_of_advertiser, 
            swimming_pool, paid, price, rental_period, number_of_rooms, area_dimension, 
            street_direction, street_width, for_sale_or_rent, number_of_bathrooms, 
            latitude, longitude, region_name_ar, region_name_en, province_name, 
            nearest_city_name_ar, nearest_city_name_en, district_name_ar, district_name_en, 
            zip_code_no
        ) VALUES (
            %(advertisement_number)s, %(user_number)s, %(creation_time)s, %(last_update_time)s, %(age_less_than)s, 
            %(number_of_apartments)s, %(number_of_bedrooms)s, %(floor)s, %(number_of_kitchens)s, %(closed)s, 
            %(residential_or_commercial)s, %(property_type)s, %(driver_room)s, %(duplex)s, %(families_or_singles)s, 
            %(furnished)s, %(number_of_living_rooms)s, %(maids_room)s, %(price_per_meter)s, %(type_of_advertiser)s, 
            %(swimming_pool)s, %(paid)s, %(price)s, %(rental_period)s, %(number_of_rooms)s, %(area_dimension)s, 
            %(street_direction)s, %(street_width)s, %(for_sale_or_rent)s, %(number_of_bathrooms)s, 
            %(latitude)s, %(longitude)s, %(region_name_ar)s, %(region_name_en)s, %(province_name)s, 
            %(nearest_city_name_ar)s, %(nearest_city_name_en)s, %(district_name_ar)s, %(district_name_en)s, 
            %(zip_code_no)s
        )
        """

        cur.executemany(insert_query, data_list)
        conn.commit()
        cur.close()

    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"Error inserting data into PostgreSQL: {e}")

    finally:
        if conn:
            conn.close()

# Task to delete old data
delete_old_data_task = PostgresOperator(
    task_id='delete_old_data',
    postgres_conn_id='postgres_default',
    sql="DELETE FROM real_estate_ads;",
    dag=dag,
)

# Airflow task to crawl data and insert into Postgres
crawl_task = PythonOperator(
    task_id='crawl_data_task',
    python_callable=crawl_data_from_fastapi,
    op_kwargs={
        'fields': 'advertisement_number,user_number,creation_time,last_update_time,age_less_than,number_of_apartments,number_of_bedrooms,floor,number_of_kitchens,closed,residential_or_commercial,property_type,driver_room,duplex,families_or_singles,furnished,number_of_living_rooms,maids_room,price_per_meter,type_of_advertiser,swimming_pool,paid,price,rental_period,number_of_rooms,area_dimension,street_direction,street_width,for_sale_or_rent,number_of_bathrooms,latitude,longitude,region_name_ar,region_name_en,province_name,nearest_city_name_ar,nearest_city_name_en,district_name_ar,district_name_en,zip_code_no'
    },
    dag=dag,
)

# Task dependencies
delete_old_data_task >> crawl_task
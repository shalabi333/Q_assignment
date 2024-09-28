WITH csv_source AS (
    SELECT * FROM {{ ref('csv_data_realstate') }}
)

SELECT 
 "Advertisement_Number" 
,"User_Number"
,"Creation_Time "
,"Last_Update_Time" 
,"Age_Less_Than" 
,"Number_of_Appartment" 
,"Number_of_Beadrooms" 
,"Floor" 
,"Number_of_Kitchens " 
,"Closed"
,"Residential_or_Commercial"
,"Property_Type" 
,"Driver_Room" 
,"Duplex" 
,CASE WHEN 
"Families_or_Singls" = N'عوائل' THEN 'FAMILY'
WHEN "Families_or_Singls" = N'عزاب' THEN 'SINGLES'
 ELSE 'UNKNOWN' END AS "Families_or_Singls"
,"Furnished" 
,"Number_of_Living_Rooms" 
,"Maid_Room" 
,"Price_per_Meter" 
,"Type_of_Advertiser" 
,"Swimming_Pool" 
,"Paid" 
,"Price"
,"Rental_Period" 
,"Number_of_Rooms" 
,"Area_Dimension" 
,"Street_Direction" 
,"Street_Width" 
,"Fore_saleor_Rent" 
,"Number_of_Bathrooms" 
,"Latitude" 
,"Longitude" 
,"region_name_ar" 
,"region_name_en" 
,"province_name" 
,"nearest_city_name_ar" 
,"nearest_city_name_en" 
,"district_name_ar" 
,"district_name_en" 
FROM csv_source

-- /Users/shalabi/Desktop/airflow_project/dbt/dbt_project.yml.


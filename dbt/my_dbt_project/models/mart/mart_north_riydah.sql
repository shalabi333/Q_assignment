{{ config(
    materialized='incremental',
    schema='mart'
) }}
WITH north_riyadh AS (SELECT

        CAST("Advertisement_Number" AS BIGINT) AS "Advertisement_Number",  -- Use BIGINT if purely numeric
        CAST("Creation_Time " AS TIMESTAMP) AS "Creation_Time",  -- Changed to TIMESTAMP
        CAST("Last_Update_Time" AS TIMESTAMP) AS "Last_Update_Time",  -- Changed to TIMESTAMP
        CAST("Age_Less_Than" AS INT) AS "Age_Less_Than",  -- Changed to INT
        CAST("Number_of_Beadrooms" AS INT) AS "Number_of_Beadrooms",  -- Changed to INT
        CAST("Closed" AS VARCHAR) AS "Closed",  -- Changed to BOOLEAN
        CAST("Residential_or_Commercial" AS VARCHAR) AS "Residential_or_Commercial",  -- Categorical, keep as VARCHAR
        CAST("Property_Type" AS VARCHAR) AS "Property_Type",  -- Categorical, keep as VARCHAR
        CAST("Families_or_Singls" AS VARCHAR) AS "Families_or_Singls",  -- Categorical, keep as VARCHAR
        CAST("Price_per_Meter" AS NUMERIC) AS "Price_per_Meter",  -- Changed to NUMERIC for price
        CAST("Price" AS NUMERIC) AS "Price",  -- Changed to NUMERIC for price
        CAST("Rental_Period" AS VARCHAR) AS "Rental_Period",  -- Categorical, keep as VARCHAR
        CAST("Fore_saleor_Rent" AS VARCHAR) AS "For_sale_or_Rent",  -- Categorical, keep as VARCHAR
        CAST("Area_Dimension" AS NUMERIC) AS "Area_Dimension",  -- Changed to NUMERIC for dimensions
        CAST(district_name_ar AS VARCHAR) AS district_name_ar,  -- Categorical, keep as VARCHAR

    'csv_sheet' AS source_flag
FROM {{ref('src_csv')}}

WHERE district_name_ar IN(N'الياسمين',N'الملقا')
UNION ALL
SELECT
        CAST("Advertisement_Number" AS BIGINT) AS "Advertisement_Number",  -- Use BIGINT if purely numeric
        CAST("Creation_Time " AS TIMESTAMP) AS "Creation_Time",  -- Changed to TIMESTAMP
        CAST("Last_Update_Time" AS TIMESTAMP) AS "Last_Update_Time",  -- Changed to TIMESTAMP
        CAST("Age_Less_Than" AS INT) AS "Age_Less_Than",  -- Changed to INT
        CAST("Number_of_Beadrooms" AS INT) AS "Number_of_Beadrooms",  -- Changed to INT
        CAST("Closed" AS VARCHAR) AS "Closed",  -- Changed to BOOLEAN
        CAST("Residential_or_Commercial" AS VARCHAR) AS "Residential_or_Commercial",  -- Categorical, keep as VARCHAR
        CAST("Property_Type" AS VARCHAR) AS "Property_Type",  -- Categorical, keep as VARCHAR
        CAST("Families_or_Singls" AS VARCHAR) AS "Families_or_Singls",  -- Categorical, keep as VARCHAR
        CAST("Price_per_Meter" AS NUMERIC) AS "Price_per_Meter",  -- Changed to NUMERIC for price
        CAST("Price" AS NUMERIC) AS "Price",  -- Changed to NUMERIC for price
        CAST("Rental_Period" AS VARCHAR) AS "Rental_Period",  -- Categorical, keep as VARCHAR
        CAST("For_sale_or_Rent" AS VARCHAR) AS "For_sale_or_Rent",  -- Categorical, keep as VARCHAR
        CAST("Area_Dimension" AS NUMERIC) AS "Area_Dimension",  -- Changed to NUMERIC for dimensions
        CAST(district_name_ar AS VARCHAR) AS district_name_ar,  -- Categorical, keep as VARCHAR
       
    'real_estate_API' AS source_flag
FROM {{ref('src_real_estate_ads')}}

WHERE district_name_ar IN(N'الياسمين',N'الملقا')
)

SELECT 

  row_number() over() as id
,*,

CASE WHEN 

 FROM north_riyadh
WHERE  "Families_or_Singls" IS NOT NULL
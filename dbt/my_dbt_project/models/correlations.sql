SELECT
    CORR("Price", "Number_of_Beadrooms") AS correlation_bedrooms_rent,
    CORR("Price", "Area_Dimension") AS correlation_area_rent,
    CORR("Price", "Number_of_Beadrooms") AS correlation_bedrooms_sale,
    CORR("Price", "Area_Dimension") AS correlation_area_sale
FROM {{ref('mart_north_riydah')}}
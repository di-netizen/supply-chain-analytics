-- =========================================
-- 1. TOTAL SHIPMENTS
-- =========================================
SELECT COUNT(*) AS total_shipments
FROM shipments;


-- =========================================
-- 2. DELIVERY STATUS DISTRIBUTION
-- =========================================
SELECT 
    delivery_status,
    COUNT(*) AS total
FROM shipments
GROUP BY delivery_status;


-- =========================================
-- 3. AVERAGE DELIVERY TIME
-- =========================================
SELECT 
    ROUND(AVG(delivery_time_days), 2) AS avg_delivery_time
FROM shipments;


-- =========================================
-- 4. DELAY % BY DESTINATION (IMPORTANT KPI)
-- =========================================
SELECT 
    destination,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN delivery_status = 'Delayed' THEN 1 ELSE 0 END) AS delayed_orders,
    ROUND(
        100.0 * SUM(CASE WHEN delivery_status = 'Delayed' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS delay_percentage
FROM shipments
GROUP BY destination
ORDER BY delay_percentage DESC;


-- =========================================
-- 5. COST ANALYSIS (ROUTE LEVEL)
-- =========================================
SELECT 
    origin,
    destination,
    ROUND(AVG(transport_cost), 2) AS avg_cost,
    ROUND(AVG(distance_km), 2) AS avg_distance,
    ROUND(AVG(transport_cost / distance_km), 2) AS cost_per_km
FROM shipments
GROUP BY origin, destination
ORDER BY cost_per_km DESC;


-- =========================================
-- 6. DISTANCE VS DELIVERY TIME
-- =========================================
SELECT 
    (distance_km / 100) * 100 AS distance_bucket,
    ROUND(AVG(delivery_time_days), 2) AS avg_delivery_time
FROM shipments
GROUP BY distance_bucket
ORDER BY distance_bucket;


-- =========================================
-- 7. WORST ROUTES BY DELAYS (WINDOW FUNCTION)
-- =========================================
SELECT 
    origin,
    destination,
    COUNT(*) AS total_shipments,
    SUM(CASE WHEN delivery_status = 'Delayed' THEN 1 ELSE 0 END) AS delays,
    RANK() OVER (
        ORDER BY SUM(CASE WHEN delivery_status = 'Delayed' THEN 1 ELSE 0 END) DESC
    ) AS delay_rank
FROM shipments
GROUP BY origin, destination;


-- =========================================
-- 8. KPI SUMMARY TABLE
-- =========================================
SELECT 
    COUNT(*) AS total_shipments,
    
    SUM(CASE WHEN delivery_status = 'Delayed' THEN 1 ELSE 0 END) AS total_delays,
    
    ROUND(
        100.0 * SUM(CASE WHEN delivery_status = 'Delayed' THEN 1 ELSE 0 END) / COUNT(*),
        2
    ) AS delay_rate,
    
    ROUND(AVG(delivery_time_days), 2) AS avg_delivery_time,
    
    ROUND(AVG(transport_cost), 2) AS avg_cost
    
FROM shipments;


-- =========================================
-- 9. VEHICLE PERFORMANCE ANALYSIS
-- =========================================
SELECT 
    vehicle_type,
    COUNT(*) AS total_shipments,
    ROUND(AVG(delivery_time_days), 2) AS avg_delivery_time,
    ROUND(AVG(transport_cost), 2) AS avg_cost
FROM shipments
GROUP BY vehicle_type
ORDER BY avg_delivery_time DESC;


-- =========================================
-- 10. TOP 5 MOST EXPENSIVE ROUTES
-- =========================================
SELECT 
    origin,
    destination,
    ROUND(AVG(transport_cost), 2) AS avg_cost
FROM shipments
GROUP BY origin, destination
ORDER BY avg_cost DESC
LIMIT 5;
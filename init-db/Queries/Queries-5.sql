SELECT 
    TO_CHAR(admission_date, 'Month') AS admission_month,
    TO_CHAR(admission_date, 'Day') AS day_of_week,
    COUNT(*) AS num_of_admissions
FROM ADMISSION
GROUP BY admission_month, day_of_week, EXTRACT(MONTH FROM admission_date), EXTRACT(DOW FROM admission_date)
ORDER BY EXTRACT(MONTH FROM admission_date), EXTRACT(DOW FROM admission_date);
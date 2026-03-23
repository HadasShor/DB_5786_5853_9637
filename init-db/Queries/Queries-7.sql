SELECT 
    gender, 
    AVG(EXTRACT(YEAR FROM AGE(date_of_birth))) AS avg_age,
    COUNT(*) AS total_patients
FROM PATIENT
GROUP BY gender
HAVING COUNT(*) > 1;
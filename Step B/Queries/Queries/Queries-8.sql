SELECT 
    p.first_name, 
    p.last_name, 
    EXTRACT(YEAR FROM p.date_of_birth) AS birth_year,
    COUNT(pa.allergy_id) AS num_of_allergies
FROM PATIENT p
JOIN PATIENT_ALLERGY pa ON p.patient_id = pa.patient_id
WHERE p.patient_id IN (
    SELECT patient_id 
    FROM PATIENT 
    WHERE EXTRACT(YEAR FROM date_of_birth) < 2000
)
GROUP BY p.first_name, p.last_name, p.date_of_birth
ORDER BY p.last_name ASC;
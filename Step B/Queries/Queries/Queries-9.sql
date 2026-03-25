UPDATE PATIENT_INSURANCE 
SET coverage_type = 'Chronic Care'
WHERE EXTRACT(YEAR FROM expiration_date) >= 2024
AND patient_id IN (
    SELECT patient_id 
    FROM PATIENT_MEDICAL_HISTORY 
    GROUP BY patient_id 
    HAVING COUNT(*) >= 1 
);
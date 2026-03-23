UPDATE PATIENT_INSURANCE 
SET coverage_type = 'Chronic Care'
WHERE patient_id IN (
    SELECT patient_id 
    FROM PATIENT_MEDICAL_HISTORY 
    GROUP BY patient_id 
    HAVING COUNT(*) >= 1 
);
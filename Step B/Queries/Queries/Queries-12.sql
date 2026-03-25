DELETE FROM EMERGENCY_CONTACT ec
WHERE NOT EXISTS (
    SELECT 1 
    FROM ADMISSION a 
    WHERE a.patient_id = ec.patient_id
    AND EXTRACT(YEAR FROM a.admission_date) = 2024
);
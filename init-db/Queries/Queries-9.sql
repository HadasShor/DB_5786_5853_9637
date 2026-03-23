

UPDATE PATIENT_INSURANCE
SET provider_name = 'Senior Care'
WHERE patient_id IN (
    SELECT patient_id 
    FROM PATIENT 
    WHERE EXTRACT(YEAR FROM AGE(date_of_birth)) > 70
);
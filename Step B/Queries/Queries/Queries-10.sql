UPDATE PATIENT_INSURANCE
SET expiration_date = expiration_date + 365
WHERE patient_id IN (
    SELECT patient_id FROM PATIENT 
    WHERE EXTRACT(DAY FROM date_of_birth) = 1
    GROUP BY patient_id
);
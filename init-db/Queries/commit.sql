UPDATE ADMISSION 
SET admission_type = 'Urgent'
WHERE admission_type = 'Elective'
AND patient_id IN (
    SELECT patient_id 
    FROM PATIENT_MEDICAL_HISTORY 
    WHERE condition LIKE '%Heart%'
);
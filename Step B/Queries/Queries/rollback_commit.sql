UPDATE ADMISSION 
SET admission_type = 'Urgent'
WHERE admission_type = 'Elective'
AND patient_id IN (
    SELECT pmh.patient_id 
    FROM PATIENT_MEDICAL_HISTORY pmh
    WHERE pmh.condition LIKE '%Heart%' 
       OR pmh.condition LIKE '%Diabetes%'
);




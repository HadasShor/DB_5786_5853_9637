UPDATE ADMISSION 
SET reason = 'Senior Emergency Care' 
WHERE admission_id IN (
    SELECT a.admission_id 
    FROM ADMISSION a
    JOIN PATIENT p ON a.patient_id = p.patient_id
    WHERE a.admission_type = 'Emergency' 
      AND a.admission_date < CURRENT_DATE - INTERVAL '1 month'
      AND EXTRACT(YEAR FROM AGE(p.date_of_birth)) > 60
);
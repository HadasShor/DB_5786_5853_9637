DELETE FROM PATIENT_MEDICAL_HISTORY 
WHERE patient_id IN (
    SELECT p.patient_id 
    FROM PATIENT p
    LEFT JOIN ADMISSION a ON p.patient_id = a.patient_id
    WHERE p.date_of_birth > '2000-01-01'
    GROUP BY p.patient_id
    HAVING COUNT(a.admission_id) = 0
);
SELECT DISTINCT p.first_name, p.last_name, p.email
FROM PATIENT p
JOIN ADMISSION a ON p.patient_id = a.patient_id
WHERE EXTRACT(YEAR FROM a.admission_date) = 2024
ORDER BY last_name;

SELECT first_name, last_name, email
FROM PATIENT
WHERE patient_id IN (
    SELECT patient_id FROM ADMISSION 
    WHERE EXTRACT(YEAR FROM admission_date) = 2024
)
ORDER BY last_name;
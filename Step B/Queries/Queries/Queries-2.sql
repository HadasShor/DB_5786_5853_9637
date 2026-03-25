SELECT EXTRACT(YEAR FROM a.admission_date) as year_part, COUNT(a.admission_id) as total_admissions
FROM ADMISSION a
JOIN PATIENT_ALLERGY pa ON a.patient_id = pa.patient_id
WHERE pa.severity = 'Severe'
GROUP BY EXTRACT(YEAR FROM a.admission_date)
ORDER BY year_part DESC;



SELECT EXTRACT(YEAR FROM admission_date) as year_part, COUNT(*) as total_admissions
FROM ADMISSION
WHERE patient_id IN (
    SELECT patient_id FROM PATIENT_ALLERGY WHERE severity = 'Severe'
)
GROUP BY EXTRACT(YEAR FROM admission_date)
ORDER BY year_part DESC;
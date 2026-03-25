

SELECT EXTRACT(YEAR FROM a.admission_date) as year_part, COUNT(*) as total_admissions
FROM ADMISSION a
WHERE EXISTS (SELECT 1 FROM PATIENT_ALLERGY pa WHERE pa.patient_id = a.patient_id AND pa.severity = 'Severe')
GROUP BY EXTRACT(YEAR FROM a.admission_date)
ORDER BY year_part DESC;



SELECT EXTRACT(YEAR FROM admission_date) as year_part, COUNT(*) as total_admissions
FROM ADMISSION
WHERE patient_id IN (SELECT patient_id FROM PATIENT_ALLERGY WHERE severity = 'Severe')
GROUP BY EXTRACT(YEAR FROM admission_date)
ORDER BY year_part DESC;
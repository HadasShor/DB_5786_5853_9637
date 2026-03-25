SELECT 
    p.first_name || ' ' || p.last_name AS full_name,
    pmh.condition,
    EXTRACT(YEAR FROM pmh.diagnosis_date) AS diagnosis_year,
    EXTRACT(MONTH FROM pmh.diagnosis_date) AS diagnosis_month,
    (SELECT COUNT(*) FROM ADMISSION a WHERE a.patient_id = p.patient_id) AS total_admissions
FROM PATIENT p
JOIN PATIENT_MEDICAL_HISTORY pmh ON p.patient_id = pmh.patient_id
WHERE pmh.condition LIKE '%Chronic%'
  AND p.patient_id IN (SELECT patient_id FROM ADMISSION)
GROUP BY p.first_name, p.last_name, pmh.condition, pmh.diagnosis_date, p.patient_id
ORDER BY total_admissions DESC, diagnosis_year ASC;
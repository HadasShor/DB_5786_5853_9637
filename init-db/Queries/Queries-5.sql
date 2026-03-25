SELECT p.first_name, p.last_name, COUNT(a.admission_id) as num_admissions
FROM PATIENT p
JOIN ADMISSION a ON p.patient_id = a.patient_id
GROUP BY p.patient_id, p.first_name, p.last_name
HAVING COUNT(a.admission_id) > (SELECT AVG(cnt) FROM (SELECT COUNT(*) as cnt FROM ADMISSION GROUP BY patient_id));
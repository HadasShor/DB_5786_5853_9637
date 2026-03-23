-- צורה א': שימוש ב-EXTRACT (פירוק תאריך לחודש)
SELECT p.first_name, p.last_name, a.admission_date, a.reason
FROM ADMISSION a
JOIN PATIENT p ON a.patient_id = p.patient_id
WHERE EXTRACT(MONTH FROM a.admission_date) = 1;

-- צורה ב': שימוש ב-BETWEEN (טווח תאריכים)
SELECT p.first_name, p.last_name, a.admission_date, a.reason
FROM ADMISSION a
JOIN PATIENT p ON a.patient_id = p.patient_id
WHERE a.admission_date BETWEEN '2024-01-01' AND '2024-01-31';
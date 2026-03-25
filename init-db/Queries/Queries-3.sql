SELECT p.first_name, p.last_name, p.phone
FROM PATIENT p
WHERE p.patient_id IN (
    SELECT pa.patient_id 
    FROM PATIENT_ALLERGY pa 
    WHERE pa.severity = 'Severe'
) AND EXTRACT(YEAR FROM p.date_of_birth) < 1965;



-- שימוש ב-JOIN ו-GROUP BY
SELECT p.first_name, p.last_name, p.phone, 
       EXTRACT(YEAR FROM p.date_of_birth) as birth_year,
       COUNT(pa.allergy_id) as total_severe_allergies
FROM PATIENT p
JOIN PATIENT_ALLERGY pa ON p.patient_id = pa.patient_id
WHERE p.date_of_birth < TO_DATE('1965-01-01', 'YYYY-MM-DD')
  AND pa.severity = 'Severe'
GROUP BY p.patient_id, p.first_name, p.last_name, p.phone, p.date_of_birth
ORDER BY birth_year ASC;
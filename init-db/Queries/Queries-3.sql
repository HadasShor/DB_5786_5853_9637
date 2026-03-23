-- צורה א': שימוש ב-JOIN 
SELECT DISTINCT p.first_name, p.last_name, p.phone
FROM PATIENT p 
JOIN PATIENT_ALLERGY pa ON p.patient_id = pa.patient_id 
WHERE pa.severity = 'Severe'
ORDER BY p.last_name;

-- צורה ב': שימוש ב-ANY
SELECT p.first_name, p.last_name, p.phone 
FROM PATIENT p 
WHERE p.patient_id = ANY (
    SELECT patient_id 
    FROM PATIENT_ALLERGY 
    WHERE severity = 'Severe'
)
ORDER BY p.last_name;
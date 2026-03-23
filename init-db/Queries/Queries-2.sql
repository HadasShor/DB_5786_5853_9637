-- צורה א': שימוש ב-NOT IN
SELECT first_name, last_name, phone 
FROM PATIENT 
WHERE patient_id NOT IN (SELECT patient_id FROM PATIENT_INSURANCE WHERE expiration_date > CURRENT_DATE);

-- צורה ב': שימוש ב-LEFT JOIN (יעיל יותר לזיהוי חוסרים)
SELECT p.first_name, p.last_name, p.phone 
FROM PATIENT p 
LEFT JOIN PATIENT_INSURANCE pi ON p.patient_id = pi.patient_id AND pi.expiration_date > CURRENT_DATE 
WHERE pi.patient_id IS NULL;
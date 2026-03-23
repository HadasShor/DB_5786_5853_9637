-- צורה א': שימוש ב-IN
SELECT first_name, last_name, email, phone 
FROM PATIENT 
WHERE patient_id IN (SELECT patient_id FROM PATIENT_ALLERGY WHERE allergy_name = 'Gabapentin');

-- צורה ב': שימוש ב-EXISTS
SELECT p.first_name, p.last_name, p.email, p.phone 
FROM PATIENT p 
WHERE EXISTS (SELECT 1 FROM PATIENT_ALLERGY pa WHERE pa.patient_id = p.patient_id AND pa.allergy_name = 'Gabapentin');
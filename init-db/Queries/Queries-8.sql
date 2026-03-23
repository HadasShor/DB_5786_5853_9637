SELECT 
    p.first_name || ' ' || p.last_name AS patient_name,
    a.reason,
    a.admission_date,
    ec.name AS emergency_contact,
    ec.phone AS emergency_phone
FROM PATIENT p
JOIN ADMISSION a ON p.patient_id = a.patient_id
JOIN EMERGENCY_CONTACT ec ON p.patient_id = ec.patient_id
WHERE a.discharge_date IS NULL;
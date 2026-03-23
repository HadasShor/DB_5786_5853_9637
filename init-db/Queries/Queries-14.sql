DELETE FROM PATIENT_ALLERGY 
WHERE severity IN ('Mild', 'Unknown')
AND patient_id IN (
    -- תת-שאילתה: מוצאת מטופלים מבוגרים שיש להם לפחות 2 אלרגיות
    SELECT pa.patient_id 
    FROM PATIENT_ALLERGY pa
    JOIN PATIENT p ON pa.patient_id = p.patient_id
    WHERE EXTRACT(YEAR FROM p.date_of_birth) < 1990
    GROUP BY pa.patient_id
    HAVING COUNT(pa.allergy_name) >= 2
);
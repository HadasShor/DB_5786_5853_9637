UPDATE PATIENT_ALLERGY
SET notes = 'Post-Hospitalization Allergy Validation'
WHERE patient_id IN (
    -- תת שאילתה: מוצאת מטופלים שהתאשפזו בחודש ינואר
    SELECT patient_id 
    FROM ADMISSION 
    WHERE EXTRACT(MONTH FROM admission_date) = 1
    GROUP BY patient_id
    HAVING COUNT(*) >= 1
);
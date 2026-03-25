DELETE FROM EMERGENCY_CONTACT
WHERE relationship = 'Friend'
  AND patient_id IN (
      -- תת שאילתה מקוננת: מוצאת מזהי מטופלים שנולדו לפני שנת 2000
      SELECT patient_id 
      FROM PATIENT 
      WHERE EXTRACT(YEAR FROM date_of_birth) < 2000
      GROUP BY patient_id
  );
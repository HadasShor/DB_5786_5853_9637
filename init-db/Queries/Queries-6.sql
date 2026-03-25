SELECT p.first_name, p.last_name, p.phone, count_table.total_visits
FROM PATIENT p
JOIN (
    SELECT patient_id, COUNT(*) AS total_visits
    FROM ADMISSION
    GROUP BY patient_id
    HAVING COUNT(*) > 3
) AS count_table ON p.patient_id = count_table.patient_id
ORDER BY count_table.total_visits DESC;



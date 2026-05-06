CREATE OR REPLACE VIEW public.patient_admission_summary AS
SELECT 
    p.patient_id, 
    p.first_name || ' ' || p.last_name AS patient_full_name, 
    a.admission_date, 
    a.admission_type, 
    a.reason
FROM public.patient p
JOIN public.admission a ON p.patient_id = a.patient_id;




SELECT * FROM public.patient_admission_summary;


SELECT 
    admission_type, 
    COUNT(*) AS total_admissions
FROM public.patient_admission_summary
GROUP BY admission_type
ORDER BY total_admissions DESC;
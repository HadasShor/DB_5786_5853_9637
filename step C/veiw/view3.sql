CREATE OR REPLACE VIEW public.integrated_patient_staff_view AS
SELECT 
    p.patient_id, 
    p.first_name || ' ' || p.last_name AS patient_name,
    d.doctor_id AS partner_doc_id,
    d.specialization AS partner_specialization,
    m.integration_notes
FROM partner_data.staff_integration_map m
JOIN public."patient" p ON m.my_staff_id = p.patient_id 
JOIN partner_data.doctor d ON m.partner_staff_id = d.doctor_id;



SELECT patient_name, integration_notes 
FROM public.integrated_patient_staff_view 
WHERE partner_specialization = 'Cardiology';

SELECT partner_doc_id, COUNT(patient_id) AS total_patients
FROM public.integrated_patient_staff_view
GROUP BY partner_doc_id;
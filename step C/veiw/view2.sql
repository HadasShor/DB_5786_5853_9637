CREATE OR REPLACE VIEW public.partner_clinic_view AS
SELECT 
    d.doctor_id, 
    d.specialization,
    dep.department_name,
    dep.location
FROM partner_data.doctor d
JOIN partner_data.department dep ON d.staff_id = dep.department_id;



SELECT doctor_id, department_name 
FROM public.partner_clinic_view 
WHERE specialization = 'Cardiology';


SELECT location, COUNT(doctor_id) AS total_doctors
FROM public.partner_clinic_view
GROUP BY location;
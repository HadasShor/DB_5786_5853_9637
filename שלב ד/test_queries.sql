-- שאילתות בדיקה לצילומי מסך בדו"ח שלב ד'
-- הריצי כל בלוק בנפרד ב-pgAdmin

-- === בדיקת טריגר 1: תאריך אשפוז עתידי (צפויה שגיאה) ===
-- INSERT INTO public.admission (admission_id, admission_date, admission_type, reason, patient_id)
-- VALUES (99999001, CURRENT_DATE + 30, 'Elective', 'Test future date', 7380);

-- === בדיקת טריגר 1: אשפוז חירום ללא סיבה (צפויה שגיאה) ===
-- INSERT INTO public.admission (admission_id, admission_date, admission_type, reason, patient_id)
-- VALUES (99999002, CURRENT_DATE, 'Emergency', '', 7380);

-- === בדיקת טריגר 2: לפני עדכון חומרה ===
SELECT allergy_id, patient_id, allergy_name, severity, notes
FROM public.patient_allergy
WHERE severity <> 'Severe'
LIMIT 5;

-- === בדיקת טריגר 2: עדכון חומרה ל-Severe ===
-- UPDATE public.patient_allergy
-- SET severity = 'Severe'
-- WHERE allergy_id = <allergy_id מהשאילתה למעלה>;

-- === בדיקת טריגר 2: אחרי עדכון ===
-- SELECT allergy_id, severity, notes FROM public.patient_allergy WHERE allergy_id = <allergy_id>;
-- SELECT * FROM public.patient_medical_history WHERE condition = 'Allergy Severity Alert' ORDER BY history_id DESC LIMIT 3;

-- === בדיקת פונקציה 1: Ref Cursor ===
BEGIN;
SELECT public.fn_patient_admissions_refcursor(
  (SELECT patient_id FROM public.admission LIMIT 1)
);
FETCH ALL IN "<unnamed portal 1>";
COMMIT;

-- === בדיקת פונקציה 1: חריגה על מטופל לא קיים ===
-- SELECT public.fn_patient_admissions_refcursor(99999999);

-- === בדיקת פונקציה 2: ציון סיכון ===
SELECT public.fn_patient_risk_score(
  (SELECT patient_id FROM public.patient_allergy WHERE severity = 'Severe' LIMIT 1)
) AS risk_score;

-- === בדיקת פרוצדורה 1: אשפוזים פתוחים ישנים (לפני) ===
SELECT admission_id, patient_id, admission_date, discharge_date
FROM public.admission
WHERE discharge_date IS NULL
  AND admission_date < (CURRENT_DATE - 60)
ORDER BY admission_date;

-- === בדיקת פרוצדורה 2: מיפוי אינטגרציה (לפני) ===
SELECT m.my_staff_id, m.partner_staff_id, m.integration_notes, d.specialization
FROM public.staff_integration_map m
JOIN partner_data.doctor d ON d.doctor_id = m.partner_staff_id
WHERE d.specialization = 'Cardiology';

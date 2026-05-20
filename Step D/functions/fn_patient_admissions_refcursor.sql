CREATE OR REPLACE FUNCTION public.fn_patient_admissions_refcursor(p_patient_id numeric)
RETURNS refcursor
LANGUAGE plpgsql
AS $$
DECLARE
  c refcursor;
  v_exists boolean;
BEGIN
  SELECT EXISTS (
    SELECT 1
    FROM public.patient p
    WHERE p.patient_id = p_patient_id
  ) INTO v_exists;

  IF NOT v_exists THEN
    RAISE EXCEPTION 'Patient % does not exist', p_patient_id
      USING ERRCODE = 'P0001';
  END IF;

  OPEN c FOR
    SELECT
      a.admission_id,
      a.admission_date,
      a.discharge_date,
      a.admission_type,
      a.reason,
      a.patient_id
    FROM public.admission a
    WHERE a.patient_id = p_patient_id
    ORDER BY a.admission_date DESC, a.admission_id DESC;

  RETURN c;
END;
$$;


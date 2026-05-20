CREATE OR REPLACE FUNCTION public.fn_patient_risk_score(p_patient_id numeric)
RETURNS integer
LANGUAGE plpgsql
AS $$
DECLARE
  score integer := 0;
  severe_allergies_count integer := 0;
  has_open_admission boolean := false;
  rec record;
BEGIN
  IF NOT EXISTS (SELECT 1 FROM public.patient p WHERE p.patient_id = p_patient_id) THEN
    RAISE EXCEPTION 'Patient % does not exist', p_patient_id
      USING ERRCODE = 'P0001';
  END IF;

  SELECT COUNT(*)
  INTO severe_allergies_count
  FROM public.patient_allergy pa
  WHERE pa.patient_id = p_patient_id
    AND pa.severity = 'Severe';

  score := score + (severe_allergies_count * 10);

  SELECT EXISTS (
    SELECT 1
    FROM public.admission a
    WHERE a.patient_id = p_patient_id
      AND a.discharge_date IS NULL
  )
  INTO has_open_admission;

  IF has_open_admission THEN
    score := score + 15;
  END IF;

  FOR rec IN
    SELECT pmh.condition
    FROM public.patient_medical_history pmh
    WHERE pmh.patient_id = p_patient_id
  LOOP
    IF rec.condition ILIKE '%chronic%' THEN
      score := score + 20;
      EXIT;
    END IF;
  END LOOP;

  RETURN score;
EXCEPTION
  WHEN others THEN
    RAISE;
END;
$$;


-- תוכנית ראשית ב': חישוב ציון סיכון + סנכרון הערות אינטגרציה
DO $$
DECLARE
  p_id numeric;
  v_score integer;
BEGIN
  SELECT pa.patient_id
  INTO p_id
  FROM public.patient_allergy pa
  JOIN public.patient p ON p.patient_id = pa.patient_id
  WHERE pa.severity = 'Severe'
  LIMIT 1;

  IF p_id IS NULL THEN
    SELECT patient_id INTO p_id FROM public.patient LIMIT 1;
  END IF;

  IF p_id IS NULL THEN
    RAISE EXCEPTION 'No patients found in database';
  END IF;

  RAISE NOTICE '=== Main Program B: patient_id=% ===', p_id;

  v_score := public.fn_patient_risk_score(p_id);
  RAISE NOTICE 'Risk score for patient_id=% is %', p_id, v_score;

  BEGIN
    CALL public.sp_update_integration_notes_for_specialization('Cardiology');
  EXCEPTION
    WHEN others THEN
      RAISE NOTICE 'sp_update_integration_notes_for_specialization: % (SQLSTATE=%)', SQLERRM, SQLSTATE;
  END;
END;
$$;

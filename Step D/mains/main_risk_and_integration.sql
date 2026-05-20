DO $$
DECLARE
  p_id numeric := 42001;
  v_score integer;
BEGIN
  v_score := public.fn_patient_risk_score(p_id);
  RAISE NOTICE 'Risk score for patient_id=% is %', p_id, v_score;

  CALL public.sp_update_integration_notes_for_specialization('Cardiology');
END;
$$;


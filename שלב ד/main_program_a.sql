-- תוכנית ראשית א': Ref Cursor + סגירת אשפוזים ישנים
DO $$
DECLARE
  p_id numeric;
  c refcursor;
  r record;
BEGIN
  SELECT a.patient_id
  INTO p_id
  FROM public.admission a
  JOIN public.patient p ON p.patient_id = a.patient_id
  ORDER BY a.admission_date DESC
  LIMIT 1;

  IF p_id IS NULL THEN
    RAISE EXCEPTION 'No patients with admissions found in database';
  END IF;

  RAISE NOTICE '=== Main Program A: patient_id=% ===', p_id;

  c := public.fn_patient_admissions_refcursor(p_id);

  LOOP
    FETCH c INTO r;
    EXIT WHEN NOT FOUND;
    RAISE NOTICE 'admission_id=% admission_date=% discharge_date=% type=% reason=% patient_id=%',
      r.admission_id, r.admission_date, r.discharge_date, r.admission_type, r.reason, r.patient_id;
  END LOOP;
  CLOSE c;

  BEGIN
    CALL public.sp_close_long_open_admissions(60);
  EXCEPTION
    WHEN others THEN
      RAISE NOTICE 'sp_close_long_open_admissions: % (SQLSTATE=%)', SQLERRM, SQLSTATE;
  END;
END;
$$;

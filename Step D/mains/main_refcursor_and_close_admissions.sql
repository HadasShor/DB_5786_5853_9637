DO $$
DECLARE
  p_id numeric := 42001;
  c refcursor;
  r record;
BEGIN
  c := public.fn_patient_admissions_refcursor(p_id);

  LOOP
    FETCH c INTO r;
    EXIT WHEN NOT FOUND;
    RAISE NOTICE 'admission_id=% admission_date=% discharge_date=% type=% reason=% patient_id=%',
      r.admission_id, r.admission_date, r.discharge_date, r.admission_type, r.reason, r.patient_id;
  END LOOP;
  CLOSE c;

  CALL public.sp_close_long_open_admissions(60);
END;
$$;


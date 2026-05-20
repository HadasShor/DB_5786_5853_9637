CREATE OR REPLACE PROCEDURE public.sp_close_long_open_admissions(p_days integer)
LANGUAGE plpgsql
AS $$
DECLARE
  cur_adm CURSOR FOR
    SELECT a.admission_id, a.patient_id, a.admission_date
    FROM public.admission a
    WHERE a.discharge_date IS NULL
      AND a.admission_date < (CURRENT_DATE - p_days)
    ORDER BY a.admission_date ASC, a.admission_id ASC;

  v_row record;
  v_closed_count integer := 0;
BEGIN
  IF p_days IS NULL OR p_days < 0 THEN
    RAISE EXCEPTION 'p_days must be a non-negative integer, got %', p_days
      USING ERRCODE = '22023';
  END IF;

  OPEN cur_adm;
  LOOP
    FETCH cur_adm INTO v_row;
    EXIT WHEN NOT FOUND;

    BEGIN
      UPDATE public.admission a
      SET discharge_date = CURRENT_DATE
      WHERE a.admission_id = v_row.admission_id
        AND a.discharge_date IS NULL;

      UPDATE public.patient_allergy pa
      SET notes = COALESCE(pa.notes, '') ||
                  CASE WHEN pa.notes IS NULL OR pa.notes = '' THEN '' ELSE ' | ' END ||
                  'Auto-note: admission closed by procedure on ' || CURRENT_DATE::text
      WHERE pa.patient_id = v_row.patient_id
        AND pa.severity = 'Severe';

      v_closed_count := v_closed_count + 1;
    EXCEPTION
      WHEN others THEN
        RAISE NOTICE 'Failed to close admission_id=% for patient_id=%: %',
          v_row.admission_id, v_row.patient_id, SQLERRM;
    END;
  END LOOP;
  CLOSE cur_adm;

  IF v_closed_count = 0 THEN
    RAISE EXCEPTION 'No open admissions older than % days were found', p_days
      USING ERRCODE = 'P0001';
  END IF;
END;
$$;


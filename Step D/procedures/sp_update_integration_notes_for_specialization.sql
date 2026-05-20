CREATE OR REPLACE PROCEDURE public.sp_update_integration_notes_for_specialization(p_specialization text)
LANGUAGE plpgsql
AS $$
DECLARE
  rec record;
  v_updated_count integer := 0;
BEGIN
  IF p_specialization IS NULL OR btrim(p_specialization) = '' THEN
    RAISE EXCEPTION 'p_specialization must be non-empty'
      USING ERRCODE = '22023';
  END IF;

  FOR rec IN
    SELECT
      m.my_staff_id,
      m.partner_staff_id,
      d.specialization
    FROM partner_data.staff_integration_map m
    JOIN partner_data.doctor d
      ON d.doctor_id = m.partner_staff_id
    WHERE d.specialization = p_specialization
  LOOP
    BEGIN
      UPDATE partner_data.staff_integration_map m2
      SET integration_notes =
        'Auto-updated on ' || CURRENT_DATE::text ||
        ' for specialization=' || p_specialization
      WHERE m2.my_staff_id = rec.my_staff_id
        AND m2.partner_staff_id = rec.partner_staff_id;

      IF FOUND THEN
        v_updated_count := v_updated_count + 1;
      END IF;
    EXCEPTION
      WHEN others THEN
        RAISE NOTICE 'Failed to update mapping my_staff_id=% partner_staff_id=%: %',
          rec.my_staff_id, rec.partner_staff_id, SQLERRM;
    END;
  END LOOP;

  IF v_updated_count = 0 THEN
    RAISE EXCEPTION 'No mappings found/updated for specialization=%', p_specialization
      USING ERRCODE = 'P0001';
  END IF;
END;
$$;


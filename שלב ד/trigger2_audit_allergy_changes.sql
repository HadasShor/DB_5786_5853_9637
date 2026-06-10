-- טריגר 2 (UPDATE): trg_patient_allergy_severe_after_update
-- מתעד שינוי חומרת אלרגיה ל-Severe: מעדכן notes ומוסיף רשומה להיסטוריה הרפואית
CREATE OR REPLACE FUNCTION public.trgfn_patient_allergy_severe_after_update()
RETURNS trigger
LANGUAGE plpgsql
AS $$
DECLARE
  v_new_history_id numeric;
BEGIN
  IF (TG_OP = 'UPDATE')
     AND (NEW.severity = 'Severe')
     AND (OLD.severity IS DISTINCT FROM NEW.severity) THEN

    UPDATE public.patient_allergy pa
    SET notes = COALESCE(pa.notes, '') ||
              CASE WHEN pa.notes IS NULL OR pa.notes = '' THEN '' ELSE ' | ' END ||
              'Severity changed to Severe on ' || CURRENT_DATE::text
    WHERE pa.allergy_id = NEW.allergy_id;

    SELECT COALESCE(MAX(history_id), 0) + 1
    INTO v_new_history_id
    FROM public.patient_medical_history;

    INSERT INTO public.patient_medical_history (history_id, condition, diagnosis_date, notes, patient_id)
    VALUES (
      v_new_history_id,
      'Allergy Severity Alert',
      CURRENT_DATE,
      'Auto-created by trigger (allergy_id=' || NEW.allergy_id::text || ')',
      NEW.patient_id
    );
  END IF;

  RETURN NEW;
EXCEPTION
  WHEN others THEN
    RAISE EXCEPTION 'Trigger failed on patient_allergy(allergy_id=%): %', NEW.allergy_id, SQLERRM
      USING ERRCODE = 'P0001';
END;
$$;

DROP TRIGGER IF EXISTS trg_patient_allergy_severe_after_update ON public.patient_allergy;

CREATE TRIGGER trg_patient_allergy_severe_after_update
AFTER UPDATE OF severity ON public.patient_allergy
FOR EACH ROW
EXECUTE FUNCTION public.trgfn_patient_allergy_severe_after_update();

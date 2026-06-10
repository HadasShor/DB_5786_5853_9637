-- טריגר 1: trg_admission_validate_before_write
-- חוסם תאריך אשפוז עתידי, אשפוז חירום ללא סיבה, ותאריך שחרור לפני תאריך קליטה
CREATE OR REPLACE FUNCTION public.trgfn_admission_validate_before_write()
RETURNS trigger
LANGUAGE plpgsql
AS $$
BEGIN
  IF NEW.admission_date > CURRENT_DATE THEN
    RAISE EXCEPTION 'admission_date (%) cannot be in the future (admission_id=%)',
      NEW.admission_date, NEW.admission_id
      USING ERRCODE = '22008';
  END IF;

  IF NEW.admission_type = 'Emergency' AND (NEW.reason IS NULL OR btrim(NEW.reason) = '') THEN
    RAISE EXCEPTION 'Emergency admission requires non-empty reason (admission_id=%)', NEW.admission_id
      USING ERRCODE = 'P0001';
  END IF;

  IF NEW.discharge_date IS NOT NULL AND NEW.discharge_date < NEW.admission_date THEN
    RAISE EXCEPTION 'discharge_date (%) cannot be before admission_date (%) for admission_id=%',
      NEW.discharge_date, NEW.admission_date, NEW.admission_id
      USING ERRCODE = '22007';
  END IF;

  RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS trg_admission_validate_before_write ON public.admission;

CREATE TRIGGER trg_admission_validate_before_write
BEFORE INSERT OR UPDATE ON public.admission
FOR EACH ROW
EXECUTE FUNCTION public.trgfn_admission_validate_before_write();

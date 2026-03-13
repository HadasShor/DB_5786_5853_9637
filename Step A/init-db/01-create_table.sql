-- ==========================================
-- 1. (PATIENT)
-- ==========================================
CREATE TABLE PATIENT
(
  patient_id    numeric NOT NULL,
  phone         varchar(20) NOT NULL,
  gender        varchar(20) NOT NULL,
  date_of_birth date NOT NULL,
  last_name     varchar(50) NOT NULL,
  first_name    varchar(50) NOT NULL,
  address       varchar(200),
  email         varchar(100),
  PRIMARY KEY (patient_id),
  CONSTRAINT chk_patient_dob CHECK (date_of_birth < CURRENT_DATE),
  CONSTRAINT chk_patient_gender CHECK (gender IN ('Male', 'Female', 'Other'))
);

-- ==========================================
-- 2. (PATIENT_INSURANCE)
-- ==========================================
CREATE TABLE PATIENT_INSURANCE
(
  insurance_id    numeric NOT NULL,
  provider_name   varchar(100) NOT NULL,
  policy_number   varchar(50) NOT NULL,
  coverage_type   varchar(50),
  expiration_date date NOT NULL,
  patient_id      numeric NOT NULL,
  PRIMARY KEY (insurance_id),
  FOREIGN KEY (patient_id) REFERENCES PATIENT(patient_id)
);

-- ==========================================
-- 3. (ADMISSION)
-- ==========================================
CREATE TABLE ADMISSION
(
  admission_id   numeric NOT NULL,
  admission_date date NOT NULL,
  discharge_date date,
  admission_type varchar(50) NOT NULL,
  reason         varchar(500),
  patient_id     numeric NOT NULL,
  PRIMARY KEY (admission_id),
  FOREIGN KEY (patient_id) REFERENCES PATIENT(patient_id),
  CONSTRAINT chk_admission_dates CHECK (discharge_date IS NULL OR discharge_date >= admission_date),
  CONSTRAINT chk_adm_type CHECK (admission_type IN ('Emergency', 'Elective', 'Urgent'))
);

-- ==========================================
-- 4. (EMERGENCY_CONTACT)
-- ==========================================
CREATE TABLE EMERGENCY_CONTACT
(
  contact_id numeric NOT NULL,
  name       varchar(100) NOT NULL,
  relationship varchar(50),
  phone      varchar(20) NOT NULL,
  patient_id numeric NOT NULL,
  PRIMARY KEY (contact_id),
  FOREIGN KEY (patient_id) REFERENCES PATIENT(patient_id)
);

-- ==========================================
-- 5. (PATIENT_ALLERGY)
-- ==========================================
CREATE TABLE PATIENT_ALLERGY
(
  allergy_id   numeric NOT NULL,
  allergy_name varchar(100) NOT NULL,
  severity     varchar(50),
  notes        varchar(500),
  patient_id   numeric NOT NULL,
  PRIMARY KEY (allergy_id),
  FOREIGN KEY (patient_id) REFERENCES PATIENT(patient_id),
  CONSTRAINT chk_allergy_sev CHECK (severity IN ('Mild', 'Moderate', 'Severe', 'Unknown'))
);

-- ==========================================
-- 6. (PATIENT_MEDICAL_HISTORY)
-- ==========================================
CREATE TABLE PATIENT_MEDICAL_HISTORY
(
  history_id     numeric NOT NULL,
  condition      varchar(100) NOT NULL,
  diagnosis_date date NOT NULL,
  notes          varchar(500),
  patient_id     numeric NOT NULL,
  PRIMARY KEY (history_id),
  FOREIGN KEY (patient_id) REFERENCES PATIENT(patient_id),
  CONSTRAINT chk_history_date CHECK (diagnosis_date <= CURRENT_DATE)
);
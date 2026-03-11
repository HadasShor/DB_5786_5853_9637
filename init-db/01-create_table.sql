-- ==========================================
-- 1. TEACHER TABLE
-- ==========================================
CREATE TABLE TEACHER (
    -- Using VARCHAR(9) to support Israeli IDs (Teudat Zehut) with leading zeros
    T_ID VARCHAR(9) PRIMARY KEY CHECK (T_ID ~ '^[0-9]{9}$'), 
    Name VARCHAR(100) NOT NULL,
    Phone VARCHAR(15) NOT NULL UNIQUE,
    Mail VARCHAR(255) UNIQUE,
    
    -- Constraint: Basic format check for email
    CONSTRAINT valid_email CHECK (Mail ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$')
);

COMMENT ON TABLE TEACHER IS 'Registered kindergarten staff and teachers.';

-- ==========================================
-- 2. CHILD TABLE
-- ==========================================
CREATE TABLE CHILD (
    -- Child's Israeli ID (Teudat Zehut)
    C_ID VARCHAR(9) PRIMARY KEY CHECK (C_ID ~ '^[0-9]{9}$'), 
    Name VARCHAR(100) NOT NULL,
    ParentPhone VARCHAR(15) NOT NULL,
    BirthDate DATE NOT NULL,
    
    -- BINARY GENDER CONSTRAINT: Only 'M' (Male) or 'F' (Female) allowed
    Gender CHAR(1) NOT NULL CHECK (Gender IN ('M', 'F')),
    
    Allergies TEXT DEFAULT 'None',
    T_ID VARCHAR(9) NOT NULL, -- Must match the type of TEACHER.T_ID
    
    -- Constraint: Gan Age Range (Usually between 2.5 and 7 years old)
    CONSTRAINT gan_age_check CHECK (
        BirthDate > CURRENT_DATE - INTERVAL '7 years' AND 
        BirthDate < CURRENT_DATE - INTERVAL '2 years'
    ),
    
    -- Constraint: Israeli Phone format (Starts with 0, total 9-10 digits)
    CONSTRAINT valid_parent_phone CHECK (ParentPhone ~ '^0[0-9]{8,9}$'),

    -- Relationship: A child must be assigned to an existing teacher
    FOREIGN KEY (T_ID) REFERENCES TEACHER(T_ID) ON DELETE RESTRICT
);

COMMENT ON COLUMN CHILD.Gender IS 'Strict binary selection: M for Male, F for Female.';
COMMENT ON COLUMN CHILD.C_ID IS '9-digit Teudat Zehut of the child.';
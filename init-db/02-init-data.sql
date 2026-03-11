INSERT INTO TEACHER (T_ID, Name, Phone, Mail) VALUES
('312456789', 'Sarah Levy', '0501234567', 'sarah.l@gan-kids.org.il'),
('201456782', 'Michal Cohen', '0522233445', 'michal.c@gan-kids.org.il'),
('054789123', 'Rivka Mizrahi', '0543344556', 'rivka.m@gan-kids.org.il'),
('300123456', 'Noa Peretz', '0584455667', 'noa.p@gan-kids.org.il'),
('025896314', 'Tamar Friedman', '0505566778', 'tamar.f@gan-kids.org.il'),
('315487962', 'Yael Katz', '0526677889', 'yael.k@gan-kids.org.il'),
('047852369', 'Adi Biton', '0547788990', 'adi.b@gan-kids.org.il'),
('206987412', 'Sigal Amar', '0538899001', 'sigal.a@gan-kids.org.il'),
('308741256', 'Maya Ohayon', '0509900112', 'maya.o@gan-kids.org.il'),
('066321458', 'Shira Azoulay', '0521122334', 'shira.a@gan-kids.org.il');


DO $$
DECLARE
    -- Lists for generating realistic Israeli names
    boy_names TEXT[] := ARRAY['Noam', 'Ariel', 'Itay', 'David', 'Ori', 'Yosef', 'Omer', 'Adam', 'Lavie', 'Eitan', 'Daniel', 'Moshe', 'Rafael', 'Liam', 'Ben'];
    girl_names TEXT[] := ARRAY['Tamar', 'Maya', 'Abigail', 'Ayala', 'Romi', 'Adele', 'Noa', 'Shira', 'Talia', 'Yael', 'Sara', 'Lian', 'Hila', 'Roni', 'Lihi'];
    last_names TEXT[] := ARRAY['Cohen', 'Levy', 'Mizrahi', 'Peretz', 'Friedman', 'Katz', 'Biton', 'Amar', 'Ohayon', 'Azoulay', 'Klein', 'Golan', 'Hadad', 'Shapiro', 'Dahan'];
    allergies_list TEXT[] := ARRAY['Peanuts', 'Dairy', 'Eggs', 'Sesame', 'Gluten', 'None', 'None', 'None', 'None', 'None'];
    
    teacher_ids TEXT[] := ARRAY['312456789','201456782','054789123','300123456','025896314','315487962','047852369','206987412','308741256','066321458'];
    
    current_gender CHAR(1);
    current_name TEXT;
    i INT;
BEGIN
    FOR i IN 1..200 LOOP
        -- 1. Determine Gender (Binary balance)
        IF i % 2 = 0 THEN 
            current_gender := 'M';
            current_name := boy_names[1 + (i % 15)] || ' ' || last_names[1 + (i % 15)];
        ELSE 
            current_gender := 'F';
            current_name := girl_names[1 + (i % 15)] || ' ' || last_names[1 + (i % 15)];
        END IF;

        -- 2. Insert the record
        INSERT INTO CHILD (C_ID, Name, ParentPhone, BirthDate, Gender, Allergies, T_ID)
        VALUES (
            -- ID: Generate unique 9-digit ID starting with 5 or 6 (Israeli TZ style)
            (500000000 + i)::text, 
            
            -- Name from the arrays above
            current_name,
            
            -- Parent Phone: Realistic Israeli mobile format
            '05' || (40000000 + (i * 12345) % 8999999)::text,
            
            -- BirthDate: Randomly distributed between 3.5 and 5.5 years ago
            CURRENT_DATE - (INTERVAL '3 years' + ( (i * 7 % 1000) * INTERVAL '1 day')),
            
            -- Gender (Strict Binary)
            current_gender,
            
            -- Allergies (Random selection from the list)
            allergies_list[1 + (i % 10)],
            
            -- T_ID: Distributes 20 children to each of the 10 teachers
            teacher_ids[1 + ((i - 1) / 20)]
        );
    END LOOP;
END $$;
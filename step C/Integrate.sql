CREATE EXTENSION IF NOT EXISTS postgres_fdw;

CREATE SERVER partner_server FOREIGN DATA WRAPPER postgres_fdw 
OPTIONS (host 'localhost', dbname 'partner_db', port '5432');

CREATE USER MAPPING FOR current_user SERVER partner_server 
OPTIONS (user 'Myuser', password 'pas1234');


CREATE SCHEMA partner_data;
IMPORT FOREIGN SCHEMA public FROM SERVER partner_server INTO partner_data;

CREATE TABLE public.staff_integration_map (
    my_staff_id INT REFERENCES public.staff(staff_id), 
    partner_staff_id INT, 
    integration_notes TEXT,
    PRIMARY KEY (my_staff_id, partner_staff_id)
);
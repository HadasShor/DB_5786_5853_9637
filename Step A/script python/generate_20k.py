import random

with open('big_data.sql', 'w', encoding='utf-8') as f:
    f.write("-- 20,000 Patients\n")
    for i in range(1, 20001):
        f.write(f"INSERT INTO PATIENT (patient_id, first_name, last_name, date_of_birth, gender, phone) VALUES ({i}, 'Patient_{i}', 'Last_{i}', '1985-01-01', 'Other', '0501111111');\n")
    
    f.write("\n-- 20,000 Admissions\n")
    for i in range(1, 20001):
        p_id = random.randint(1, 20000)
        f.write(f"INSERT INTO ADMISSION (admission_id, patient_id, admission_date, admission_type) VALUES ({i}, {p_id}, '2024-01-01', 'Emergency');\n")

print("Done! Open big_data.sql and copy the content.")
# שלב ה – ממשק גרפי (GUI)

## הקדמה

בשלב זה נבנתה אפליקציית GUI ב‑Python עם Tkinter, שמתחברת ל‑PostgreSQL ומאפשרת:

- **CRUD מלא** (Create / Read / Update / Delete) עבור כל הטבלאות במערכת
- הצגת נתונים בצורה ידידותית: **ללא הצגת IDs בטבלאות התצוגה**, ובמקום מפתחות זרים מוצגים ערכים “אנושיים” (לדוגמה: שם מטופל במקום `patient_id`)
- מסך ייעודי להפעלת:
  - לפחות **2 שאילתות** משלב ב'
  - לפחות **2 תתי‑תוכניות** (פונקציות/פרוצדורות) משלב ד'

## התקנה

מומלץ לעבוד עם venv:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## הרצה

```bash
python -m medflow_gui.main
```

## פרטי חיבור לבסיס הנתונים

האפליקציה מציגה **מסך כניסה** שבו מזינים Host/Port/DB/User/Password.

אפשר גם להגדיר משתני סביבה (אופציונלי):

- `PGHOST`
- `PGPORT`
- `PGDATABASE`
- `PGUSER`
- `PGPASSWORD`

## מסכים באפליקציה

- **Login**: התחברות לבסיס הנתונים וכניסה למערכת
- **Patients**: CRUD לטבלת `patient`
- **Admissions**: CRUD לטבלת `admission` (הצגת שם מטופל במקום `patient_id`)
- **Allergies**: CRUD לטבלת `patient_allergy`
- **Insurance**: CRUD לטבלת `patient_insurance`
- **Medical History**: CRUD לטבלת `patient_medical_history`
- **Emergency Contacts**: CRUD לטבלת `emergency_contact`
- **Queries & Programs**:
  - 2 שאילתות משלב ב'
  - הפעלת 2 תתי‑תוכניות משלב ד' (פונקציה + פרוצדורה)

## הוכחות לדו"ח (איפה לשים תמונות)

יש לשמור את כל צילומי המסך לדו"ח בתיקייה:

`Step E/screenshots/`

ובדו"ח/README של השלב לשבץ אותם בסגנון:

`![תיאור](screenshots/TODO.png)`


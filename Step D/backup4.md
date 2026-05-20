## backup4 (שלב ד)

לא ניתן לייצר גיבוי `pg_dump` מתוך הריפו בלי גישה ישירה לשרת/DB בזמן העבודה כאן.

כדי לייצר את קובץ ההגשה `backup4.sql` אצלך אחרי שהרצת את כל קבצי שלב ד', הריצי (בדוגמה):

```bash
pg_dump -h localhost -p 5432 -U Myuser -d <YOUR_DB_NAME> -F p -f "backup4.sql"
```

ולאחר מכן שימי את `backup4.sql` בתוך תיקיית `שלב ד`.


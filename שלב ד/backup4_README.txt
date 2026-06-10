יצירת backup4.sql
=================

לאחר הרצת כל קבצי שלב ד' ב-pgAdmin, הריצי מהטרמינל:

  pg_dump -h localhost -p 5432 -U Myuser -d <שם_בסיס_הנתונים> -F p -f "backup4.sql"

שמרי את הקובץ backup4.sql בתיקייה זו (שלב ד).

אם אתן משתמשות ב-Docker:
  docker exec PostgreSQL_DB pg_dump -U <DB_USER> -d <DB_NAME> -F p > "שלב ד/backup4.sql"

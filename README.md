# DB_5786_5853_9637
# מיני פרוייקט בבסיסי נתונים
## שלב א'

**מגישות:**
* הדס שור - 327785853
* נורית עזרא - 327739637

**מערכת:** בית חולים
**יחידה:** מחלקת פציינט

---

### מטרת המערכת:
מערכת MedFlow היא פלטפורמה לניהול מקיף של נתוני מטופלים ותהליכי אשפוז בתוך יחידה רפואית (מחלקה או בית חולים). 
המערכת נועדה להחליף רישום ידני בניהול דיגיטלי חכם, המאפשר מעקב בזמן אמת אחר ההיסטוריה הרפואית של המטופל מרגע קליטתו ועד שחרורו.

---

### הנתונים הנשמרים במערכת:
בסיס הנתונים של המערכת מרכז מידע רב-שכבתי על כל מטופל.

* **מידע דמוגרפי וקשר:** פרטים אישיים (שם, תאריך לידה, מגדר) ודרכי התקשרות מהירות.
* **נתוני אשפוז וקליטה:** תיעוד מועדי כניסה ושחרור, סוג האשפוז (חירום/מוזמן) וסיבת הפנייה הרפואית.
* **היסטורית רפואית ובטיחות:** מעקב אחר אבחנות קודמות (Conditions) ורשימת אלרגיות מעודכנת כולל רמות חומרה, למניעת טעויות רפואיות.
* **ניהול אדמיניסטרטיבי:** פרטי ביטוח רפואי (ספק, מספר פוליסה ותוקף) ואנשי קשר לשעת חירום לצורך תיאום מול משפחת המטופל.

### הפונקציונאליות העיקרית:



**ניהול רשומת מטופל (Patient Registry):** ריכוז כל המידע הרפואי והאישי תחת מזהה ייחודי (Patient_ID) המאפשר שליפה מהירה של נתונים בכל רגע נתון.

* **תהליך קליטה מהיר (Admission Streamlining):** ממשק המאפשר פתיחת תיק מטופל חדש במקביל לרישום פרטי האשפוז הנוכחי, מה שחוסך זמן קריטי בחדרי מיון.

* **בקרה רפואית:** מתן אפשרות לצוות הרפואי לצפות באלרגיות ובהיסטוריה הרפואית של המטופל מיד עם הגעתו, כדי להתאים לו את הטיפול הבטוח ביותר.

* **מעקב סטטיסטי ותפעולי:** ניהול תאריכי שחרור ואשפוז המאפשר למנהלי המחלקה לעקוב אחר תפוסת מיטות ומשך אשפוז ממוצע.

---



### המסכים שלנו:
![M1](Step%20A/screenshot/1_1.png)
![M1](Step%20A/screenshot/1_2.png)
![M1](Step%20A/screenshot/1_3.png)




__החלטות עיצוב ונימוקים__

בתהליך תכנון בסיס הנתונים של מערכת MedFlow, התקבלה סדרה של החלטות עיצוביות שמטרתן להבטיח את תקינות הנתונים, גמישות המערכת ועמידה בסטנדרטים של נרמול (3NF).

א. הפרדה לישויות עצמאיות (נרמול 3NF)

במקום לשמור את כל פרטי המטופל בטבלה אחת גדולה, בחרנו לפצל את המידע ל-6 ישויות שונות

הנימוק: מטופל אחד יכול לעבור מספר אשפוזים, לסבול ממספר אלרגיות ולהחזיק מספר היסטוריות רפואיות. 
הפרדה זו מונעת כפילות נתונים (Redundancy) ומאפשרת הוספת נתונים חדשים מבלי לפגוע בנתונים הקיימים.


ב. ניהול היסטוריה רפואית ואלרגיות כישויות נפרדות

החלטנו להפריד את Patient_Allergy ו-Patient_Medical_History מטבלת המטופל.
	
	הנימוק: מדובר במאפיינים רב-ערכיים (Multi-valued attributes). 
	אם היינו שומרים אלרגיות בשדה טקסט אחד בטבלת המטופל, לא היינו יכולים לבצע שאילתות חכמות (כמו "כמה מטופלים 
	אלרגיים לפניצילין?").
	העיצוב הנוכחי מאפשר שליפה מדויקת וניתוח נתונים רפואי.


ג. שימוש במפתחות מלאכותיים (Surrogate Keys)

לכל טבלה הגדרנו מזהה ייחודי מסוג SERIAL (למשל patient_id, admission_id).

	הנימוק: העדפנו מפתחות מלאכותיים על פני מפתחות טבעיים (כמו תעודת זהות) כדי להבטיח שהמפתח הראשי לעולם לא 
	ישתנה, מה ששומר על יציבות הקשרים (Foreign Keys) בין הטבלאות.


ד. תיעוד תאריכים משמעותיים (Temporal Data)

הקפדנו על שימוש בשדות DATE עבור אירועים קריטיים: date_of_birth, admission_date, discharge_date ו-expiration_date.

	הנימוק: שימוש בטיפוס הנתונים DATE (ולא במחרוזת טקסט) מאפשר לנו לבצע חישובים לוגיים כמו חישוב גיל המטופל,
	חישוב משך ימי אשפוז, ושליחת התראות על פוליסת ביטוח שעומדת לפוג.


ה. ישות קשר לשעת חירום (Emergency_Contact)


הפרדנו את פרטי איש הקשר לטבלה נפרדת המקושרת למטופל.

	הנימוק: בבתי חולים, לעיתים יש צורך ביותר מאיש קשר אחד. המבנה הנוכחי תומך בקשר של 1:N (מטופל אחד ל-N אנשי קשר), 
	מה שמעניק גמישות תפעולית במצבי חירום.


__סכמות__:

__ERD__

![ERD](Step%20A/ERD.jpeg)
__DSD__

![DSD](Step%20A/DSD.jpeg)



__שיטות הכנסת נתונים__:
__script python__
![M1](Step%20A/screenshot/1_4.png)

__Programing__
![M1](Step%20A/screenshot/1_5.png)

__mockarooFiles__
![M1](Step%20A/screenshot/1_6.png)





__גיבוי ושחזור נתונים__:
1. 
![M1](Step%20A/screenshot/1_7.png)

2.
![M1](Step%20A/screenshot/1_8.png)

3.
![M1](Step%20A/screenshot/1_9.png)





__שלב ב'__



__שאילתות select:__ 


1. תיאור: שליפת השם הפרטי, שם המשפחה והאימייל של כל המטופלים שיש להם לפחות רישום אשפוז אחד במהלך שנת 2024, מסודר לפי שם משפחה.
   
הבדל בין שתי הצורות:
הצורה הראשונה משתמשת בתת-שאילתה עם האופרטור IN כדי לסנן מזהי מטופלים. 
הצורה השנייה משתמשת ב-JOIN ישיר בין טבלת המטופלים לאשפוזים ומשתמשת ב-DISTINCT כדי למנוע כפילויות (במקרה שלמטופל יש יותר מאשפוז אחד).

מי יותר יעיל: הצורה השנייה (JOIN).

סיבה: ברוב מסדי הנתונים המודרניים, ה-Optimizer יודע לבצע JOIN בצורה יעילה יותר (למשל באמצעות Hash Join). שימוש ב-IN עלול להיות איטי יותר אם תת-השאילתה מחזירה כמות עצומה של מזהים ייחודיים, שכן מסד הנתונים צריך להשוות כל שורה בטבלה הראשית מול הרשימה שנוצרה.



קוד: 

* SELECT first_name, last_name, email
	FROM PATIENT
	WHERE patient_id IN (
	    SELECT patient_id FROM ADMISSION 
	    WHERE EXTRACT(YEAR FROM admission_date) = 2024
	)
	ORDER BY last_name;


* SELECT DISTINCT p.first_name, p.last_name, p.email
FROM PATIENT p
JOIN ADMISSION a ON p.patient_id = a.patient_id
WHERE EXTRACT(YEAR FROM a.admission_date) = 2024
ORDER BY last_name;


הרצת תוצאה:

![M1](Step%20B/screenshot/s1_1.png)
![M1](Step%20B/screenshot/s1_2.png)





2.תיאור: הצגת כמות האשפוזים הכוללת שבוצעה בכל שנה, עבור מטופלים שמוגדרת להם אלרגיה ברמת חומרה 'Severe

הבדל בין שתי הצורות:
השאילתה הראשונה מבצעת JOIN בין אשפוזים לאלרגיות. 
השאילתה השנייה משתמשת בקינון (IN) כדי לבודד קודם את המטופלים האלרגיים ורק אז לספור את האשפוזים שלהם בטבלה הראשית.

מי יותר יעיל: הצורה השנייה (IN / תת-שאילתה)

סיבה: במקרה הזה, מכיוון שאנחנו צריכים לספור אשפוזים, ה-JOIN (צורה 1) עלול ליצור כפילויות בשורות לפני ה-Count אם למטופל יש מספר אלרגיות חמורות, מה שיחייב שימוש ב-COUNT(DISTINCT...). השאילתה עם ה-IN "מנקה" את רשימת המטופלים מראש ומאפשרת ספירה פשוטה ומהירה יותר של טבלת האשפוזים.


קוד:
	* 
SELECT EXTRACT(YEAR FROM a.admission_date) as year_part, COUNT(a.admission_id) as total_admissions
FROM ADMISSION a
JOIN PATIENT_ALLERGY pa ON a.patient_id = pa.patient_id
WHERE pa.severity = 'Severe'
GROUP BY EXTRACT(YEAR FROM a.admission_date)
ORDER BY year_part DESC;


* 
SELECT EXTRACT(YEAR FROM admission_date) as year_part, COUNT(*) as total_admissions
FROM ADMISSION
WHERE patient_id IN (
    SELECT patient_id FROM PATIENT_ALLERGY WHERE severity = 'Severe'
)
GROUP BY EXTRACT(YEAR FROM admission_date)
ORDER BY year_part DESC;


הרצת תוצאה:

![M1](Step%20B/screenshot/s2_1.png)
![M1](Step%20B/screenshot/s2_2.png)

3.תיאור: שליפת פרטים אישיים של מטופלים שנולדו לפני שנת 1965 וסובלים מאלרגיה חמורה.

הבדל בין שתי הצורות:
השאילתה הראשונה מחזירה רק פרטי זיהוי בסיסיים באמצעות תת-שאילתה.
השאילתה השנייה מורכבת יותר: היא מחזירה עמודה נוספת (סך כל האלרגיות החמורות לכל מטופל) ומשתמשת ב-GROUP BY ו-ORDER BY כדי לארגן את המידע בצורה מפורטת יותר.

מי יותר יעיל: הצורה הראשונה (IN)

סיבה: אם המטרה היא רק להציג את רשימת האנשים (בלי לספור כמה אלרגיות יש להם), הצורה הראשונה מהירה יותר כי היא לא צריכה לבצע פעולת קיבוץ (Aggregation) וחישוב ממוצעים/סכומים על כל שורה ושורה. היא פשוט בודקת תנאי קיום.


קוד:

	*
	SELECT p.first_name, p.last_name, p.phone
	FROM PATIENT p
	WHERE p.patient_id IN (
	    SELECT pa.patient_id 
	    FROM PATIENT_ALLERGY pa 
	    WHERE pa.severity = 'Severe'
	) AND EXTRACT(YEAR FROM p.date_of_birth) < 1965;

	* -- שימוש ב-JOIN ו-GROUP BY
SELECT p.first_name, p.last_name, p.phone, 
       EXTRACT(YEAR FROM p.date_of_birth) as birth_year,
       COUNT(pa.allergy_id) as total_severe_allergies
FROM PATIENT p
JOIN PATIENT_ALLERGY pa ON p.patient_id = pa.patient_id
WHERE p.date_of_birth < TO_DATE('1965-01-01', 'YYYY-MM-DD')
  AND pa.severity = 'Severe'
GROUP BY p.patient_id, p.first_name, p.last_name, p.phone, p.date_of_birth
ORDER BY birth_year ASC;


הרצת תוצאה:
![M1](Step%20B/screenshot/s3_1.png)
![M1](Step%20B/screenshot/s3_2.png)

4.תיאור: ספירת כמות האשפוזים לכל שנה עבור מטופלים עם אלרגיה חמורה, תוך שימוש בפירוק תאריך לשנה.

ההבדל בין שתי הצורות:
 השאילתה הראשונה משתמשת ב-IN, שיוצר רשימה קבועה של מזהים. 
 השאילתה השנייה משתמשת ב-EXISTS, שזו שאילתה מקושרת (Correlated Subquery) שבודקת עבור כל שורת אשפוז האם קיים מטופל מתאים בטבלת האלרגיות.

מי יותר יעיל: הצורה השנייה (EXISTS).

סיבה: EXISTS נחשב ליעיל יותר בבסיסי נתונים גדולים כי הוא עובד בשיטת "Short-circuit" – ברגע שהוא מוצא התאמה אחת בטבלת האלרגיות עבור המטופל, הוא עוצר ומחזיר 'True' בלי לסרוק את שאר האלרגיות שלו. IN לעומת זאת, חייב לעיתים קרובות לבנות את כל רשימת המזהים בזיכרון לפני תחילת הסינון.

קוד:
	*
SELECT EXTRACT(YEAR FROM admission_date) as year_part, COUNT(*) as total_admissions
FROM ADMISSION
WHERE patient_id IN (SELECT patient_id FROM PATIENT_ALLERGY WHERE severity = 'Severe')
GROUP BY EXTRACT(YEAR FROM admission_date)
ORDER BY year_part DESC;

*
SELECT EXTRACT(YEAR FROM a.admission_date) as year_part, COUNT(*) as total_admissions
FROM ADMISSION a
WHERE EXISTS (SELECT 1 FROM PATIENT_ALLERGY pa WHERE pa.patient_id = a.patient_id AND pa.severity = 'Severe')
GROUP BY EXTRACT(YEAR FROM a.admission_date)
ORDER BY year_part DESC;


הרצת תוצאה:
![M1](Step%20B/screenshot/s4_1.png)
![M1](Step%20B/screenshot/s4_2.png)



5.תיאור: שאילתא זו מאתרת את "המטופלים הכבדים" של בית החולים. היא מחשבת את כמות האשפוזים לכל מטופל ומציגה רק את אלו שמספר האשפוזים שלהם גבוה מהממוצע הכללי של כלל המטופלים במערכת

קוד:

	*
	SELECT p.first_name, p.last_name, COUNT(a.admission_id) as num_admissions
	FROM PATIENT p
	JOIN ADMISSION a ON p.patient_id = a.patient_id
	GROUP BY p.patient_id, p.first_name, p.last_name
	HAVING COUNT(a.admission_id) > (SELECT AVG(cnt) FROM (SELECT COUNT(*) as cnt FROM ADMISSION GROUP BY patient_id));


הרצת תוצאה:

![M1](Step%20B/screenshot/s5_1.png)


6.תיאור: השאילתא מציגה רשימת קשר (שם וטלפון) של מטופלים שביקרו בבית החולים יותר מ-3 פעמים. המידע מוצג בסדר יורד, כך שהמטופל עם הכי הרבה ביקורים מופיע ראשון.

קוד:

	SELECT p.first_name, p.last_name, p.phone, count_table.total_visits
FROM PATIENT p
JOIN (
    SELECT patient_id, COUNT(*) AS total_visits
    FROM ADMISSION
    GROUP BY patient_id
    HAVING COUNT(*) > 3
) AS count_table ON p.patient_id = count_table.patient_id
ORDER BY count_table.total_visits DESC;


הרצת תוצאה:

![M1](Step%20B/screenshot/s6_1.png)

7.תיאור: דוח רפואי מפורט המציג מטופלים הסובלים ממחלות כרוניות (Chronic) שאושפזו לפחות פעם אחת. הדוח מציג את שם המטופל, המחלה, ופירוט של שנת וחודש האבחון.

קוד:


SELECT 
    p.first_name || ' ' || p.last_name AS full_name,
    pmh.condition,
    EXTRACT(YEAR FROM pmh.diagnosis_date) AS diagnosis_year,
    EXTRACT(MONTH FROM pmh.diagnosis_date) AS diagnosis_month,
    (SELECT COUNT(*) FROM ADMISSION a WHERE a.patient_id = p.patient_id) AS total_admissions
FROM PATIENT p
JOIN PATIENT_MEDICAL_HISTORY pmh ON p.patient_id = pmh.patient_id
WHERE pmh.condition LIKE '%Chronic%'
  AND p.patient_id IN (SELECT patient_id FROM ADMISSION)
GROUP BY p.first_name, p.last_name, pmh.condition, pmh.diagnosis_date, p.patient_id
ORDER BY total_admissions DESC, diagnosis_year ASC;



הרצת תוצאה:

![M1](Step%20B/screenshot/s7_1.png)
8.תיאור: שאילתא סטטיסטית המיועדת לממשק הניהולי, המציגה את כמות האלרגיות הרשומות לכל מטופל "ותיק" (יליד המאה ה-20). השמות מוצגים בסדר אלפביתי לפי שם משפחה.


קוד:

SELECT 
    p.first_name, 
    p.last_name, 
    EXTRACT(YEAR FROM p.date_of_birth) AS birth_year,
    COUNT(pa.allergy_id) AS num_of_allergies
FROM PATIENT p
JOIN PATIENT_ALLERGY pa ON p.patient_id = pa.patient_id
WHERE p.patient_id IN (
    -- תת שאילתה: סינון מטופלים שנולדו לפני 2000
    SELECT patient_id 
    FROM PATIENT 
    WHERE EXTRACT(YEAR FROM date_of_birth) < 2000
)
GROUP BY p.first_name, p.last_name, p.date_of_birth
ORDER BY p.last_name ASC;



הרצת תוצאה:

![M1](Step%20B/screenshot/s8_1.png)
__שאילתות delete:__

1.תיאור: שאילתא זו מבצעת "ניקוי נתונים" עבור מטופלים שנולדו אחרי שנת 2000 ושמעולם לא אושפזו בבית החולים. המטרה היא להסיר היסטוריה רפואית של אנשים שאינם נחשבים למטופלים פעילים במערכת האשפוז.

הרצה:


DELETE FROM PATIENT_MEDICAL_HISTORY 
WHERE patient_id IN (
    SELECT p.patient_id 
    FROM PATIENT p
    LEFT JOIN ADMISSION a ON p.patient_id = a.patient_id
    WHERE p.date_of_birth > '2000-01-01'
    GROUP BY p.patient_id
    HAVING COUNT(a.admission_id) = 0
);


![M1](Step%20B/screenshot/d1_1.png)

בסיס נתונים לפני עידכון:

![M1](Step%20B/screenshot/d1_2.png)
בסיס נתונים אחרי עידכון:

![M1](Step%20B/screenshot/d1_3.png)

2.תיאור: השאילתא מסירה רשומות אלרגיה מסוג 'Mild' (קלה) או 'Unknown' (לא ידועה) עבור מטופלים שנולדו לפני שנת 1990 ושיש להם לפחות 2 אלרגיות רשומות במערכת. המטרה היא לצמצם עומס מידע ב-GUI ולהתמקד באלרגיות המשמעותיות יותר אצל מטופלים אלו.

הרצה:

DELETE FROM PATIENT_ALLERGY 
WHERE severity IN ('Mild', 'Unknown')
AND patient_id IN (
    -- תת-שאילתה: מוצאת מטופלים מבוגרים שיש להם לפחות 2 אלרגיות
    SELECT pa.patient_id 
    FROM PATIENT_ALLERGY pa
    JOIN PATIENT p ON pa.patient_id = p.patient_id
    WHERE EXTRACT(YEAR FROM p.date_of_birth) < 1990
    GROUP BY pa.patient_id
    HAVING COUNT(pa.allergy_name) >= 2
);


![M1](Step%20B/screenshot/d2_1.png)

בסיס נתונים לפני עידכון:
![M1](Step%20B/screenshot/d2_2.png)

בסיס נתונים אחרי עידכון:

![M1](Step%20B/screenshot/d2_3.png)

3.תיאור: 
שאילתא זו מבצעת עדכון למדיניות הקשר בחירום עבור מטופלים שנולדו במאה הקודמת (לפני שנת 2000), ומסירה מהמערכת אנשי קשר שהגדרת היחסים איתם היא 'Friend'. ההנחה היא שעבור מטופלים אלו המערכת דורשת אנשי קשר מדרגת קרבה משפחתית בלבד.


הרצה:

DELETE FROM EMERGENCY_CONTACT
WHERE relationship = 'Friend'
  AND patient_id IN (
      -- תת שאילתה מקוננת: מוצאת מזהי מטופלים שנולדו לפני שנת 2000
      SELECT patient_id 
      FROM PATIENT 
      WHERE EXTRACT(YEAR FROM date_of_birth) < 2000
      GROUP BY patient_id
  );DELETE FROM EMERGENCY_CONTACT
WHERE relationship = 'Friend'
  AND patient_id IN (
      -- תת שאילתה מקוננת: מוצאת מזהי מטופלים שנולדו לפני שנת 2000
      SELECT patient_id 
      FROM PATIENT 
      WHERE EXTRACT(YEAR FROM date_of_birth) < 2000
      GROUP BY patient_id

![M1](Step%20B/screenshot/d3_1.png)


בסיס נתונים לפני עידכון:
![M1](Step%20B/screenshot/d3_2.png)

בסיס נתונים אחרי עידכון:

![M1](Step%20B/screenshot/d3_3.png)

__שאילתות update:__

1.תיאור: 
שאילתא זו מעדכנת את סוג הכיסוי הביטוחי ל-'Chronic Care' עבור מטופלים שהביטוח שלהם בתוקף (פוקע ב-2024 ומעלה) ויש להם לפחות רישום אחד בטבלת ההיסטוריה הרפואית. המטרה היא להתאים את פוליסת הביטוח למטופלים שזקוקים למעקב רפואי שוטף.

הרצה:


UPDATE PATIENT_INSURANCE 
SET coverage_type = 'Chronic Care'
WHERE EXTRACT(YEAR FROM expiration_date) >= 2024
AND patient_id IN (
    SELECT patient_id 
    FROM PATIENT_MEDICAL_HISTORY 
    GROUP BY patient_id 
    HAVING COUNT(*) >= 1 
);

![M1](Step%20B/screenshot/u1_1.png)


בסיס נתונים לפני עידכון:
![M1](Step%20B/screenshot/u1_2.png)

בסיס נתונים אחרי עידכון:
![M1](Step%20B/screenshot/u1_3.png)

2.תיאור: שאילתא זו מעניקה הטבה של הארכת תוקף פוליסת הביטוח בשנה אחת (365 ימים) עבור קבוצת מטופלים שנולדו ביום הראשון של חודש כלשהו. זהו סוג של "מבצע" או תהליך אוטומטי המבוסס על נתונים דמוגרפיים.

הרצה:

UPDATE PATIENT_INSURANCE
SET expiration_date = expiration_date + 365
WHERE patient_id IN (
    SELECT patient_id FROM PATIENT 
    WHERE EXTRACT(DAY FROM date_of_birth) = 1
    GROUP BY patient_id
);
![M1](Step%20B/screenshot/u2_1.png)



בסיס נתונים לפני עידכון:
![M1](Step%20B/screenshot/u2_2.png)

בסיס נתונים אחרי עידכון:
![M1](Step%20B/screenshot/u2_3.png)


3.תיאור: שאילתא זו מעדכנת את עמודת ההערות ביומן האלרגיות של המטופלים. היא מסמנת את כל מי שאושפז במהלך חודש ינואר (לפי נתוני ה-INSERT שסיפקת ל-2024), ומנחה את הצוות לבצע אימות של האלרגיות שלהם בעקבות האשפוז האחרון.

הרצה:


UPDATE PATIENT_ALLERGY
SET notes = 'Post-Hospitalization Allergy Validation'
WHERE patient_id IN (
    -- תת שאילתה: מוצאת מטופלים שהתאשפזו בחודש ינואר
    SELECT patient_id 
    FROM ADMISSION 
    WHERE EXTRACT(MONTH FROM admission_date) = 1
    GROUP BY patient_id
    HAVING COUNT(*) >= 1
);
![M1](Step%20B/screenshot/u3_1.png)



בסיס נתונים לפני עידכון:
![M1](Step%20B/screenshot/u3_2.png)

בסיס נתונים אחרי עידכון:

![M1](Step%20B/screenshot/u3_3.png)

**ROLLBACK**


	1.
![M1](Step%20B/screenshot/r1_1.png)

	2.
![M1](Step%20B/screenshot/r1_2.png)

	3.
![M1](Step%20B/screenshot/r1_3.png)

	4.
![M1](Step%20B/screenshot/r1_4.png)

	5.
![M1](Step%20B/screenshot/r1_5.png)



**COMMIT**


	1.
![M1](Step%20B/screenshot/c1_1.png)

	2.
![M1](Step%20B/screenshot/c1_2.png)

	3.
![M1](Step%20B/screenshot/c1_3.png)

	4.
![M1](Step%20B/screenshot/c1_4.png)



	אילוץ 1:
	
 הגדרת כתובת דואר אלקטרוני כערך ייחודי (UNIQUE)

תיאור השינוי:
במבנה הטבלאות הראשוני, העמודה email בטבלת PATIENT הוגדרה כעמודה רגילה המאפשרת הזנת נתונים ללא הגבלה על כפילויות. בעזרת פקודת ALTER TABLE, הוספתי אילוץ מסוג UNIQUE שמוודא שכל כתובת מייל במערכת תופיע פעם אחת בלבד ותהיה מקושרת למטופל אחד בלבד.


הצורך העסקי:
במערכת רפואית מודרנית, המייל משמש לעיתים קרובות כמזהה לצורך התחברות לאזור האישי (כפי שניתן לראות במסכי ה-GUI של המערכת) או לשליחת תוצאות בדיקות רגישות. מתן אפשרות לשני מטופלים להחזיק באותה כתובת מייל עלול לגרום לטעויות בזיהוי, פגיעה בפרטיות המטופל (שליחת מידע רפואי לאדם הלא נכון) וכפילות רשומות.

פקודת ה-SQL לביצוע השינוי:


SQL
ALTER TABLE PATIENT 
ADD CONSTRAINT UNQ_PATIENT_EMAIL UNIQUE (email);



בדיקת האילוץ (ניסיון הכנסת נתונים סותרים):

כדי להוכיח שהאילוץ עובד, נבצע שני שלבים:

נכניס מטופל ראשון עם כתובת מייל מסוימת (הפעולה תצליח).
ננסה להכניס מטופל שני (עם ת"ז שונה) אך עם אותה כתובת מייל בדיוק.



SQL
-- שלב 1: הכנסת מטופל תקין
INSERT INTO PATIENT (patient_id, first_name, last_name, date_of_birth, gender, phone, email) 
VALUES (20100, 'ישראל', 'ישראלי', TO_DATE('1990-01-01', 'YYYY-MM-DD'), 'Male', '050-1111111', 'israel@example.com');

-- שלב 2: ניסיון הכנסת מטופל נוסף עם אותו מייל (צפוי להיכשל)
INSERT INTO PATIENT (patient_id, first_name, last_name, date_of_birth, gender, phone, email) 
VALUES (20101, 'הדס', 'לוי', TO_DATE('1995-05-10', 'YYYY-MM-DD'), 'Female', '050-2222222', 'israel@example.com');
תוצאה צפויה:
המערכת תעצור את הפעולה ותציג הודעת שגיאה הדומה לזו:
Error report - ORA-00001: unique constraint (UNQ_PATIENT_EMAIL) violated

	![M1](Step%20B/screenshot/e1_1.png)
	![M1](Step%20B/screenshot/e1_2.png)



אילוץ 2: הגבלת תוקף פוליסת הביטוח (CHECK)

תיאור השינוי:
בטבלת PATIENT_INSURANCE, העמודה expiration_date מייצגת את התאריך שבו פג תוקף הכיסוי הביטוחי של המטופל. בעזרת פקודת ALTER TABLE, הוספתי אילוץ מסוג CHECK המבטיח שלא יוכנס למערכת תאריך תפוגה שחל לפני שנת 2000. אילוץ זה מוודא שהנתונים המוזנים הם רלוונטיים לתקופת הפעילות של המערכת המודרנית.


הצורך העסקי:
ניהול ביטוחים הוא קריטי בבית חולים לצורך כיסוי עלויות הטיפול. הזנת תאריך שגוי (למשל, שנת 1990 במקום 2030 עקב טעות הקלדה) עלולה לגרום למערכת לסמן מטופל כ"חסר כיסוי" בטעות, מה שיגרור בעיות בירוקרטיות ועיכובים בטיפול. האילוץ מהווה "שכבת הגנה" ראשונה מפני טעויות אנוש של פקידי הקבלה.



פקודת ה-SQL לביצוע השינוי:

SQL
ALTER TABLE PATIENT_INSURANCE 
ADD CONSTRAINT CHK_INSURANCE_EXP 
CHECK (expiration_date > TO_DATE('2000-01-01', 'YYYY-MM-DD'));

בדיקת האילוץ (ניסיון הכנסת נתונים סותרים):

כדי להוכיח שהאילוץ פועל, ננסה להכניס פוליסת ביטוח עם תאריך תפוגה ישן מאוד (למשל משנת 1995), דבר שסותר את הכלל שהגדרנו.

SQL
-- ניסיון הכנסת ביטוח עם תאריך תפוגה שאינו חוקי (צפוי להיכשל)
INSERT INTO PATIENT_INSURANCE (insurance_id, provider_name, policy_number, coverage_type, expiration_date, patient_id) 
VALUES (401, 'Maccabi', 'POL-111', 'Gold', TO_DATE('1995-05-05', 'YYYY-MM-DD'), 1);


תוצאה צפויה:
בסיס הנתונים יזהה שהתאריך אינו עומד בתנאי ה-CHECK ויחסום את הפעולה עם הודעת שגיאה:
Error report - ORA-02290: check constraint (CHK_INSURANCE_EXP) violated
![M1](Step%20B/screenshot/e2_1.png)
![M1](Step%20B/screenshot/e2_2.png)

אילוץ 3:
הגבלת תאריך לידה לעבר (chk_patient_dob)

תיאור האילוץ:
אילוץ זה הוגדר בטבלת PATIENT מסוג CHECK. הוא מוודא שכל תאריך לידה שמוזן למערכת יהיה קטן מהתאריך הנוכחי (CURRENT_DATE).

הצורך העסקי:
מניעת שגיאות לוגיות חמורות שבהן מוזן בטעות תאריך לידה עתידי. במערכת לניהול בית חולים, לא ניתן לרשום מטופל שטרם נולד. הבטחת תקינות התאריך קריטית לחישובי גיל, למתן מינונים תרופתיים נכונים ולדוחות סטטיסטיים (כמו אלו שמוצגים בגרפים ב-GUI שלך).

ניסיון הכנסת נתונים סותרים (יצירת שגיאה):
ננסה להכניס מטופל חדש עם תאריך לידה עתידי (שנת 2099):



SQL
INSERT INTO PATIENT (patient_id, first_name, last_name, date_of_birth, gender, phone) 
VALUES (555, 'מטופל', 'עתידי', TO_DATE('2099-01-01', 'YYYY-MM-DD'), 'Male', '050-0000000');



תוצאת שגיאה מצופה:
Error report - ORA-02290: check constraint (CHK_PATIENT_DOB) violated
![M1](Step%20B/screenshot/e3_1.png)



אילוץ 4:
הגבלת ערכי מגדר (chk_patient_gender)

תיאור האילוץ:
בטבלת PATIENT קיים אילוץ CHECK המגביל את העמודה gender לערכים ספציפיים בלבד: 'Male', 'Female', או 'Other'.

הצורך העסקי:
שמירה על סטנדרטיזציה של הנתונים. אם כל פקיד יכתוב מגדר בצורה אחרת (למשל: 'M', 'Man', 'זכר'), לא נוכל להפיק דוחות סטטיסטיים מדויקים (כמו אלו שרואים בגרפים ב-GUI שלך).


ניסיון הכנסת נתונים סותרים (יצירת שגיאה):
ננסה להכניס ערך שלא קיים ברשימה המותרת:


SQL
INSERT INTO PATIENT (patient_id, first_name, last_name, date_of_birth, gender, phone) 
VALUES (502, 'Test', 'Gender', TO_DATE('1990-01-01', 'YYYY-MM-DD'), 'Unknown', '050-0000000');
תוצאת שגיאה מצופה: check constraint (CHK_PATIENT_GENDER) violated.
![M1](Step%20B/screenshot/e3_1.png)


אילוץ 5:
הגבלת רמת חומרת אלרגיה (chk_allergy_sev)

תיאור האילוץ:
אילוץ CHECK בטבלת PATIENT_ALLERGY המאפשר להזין בעמודת ה-severity אך ורק את הערכים הבאים: 'Mild', 'Moderate', 'Severe', או 'Unknown'.

הצורך העסקי:
מידע על חומרת אלרגיה הוא מציל חיים. האילוץ מבטיח שהצוות הרפואי משתמש בטרמינולוגיה מקצועית אחידה. הדבר מאפשר למערכת (בצד ה-GUI) להקפיץ התראות אדומות ובולטות רק עבור מקרים המוגדרים כ-'Severe', מה שמונע "עייפות התראות" ומבטיח טיפול מיידי במקרים מסכני חיים.


ניסיון הכנסת נתונים סותרים (יצירת שגיאה):
ננסה להכניס אלרגיה עם רמת חומרה שאינה חוקית לפי האילוץ:



SQL
INSERT INTO PATIENT_ALLERGY (allergy_id, allergy_name, severity, patient_id) 
VALUES (777, 'Penicillin', 'Very-High', 999999);
תוצאת שגיאה מצופה:
Error report - ORA-02290: check constraint (CHK_ALLERGY_SEV) violated

![M1](Step%20B/screenshot/e5_1.png)






















































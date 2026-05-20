from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any, Callable, Optional

from psycopg2.extensions import connection as PGConnection

from .db import DbConfig, connect, execute, fetch_all, fetch_one


def _format_rows_as_text(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "(no rows)"
    cols = list(rows[0].keys())
    widths = {c: max(len(c), *(len(str(r.get(c, ""))) for r in rows)) for c in cols}
    header = " | ".join(c.ljust(widths[c]) for c in cols)
    sep = "-+-".join("-" * widths[c] for c in cols)
    body = "\n".join(" | ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols) for r in rows)
    return f"{header}\n{sep}\n{body}"


class LoginFrame(ttk.Frame):
    def __init__(self, master: tk.Widget, on_login: Callable[[PGConnection], None]) -> None:
        super().__init__(master, padding=12)
        self._on_login = on_login
        cfg = DbConfig.from_env()

        self.var_host = tk.StringVar(value=cfg.host)
        self.var_port = tk.StringVar(value=str(cfg.port))
        self.var_db = tk.StringVar(value=cfg.database)
        self.var_user = tk.StringVar(value=cfg.user)
        self.var_pass = tk.StringVar(value=cfg.password)

        ttk.Label(self, text="Login", font=("Segoe UI", 18, "bold")).grid(row=0, column=0, sticky="w")

        form = ttk.Frame(self)
        form.grid(row=1, column=0, sticky="nsew", pady=(12, 0))
        for i, (lbl, var, show) in enumerate(
            [
                ("Host", self.var_host, None),
                ("Port", self.var_port, None),
                ("Database", self.var_db, None),
                ("User", self.var_user, None),
                ("Password", self.var_pass, "*"),
            ]
        ):
            ttk.Label(form, text=lbl).grid(row=i, column=0, sticky="w", pady=4)
            e = ttk.Entry(form, textvariable=var, width=40, show=show)
            e.grid(row=i, column=1, sticky="w", pady=4)

        ttk.Button(self, text="Connect", command=self._connect).grid(row=2, column=0, sticky="w", pady=(14, 0))
        ttk.Label(
            self,
            text="Tip: you can also set PGHOST/PGPORT/PGDATABASE/PGUSER/PGPASSWORD as environment variables.",
            foreground="#555",
        ).grid(row=3, column=0, sticky="w", pady=(10, 0))

        self.columnconfigure(0, weight=1)

    def _connect(self) -> None:
        try:
            cfg = DbConfig(
                host=self.var_host.get().strip(),
                port=int(self.var_port.get().strip()),
                database=self.var_db.get().strip(),
                user=self.var_user.get().strip(),
                password=self.var_pass.get(),
            )
            conn = connect(cfg)
            self._on_login(conn)
        except Exception as e:
            messagebox.showerror("Connection failed", str(e))


class TableCrudFrame(ttk.Frame):
    """
    CRUD helper for a single table.

    Requirement note:
    - IDs are not shown in the results table (Treeview).
    - For Update/Delete the user must provide the primary key value.
    """

    def __init__(
        self,
        master: tk.Widget,
        conn: PGConnection,
        title: str,
        pk: str,
        select_sql: str,
        insert_sql: str,
        update_sql: str,
        delete_sql: str,
        fields: list[tuple[str, str]],  # (label, column_name)
        pk_label: str,
        pk_hint: str = "",
        after_refresh: Optional[Callable[[], None]] = None,
    ) -> None:
        super().__init__(master, padding=10)
        self.conn = conn
        self.pk = pk
        self.select_sql = select_sql
        self.insert_sql = insert_sql
        self.update_sql = update_sql
        self.delete_sql = delete_sql
        self.fields = fields
        self.after_refresh = after_refresh

        ttk.Label(self, text=title, font=("Segoe UI", 14, "bold")).grid(row=0, column=0, sticky="w")

        top = ttk.Frame(self)
        top.grid(row=1, column=0, sticky="nsew", pady=(10, 0))

        # PK controls
        self.var_pk = tk.StringVar()
        ttk.Label(top, text=f"{pk_label} (for Update/Delete):").grid(row=0, column=0, sticky="w")
        ttk.Entry(top, textvariable=self.var_pk, width=18).grid(row=0, column=1, sticky="w", padx=(8, 0))
        if pk_hint:
            ttk.Label(top, text=pk_hint, foreground="#555").grid(row=0, column=2, sticky="w", padx=(10, 0))

        # Form fields
        self.vars: dict[str, tk.StringVar] = {}
        form = ttk.LabelFrame(self, text="Form", padding=10)
        form.grid(row=2, column=0, sticky="nsew", pady=(10, 0))

        for i, (lbl, col) in enumerate(fields):
            self.vars[col] = tk.StringVar()
            ttk.Label(form, text=lbl).grid(row=i, column=0, sticky="w", pady=4)
            ttk.Entry(form, textvariable=self.vars[col], width=50).grid(row=i, column=1, sticky="w", pady=4)

        btns = ttk.Frame(self)
        btns.grid(row=3, column=0, sticky="w", pady=(10, 0))
        ttk.Button(btns, text="Refresh", command=self.refresh).grid(row=0, column=0, padx=(0, 8))
        ttk.Button(btns, text="Insert", command=self.insert).grid(row=0, column=1, padx=(0, 8))
        ttk.Button(btns, text="Fetch by Key", command=self.fetch_by_key).grid(row=0, column=2, padx=(0, 8))
        ttk.Button(btns, text="Update", command=self.update).grid(row=0, column=3, padx=(0, 8))
        ttk.Button(btns, text="Delete", command=self.delete).grid(row=0, column=4, padx=(0, 8))

        # Results
        res = ttk.LabelFrame(self, text="Results", padding=8)
        res.grid(row=4, column=0, sticky="nsew", pady=(10, 0))

        self.tree = ttk.Treeview(res, columns=(), show="headings", height=14)
        vsb = ttk.Scrollbar(res, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(res, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        res.columnconfigure(0, weight=1)
        res.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(4, weight=1)

        self.refresh()

    def _set_tree(self, rows: list[dict[str, Any]]) -> None:
        self.tree.delete(*self.tree.get_children())
        if not rows:
            self.tree["columns"] = ("message",)
            self.tree.heading("message", text="message")
            self.tree.column("message", width=600, anchor="w")
            self.tree.insert("", "end", values=("No rows",))
            return

        cols = list(rows[0].keys())
        self.tree["columns"] = cols
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140, anchor="w")
        for r in rows:
            self.tree.insert("", "end", values=[r.get(c) for c in cols])

    def refresh(self) -> None:
        try:
            rows = fetch_all(self.conn, self.select_sql)
            self._set_tree(rows)
            if self.after_refresh:
                self.after_refresh()
        except Exception as e:
            messagebox.showerror("Refresh failed", str(e))

    def insert(self) -> None:
        try:
            values = [self.vars[col].get().strip() or None for _, col in self.fields]
            execute(self.conn, self.insert_sql, values)
            self.refresh()
        except Exception as e:
            messagebox.showerror("Insert failed", str(e))

    def fetch_by_key(self) -> None:
        try:
            key = self.var_pk.get().strip()
            if not key:
                messagebox.showwarning("Missing key", "Please enter the key value first.")
                return
            row = fetch_one(
                self.conn,
                f"SELECT * FROM {self._table_from_select()} WHERE {self.pk} = %s",
                (key,),
            )
            if not row:
                messagebox.showinfo("Not found", "No row found for the given key.")
                return
            for _, col in self.fields:
                if col in row:
                    self.vars[col].set("" if row[col] is None else str(row[col]))
        except Exception as e:
            messagebox.showerror("Fetch failed", str(e))

    def update(self) -> None:
        try:
            key = self.var_pk.get().strip()
            if not key:
                messagebox.showwarning("Missing key", "Please enter the key value first.")
                return
            values = [self.vars[col].get().strip() or None for _, col in self.fields] + [key]
            cnt = execute(self.conn, self.update_sql, values)
            if cnt == 0:
                messagebox.showinfo("Update", "No rows were updated (check the key).")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Update failed", str(e))

    def delete(self) -> None:
        try:
            key = self.var_pk.get().strip()
            if not key:
                messagebox.showwarning("Missing key", "Please enter the key value first.")
                return
            if not messagebox.askyesno("Confirm delete", "Are you sure you want to delete this record?"):
                return
            cnt = execute(self.conn, self.delete_sql, (key,))
            if cnt == 0:
                messagebox.showinfo("Delete", "No rows were deleted (check the key).")
            self.refresh()
        except Exception as e:
            messagebox.showerror("Delete failed", str(e))

    def _table_from_select(self) -> str:
        # best-effort: expects "FROM public.<table>" in select_sql
        lower = self.select_sql.lower()
        idx = lower.find(" from ")
        if idx == -1:
            raise ValueError("select_sql must contain FROM ...")
        after = lower[idx + 6 :].strip()
        return after.split()[0]


class QueriesAndProgramsFrame(ttk.Frame):
    def __init__(self, master: tk.Widget, conn: PGConnection) -> None:
        super().__init__(master, padding=10)
        self.conn = conn

        ttk.Label(self, text="Queries & Programs", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, sticky="w")

        left = ttk.Frame(self)
        left.grid(row=1, column=0, sticky="nsew", pady=(10, 0))

        # Step B queries (2)
        qbox = ttk.LabelFrame(left, text="Step B Queries", padding=10)
        qbox.grid(row=0, column=0, sticky="ew")
        ttk.Button(qbox, text="Query 1: Admissions in 2024 (patient names)", command=self._q1).grid(
            row=0, column=0, sticky="w", pady=4
        )
        ttk.Button(qbox, text="Query 2: Severe-allergy admissions per year", command=self._q2).grid(
            row=1, column=0, sticky="w", pady=4
        )

        # Step D programs (at least 2)
        pbox = ttk.LabelFrame(left, text="Step D Programs", padding=10)
        pbox.grid(row=1, column=0, sticky="ew", pady=(10, 0))

        self.var_patient_id = tk.StringVar(value="42001")
        ttk.Label(pbox, text="patient_id:").grid(row=0, column=0, sticky="w")
        ttk.Entry(pbox, textvariable=self.var_patient_id, width=18).grid(row=0, column=1, sticky="w", padx=(8, 0))
        ttk.Button(pbox, text="Run fn_patient_risk_score", command=self._run_risk).grid(
            row=0, column=2, sticky="w", padx=(12, 0)
        )

        self.var_days = tk.StringVar(value="60")
        ttk.Label(pbox, text="days:").grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(pbox, textvariable=self.var_days, width=18).grid(row=1, column=1, sticky="w", padx=(8, 0), pady=(8, 0))
        ttk.Button(pbox, text="Call sp_close_long_open_admissions", command=self._call_close).grid(
            row=1, column=2, sticky="w", padx=(12, 0), pady=(8, 0)
        )

        # Output
        outbox = ttk.LabelFrame(self, text="Output", padding=10)
        outbox.grid(row=1, column=1, sticky="nsew", padx=(12, 0), pady=(10, 0))
        self.txt = tk.Text(outbox, height=28, wrap="none")
        ysb = ttk.Scrollbar(outbox, orient="vertical", command=self.txt.yview)
        xsb = ttk.Scrollbar(outbox, orient="horizontal", command=self.txt.xview)
        self.txt.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
        self.txt.grid(row=0, column=0, sticky="nsew")
        ysb.grid(row=0, column=1, sticky="ns")
        xsb.grid(row=1, column=0, sticky="ew")
        outbox.columnconfigure(0, weight=1)
        outbox.rowconfigure(0, weight=1)

        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(1, weight=1)

    def _write(self, title: str, rows: Optional[list[dict[str, Any]]] = None, text: str = "") -> None:
        self.txt.delete("1.0", "end")
        self.txt.insert("end", title + "\n\n")
        if rows is not None:
            self.txt.insert("end", _format_rows_as_text(rows))
        if text:
            self.txt.insert("end", "\n\n" + text)

    def _q1(self) -> None:
        sql = """
SELECT DISTINCT p.first_name, p.last_name, p.email
FROM public.patient p
JOIN public.admission a ON p.patient_id = a.patient_id
WHERE EXTRACT(YEAR FROM a.admission_date) = 2024
ORDER BY p.last_name;
""".strip()
        rows = fetch_all(self.conn, sql)
        self._write("Query 1: Admissions in 2024", rows=rows)

    def _q2(self) -> None:
        sql = """
SELECT EXTRACT(YEAR FROM admission_date) as year_part, COUNT(*) as total_admissions
FROM public.admission
WHERE patient_id IN (
    SELECT patient_id FROM public.patient_allergy WHERE severity = 'Severe'
)
GROUP BY EXTRACT(YEAR FROM admission_date)
ORDER BY year_part DESC;
""".strip()
        rows = fetch_all(self.conn, sql)
        self._write("Query 2: Severe-allergy admissions per year", rows=rows)

    def _run_risk(self) -> None:
        pid = self.var_patient_id.get().strip()
        sql = "SELECT public.fn_patient_risk_score(%s) AS risk_score;"
        try:
            rows = fetch_all(self.conn, sql, (pid,))
            self._write("Step D: fn_patient_risk_score", rows=rows)
        except Exception as e:
            self._write("Step D: fn_patient_risk_score (ERROR)", text=str(e))

    def _call_close(self) -> None:
        days = self.var_days.get().strip()
        sql = "CALL public.sp_close_long_open_admissions(%s);"
        try:
            execute(self.conn, sql, (days,))
            self._write("Step D: sp_close_long_open_admissions", text="Procedure executed successfully.")
        except Exception as e:
            self._write("Step D: sp_close_long_open_admissions (ERROR)", text=str(e))


class MedFlowApp(ttk.Frame):
    def __init__(self, master: tk.Widget) -> None:
        super().__init__(master)
        self.conn: Optional[PGConnection] = None

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self._show_login()

    def _show_login(self) -> None:
        for w in self.container.winfo_children():
            w.destroy()
        LoginFrame(self.container, self._on_login).pack(fill="both", expand=True)

    def _on_login(self, conn: PGConnection) -> None:
        self.conn = conn
        for w in self.container.winfo_children():
            w.destroy()
        self._build_main_ui()

    def _build_main_ui(self) -> None:
        assert self.conn is not None

        nb = ttk.Notebook(self.container)
        nb.pack(fill="both", expand=True)

        # PATIENT (do not show patient_id in results)
        nb.add(
            TableCrudFrame(
                nb,
                self.conn,
                title="Patients",
                pk="patient_id",
                pk_label="patient_id",
                pk_hint="(key field; not shown in results table)",
                select_sql="""
SELECT first_name, last_name, date_of_birth, gender, phone, email, address
FROM public.patient
ORDER BY last_name, first_name;
""".strip(),
                insert_sql="""
INSERT INTO public.patient (first_name, last_name, date_of_birth, gender, phone, email, address, patient_id)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
""".strip(),
                update_sql="""
UPDATE public.patient
SET first_name=%s, last_name=%s, date_of_birth=%s, gender=%s, phone=%s, email=%s, address=%s
WHERE patient_id=%s;
""".strip(),
                delete_sql="DELETE FROM public.patient WHERE patient_id=%s;",
                fields=[
                    ("first_name", "first_name"),
                    ("last_name", "last_name"),
                    ("date_of_birth (YYYY-MM-DD)", "date_of_birth"),
                    ("gender (Male/Female/Other)", "gender"),
                    ("phone", "phone"),
                    ("email", "email"),
                    ("address", "address"),
                    ("patient_id (key for INSERT)", "patient_id"),
                ],
            ),
            text="Patients",
        )

        # ADMISSION
        nb.add(
            TableCrudFrame(
                nb,
                self.conn,
                title="Admissions",
                pk="admission_id",
                pk_label="admission_id",
                pk_hint="(key field; not shown in results table)",
                select_sql="""
SELECT
  (p.first_name || ' ' || p.last_name) AS patient_name,
  a.admission_date,
  a.discharge_date,
  a.admission_type,
  a.reason
FROM public.admission a
JOIN public.patient p ON p.patient_id = a.patient_id
ORDER BY a.admission_date DESC;
""".strip(),
                insert_sql="""
INSERT INTO public.admission (admission_date, discharge_date, admission_type, reason, patient_id, admission_id)
VALUES (%s,%s,%s,%s,%s,%s);
""".strip(),
                update_sql="""
UPDATE public.admission
SET admission_date=%s, discharge_date=%s, admission_type=%s, reason=%s, patient_id=%s
WHERE admission_id=%s;
""".strip(),
                delete_sql="DELETE FROM public.admission WHERE admission_id=%s;",
                fields=[
                    ("admission_date (YYYY-MM-DD)", "admission_date"),
                    ("discharge_date (YYYY-MM-DD or empty)", "discharge_date"),
                    ("admission_type (Emergency/Elective/Urgent)", "admission_type"),
                    ("reason", "reason"),
                    ("patient_id (key; will display as name in results)", "patient_id"),
                    ("admission_id (key for INSERT)", "admission_id"),
                ],
            ),
            text="Admissions",
        )

        # ALLERGIES
        nb.add(
            TableCrudFrame(
                nb,
                self.conn,
                title="Patient Allergies",
                pk="allergy_id",
                pk_label="allergy_id",
                pk_hint="(key field; not shown in results table)",
                select_sql="""
SELECT
  (p.first_name || ' ' || p.last_name) AS patient_name,
  pa.allergy_name,
  pa.severity,
  pa.notes
FROM public.patient_allergy pa
JOIN public.patient p ON p.patient_id = pa.patient_id
ORDER BY p.last_name, p.first_name, pa.allergy_name;
""".strip(),
                insert_sql="""
INSERT INTO public.patient_allergy (allergy_name, severity, notes, patient_id, allergy_id)
VALUES (%s,%s,%s,%s,%s);
""".strip(),
                update_sql="""
UPDATE public.patient_allergy
SET allergy_name=%s, severity=%s, notes=%s, patient_id=%s
WHERE allergy_id=%s;
""".strip(),
                delete_sql="DELETE FROM public.patient_allergy WHERE allergy_id=%s;",
                fields=[
                    ("allergy_name", "allergy_name"),
                    ("severity (Mild/Moderate/Severe/Unknown)", "severity"),
                    ("notes", "notes"),
                    ("patient_id", "patient_id"),
                    ("allergy_id (key for INSERT)", "allergy_id"),
                ],
            ),
            text="Allergies",
        )

        # INSURANCE
        nb.add(
            TableCrudFrame(
                nb,
                self.conn,
                title="Patient Insurance",
                pk="insurance_id",
                pk_label="insurance_id",
                pk_hint="(key field; not shown in results table)",
                select_sql="""
SELECT
  (p.first_name || ' ' || p.last_name) AS patient_name,
  pi.provider_name,
  pi.policy_number,
  pi.coverage_type,
  pi.expiration_date
FROM public.patient_insurance pi
JOIN public.patient p ON p.patient_id = pi.patient_id
ORDER BY p.last_name, p.first_name;
""".strip(),
                insert_sql="""
INSERT INTO public.patient_insurance (provider_name, policy_number, coverage_type, expiration_date, patient_id, insurance_id)
VALUES (%s,%s,%s,%s,%s,%s);
""".strip(),
                update_sql="""
UPDATE public.patient_insurance
SET provider_name=%s, policy_number=%s, coverage_type=%s, expiration_date=%s, patient_id=%s
WHERE insurance_id=%s;
""".strip(),
                delete_sql="DELETE FROM public.patient_insurance WHERE insurance_id=%s;",
                fields=[
                    ("provider_name", "provider_name"),
                    ("policy_number", "policy_number"),
                    ("coverage_type", "coverage_type"),
                    ("expiration_date (YYYY-MM-DD)", "expiration_date"),
                    ("patient_id", "patient_id"),
                    ("insurance_id (key for INSERT)", "insurance_id"),
                ],
            ),
            text="Insurance",
        )

        # MEDICAL HISTORY
        nb.add(
            TableCrudFrame(
                nb,
                self.conn,
                title="Medical History",
                pk="history_id",
                pk_label="history_id",
                pk_hint="(key field; not shown in results table)",
                select_sql="""
SELECT
  (p.first_name || ' ' || p.last_name) AS patient_name,
  pmh.condition,
  pmh.diagnosis_date,
  pmh.notes
FROM public.patient_medical_history pmh
JOIN public.patient p ON p.patient_id = pmh.patient_id
ORDER BY p.last_name, p.first_name, pmh.diagnosis_date DESC;
""".strip(),
                insert_sql="""
INSERT INTO public.patient_medical_history (condition, diagnosis_date, notes, patient_id, history_id)
VALUES (%s,%s,%s,%s,%s);
""".strip(),
                update_sql="""
UPDATE public.patient_medical_history
SET condition=%s, diagnosis_date=%s, notes=%s, patient_id=%s
WHERE history_id=%s;
""".strip(),
                delete_sql="DELETE FROM public.patient_medical_history WHERE history_id=%s;",
                fields=[
                    ("condition", "condition"),
                    ("diagnosis_date (YYYY-MM-DD)", "diagnosis_date"),
                    ("notes", "notes"),
                    ("patient_id", "patient_id"),
                    ("history_id (key for INSERT)", "history_id"),
                ],
            ),
            text="Medical History",
        )

        # EMERGENCY CONTACTS
        nb.add(
            TableCrudFrame(
                nb,
                self.conn,
                title="Emergency Contacts",
                pk="contact_id",
                pk_label="contact_id",
                pk_hint="(key field; not shown in results table)",
                select_sql="""
SELECT
  (p.first_name || ' ' || p.last_name) AS patient_name,
  ec.name AS contact_name,
  ec.relationship,
  ec.phone
FROM public.emergency_contact ec
JOIN public.patient p ON p.patient_id = ec.patient_id
ORDER BY p.last_name, p.first_name, ec.name;
""".strip(),
                insert_sql="""
INSERT INTO public.emergency_contact (name, relationship, phone, patient_id, contact_id)
VALUES (%s,%s,%s,%s,%s);
""".strip(),
                update_sql="""
UPDATE public.emergency_contact
SET name=%s, relationship=%s, phone=%s, patient_id=%s
WHERE contact_id=%s;
""".strip(),
                delete_sql="DELETE FROM public.emergency_contact WHERE contact_id=%s;",
                fields=[
                    ("name", "name"),
                    ("relationship", "relationship"),
                    ("phone", "phone"),
                    ("patient_id", "patient_id"),
                    ("contact_id (key for INSERT)", "contact_id"),
                ],
            ),
            text="Emergency Contacts",
        )

        nb.add(QueriesAndProgramsFrame(nb, self.conn), text="Queries & Programs")


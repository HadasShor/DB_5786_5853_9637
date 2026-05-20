from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any, Callable, Optional

import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont

from psycopg2.extensions import connection as PGConnection

from .db import DbConfig, connect, execute, fetch_all, fetch_one
from tkinter import messagebox


class Palette:
    # Modern, colorful, high-contrast palette
    bg = "#0B1220"
    surface = "#0F1A2F"
    card = "#111C33"
    card2 = "#0D1730"
    border = "#1F2B47"
    text = "#EAF0FF"
    muted = "#A8B3CF"

    accent = "#6D5EF7"  # violet
    accent2 = "#22C55E"  # green
    warn = "#F59E0B"
    danger = "#EF4444"
    info = "#38BDF8"

    input_bg = "#0B142B"
    table_bg = "#0B142B"
    table_row = "#0E1933"
    table_row_alt = "#0B152D"


def _safe_int(s: str, default: int = 0) -> int:
    try:
        return int(s.strip())
    except Exception:
        return default


def _is_date(s: str) -> bool:
    if not s:
        return True
    return bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", s.strip()))


def _mk_icon(size: int, bg: str, fg: str, label: str) -> ctk.CTkImage:
    """
    Creates a crisp rounded-square icon with a letter.
    No external image files required.
    """
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    r = int(size * 0.28)
    d.rounded_rectangle((0, 0, size - 1, size - 1), radius=r, fill=bg)

    # Font: fall back safely if not available.
    try:
        font = ImageFont.truetype("seguiemj.ttf", int(size * 0.52))
    except Exception:
        try:
            font = ImageFont.truetype("segoeui.ttf", int(size * 0.52))
        except Exception:
            font = ImageFont.load_default()

    tw, th = d.textbbox((0, 0), label, font=font)[2:]
    d.text(((size - tw) / 2, (size - th) / 2 - 1), label, font=font, fill=fg)
    return ctk.CTkImage(light_image=img, dark_image=img, size=(size, size))


@dataclass(frozen=True)
class NavItem:
    key: str
    title: str
    icon: ctk.CTkImage
    builder: Callable[[ctk.CTkFrame], ctk.CTkFrame]


class ModernMedFlowApp(ctk.CTkFrame):
    def __init__(self, master: ctk.CTk) -> None:
        super().__init__(master, fg_color=Palette.bg)
        self.conn: Optional[PGConnection] = None

        self.icons = {
            "home": _mk_icon(34, Palette.accent, "white", "H"),
            "patients": _mk_icon(34, "#8B5CF6", "white", "P"),
            "admissions": _mk_icon(34, "#38BDF8", "white", "A"),
            "allergies": _mk_icon(34, Palette.warn, "white", "!"),
            "insurance": _mk_icon(34, Palette.accent2, "white", "I"),
            "history": _mk_icon(34, "#FB7185", "white", "M"),
            "contacts": _mk_icon(34, "#2DD4BF", "white", "C"),
            "queries": _mk_icon(34, "#F97316", "white", "Q"),
        }

        self._nav_buttons: dict[str, ctk.CTkButton] = {}
        self._content: Optional[ctk.CTkFrame] = None
        self._header_title: Optional[ctk.CTkLabel] = None
        self._header_sub: Optional[ctk.CTkLabel] = None

        self._render_login()

    def _clear(self) -> None:
        for w in self.winfo_children():
            w.destroy()

    def _render_login(self) -> None:
        self._clear()

        outer = ctk.CTkFrame(self, fg_color=Palette.bg)
        outer.pack(fill="both", expand=True, padx=22, pady=22)

        card = ctk.CTkFrame(outer, fg_color=Palette.surface, corner_radius=18, border_width=1, border_color=Palette.border)
        card.pack(expand=True)

        left = ctk.CTkFrame(card, fg_color=Palette.surface, corner_radius=18)
        left.grid(row=0, column=0, padx=(18, 10), pady=18, sticky="nsew")
        right = ctk.CTkFrame(card, fg_color=Palette.card, corner_radius=18, border_width=1, border_color=Palette.border)
        right.grid(row=0, column=1, padx=(10, 18), pady=18, sticky="nsew")

        card.columnconfigure(0, weight=1)
        card.columnconfigure(1, weight=1)

        ctk.CTkLabel(left, text="MedFlow", text_color=Palette.text, font=ctk.CTkFont(size=34, weight="bold")).pack(
            anchor="w"
        )
        ctk.CTkLabel(
            left,
            text="Step E • High‑end GUI",
            text_color=Palette.muted,
            font=ctk.CTkFont(size=14),
        ).pack(anchor="w", pady=(6, 0))
        ctk.CTkLabel(
            left,
            text="A modern interface for CRUD, queries,\nfunctions & procedures on PostgreSQL.",
            text_color=Palette.muted,
            font=ctk.CTkFont(size=16),
            justify="left",
        ).pack(anchor="w", pady=(16, 0))

        cfg = DbConfig.from_env()
        vars_ = {
            "host": ctk.StringVar(value=cfg.host),
            "port": ctk.StringVar(value=str(cfg.port)),
            "db": ctk.StringVar(value=cfg.database),
            "user": ctk.StringVar(value=cfg.user),
            "pass": ctk.StringVar(value=cfg.password),
        }

        def row(lbl: str, var: ctk.StringVar, show: bool = False) -> None:
            w = ctk.CTkFrame(right, fg_color="transparent")
            w.pack(fill="x", padx=16, pady=8)
            ctk.CTkLabel(w, text=lbl, text_color=Palette.muted, font=ctk.CTkFont(size=13, weight="bold")).pack(
                anchor="w"
            )
            ctk.CTkEntry(
                w,
                textvariable=var,
                fg_color=Palette.input_bg,
                border_color=Palette.border,
                text_color=Palette.text,
                height=44,
                corner_radius=12,
                show="*" if show else None,
            ).pack(fill="x", pady=(8, 0))

        ctk.CTkLabel(
            right, text="Database Login", text_color=Palette.text, font=ctk.CTkFont(size=22, weight="bold")
        ).pack(anchor="w", padx=16, pady=(16, 6))

        row("Host", vars_["host"])
        row("Port", vars_["port"])
        row("Database", vars_["db"])
        row("User", vars_["user"])
        row("Password", vars_["pass"], show=True)

        def do_connect() -> None:
            try:
                cfg2 = DbConfig(
                    host=vars_["host"].get().strip(),
                    port=_safe_int(vars_["port"].get(), 5432),
                    database=vars_["db"].get().strip(),
                    user=vars_["user"].get().strip(),
                    password=vars_["pass"].get(),
                )
                self.conn = connect(cfg2)
                self._render_shell()
            except Exception as e:
                messagebox.showerror("Connection failed", str(e))

        ctk.CTkButton(
            right,
            text="Connect",
            fg_color=Palette.accent,
            hover_color="#5B4EE0",
            height=46,
            corner_radius=14,
            font=ctk.CTkFont(size=16, weight="bold"),
            command=do_connect,
        ).pack(fill="x", padx=16, pady=(14, 16))

    def _render_shell(self) -> None:
        assert self.conn is not None
        self._clear()

        root = ctk.CTkFrame(self, fg_color=Palette.bg)
        root.pack(fill="both", expand=True)

        # Sidebar
        sidebar = ctk.CTkFrame(root, fg_color=Palette.surface, corner_radius=0, width=265)
        sidebar.pack(side="left", fill="y")

        header = ctk.CTkFrame(sidebar, fg_color="transparent")
        header.pack(fill="x", padx=18, pady=(18, 10))
        ctk.CTkLabel(header, text="MedFlow", text_color=Palette.text, font=ctk.CTkFont(size=22, weight="bold")).pack(
            anchor="w"
        )
        ctk.CTkLabel(
            header, text="Step E • GUI", text_color=Palette.muted, font=ctk.CTkFont(size=13)
        ).pack(anchor="w", pady=(2, 0))

        nav_host = ctk.CTkFrame(sidebar, fg_color="transparent")
        nav_host.pack(fill="both", expand=True, padx=12, pady=(8, 8))

        # Main area
        main = ctk.CTkFrame(root, fg_color=Palette.bg)
        main.pack(side="left", fill="both", expand=True)

        top = ctk.CTkFrame(main, fg_color=Palette.surface, corner_radius=18, border_width=1, border_color=Palette.border)
        top.pack(fill="x", padx=18, pady=(18, 10))
        self._header_title = ctk.CTkLabel(
            top, text="Dashboard", text_color=Palette.text, font=ctk.CTkFont(size=26, weight="bold")
        )
        self._header_title.pack(anchor="w", padx=16, pady=(14, 0))
        self._header_sub = ctk.CTkLabel(
            top,
            text="Professional UI • Bigger fonts • Colorful cards • Icons • Clean layout",
            text_color=Palette.muted,
            font=ctk.CTkFont(size=14),
        )
        self._header_sub.pack(anchor="w", padx=16, pady=(6, 14))

        content = ctk.CTkFrame(main, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=18, pady=(0, 18))
        self._content = content

        # Builders
        nav_items: list[NavItem] = [
            NavItem("home", "Dashboard", self.icons["home"], lambda host: self._build_dashboard(host)),
            NavItem("patients", "Patients", self.icons["patients"], lambda host: self._build_patients(host)),
            NavItem("admissions", "Admissions", self.icons["admissions"], lambda host: self._build_admissions(host)),
            NavItem("allergies", "Allergies", self.icons["allergies"], lambda host: self._build_allergies(host)),
            NavItem("insurance", "Insurance", self.icons["insurance"], lambda host: self._build_insurance(host)),
            NavItem("history", "Medical History", self.icons["history"], lambda host: self._build_history(host)),
            NavItem("contacts", "Emergency Contacts", self.icons["contacts"], lambda host: self._build_contacts(host)),
            NavItem("queries", "Queries & Programs", self.icons["queries"], lambda host: self._build_queries(host)),
        ]

        def show(item: NavItem) -> None:
            assert self._content is not None
            for w in self._content.winfo_children():
                w.destroy()
            frame = item.builder(self._content)
            frame.pack(fill="both", expand=True)
            for k, b in self._nav_buttons.items():
                if k == item.key:
                    b.configure(fg_color=Palette.accent, hover_color=Palette.accent, text_color="white")
                else:
                    b.configure(fg_color="transparent", hover_color=Palette.card2, text_color=Palette.text)
            if self._header_title:
                self._header_title.configure(text=item.title)

        for item in nav_items:
            btn = ctk.CTkButton(
                nav_host,
                text=item.title,
                image=item.icon,
                compound="left",
                fg_color="transparent",
                hover_color=Palette.card2,
                text_color=Palette.text,
                height=44,
                corner_radius=14,
                anchor="w",
                font=ctk.CTkFont(size=15, weight="bold"),
                command=lambda it=item: show(it),
            )
            btn.pack(fill="x", pady=6)
            self._nav_buttons[item.key] = btn

        ctk.CTkButton(
            sidebar,
            text="Logout",
            fg_color=Palette.danger,
            hover_color="#DC2626",
            height=42,
            corner_radius=14,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self._render_login,
        ).pack(fill="x", padx=18, pady=(8, 18))

        show(nav_items[0])

    # ---------- Screens ----------
    def _card(self, master: ctk.CTkFrame, title: str, subtitle: str) -> ctk.CTkFrame:
        c = ctk.CTkFrame(master, fg_color=Palette.surface, corner_radius=18, border_width=1, border_color=Palette.border)
        ctk.CTkLabel(c, text=title, text_color=Palette.text, font=ctk.CTkFont(size=18, weight="bold")).pack(
            anchor="w", padx=16, pady=(14, 0)
        )
        ctk.CTkLabel(c, text=subtitle, text_color=Palette.muted, font=ctk.CTkFont(size=13)).pack(
            anchor="w", padx=16, pady=(6, 14)
        )
        return c

    def _build_dashboard(self, host: ctk.CTkFrame) -> ctk.CTkFrame:
        assert self.conn is not None
        grid = ctk.CTkFrame(host, fg_color="transparent")
        grid.columnconfigure((0, 1, 2), weight=1, uniform="col")

        stats = [
            ("Patients", "Total patients in system", "SELECT COUNT(*) AS c FROM public.patient;", Palette.accent),
            ("Admissions", "Total admissions", "SELECT COUNT(*) AS c FROM public.admission;", Palette.info),
            ("Severe allergies", "Allergies marked Severe", "SELECT COUNT(*) AS c FROM public.patient_allergy WHERE severity='Severe';", Palette.warn),
        ]

        for i, (t, sub, sql, color) in enumerate(stats):
            try:
                row = fetch_one(self.conn, sql) or {"c": 0}
                val = str(row.get("c", 0))
            except Exception:
                val = "—"

            card = ctk.CTkFrame(grid, fg_color=Palette.surface, corner_radius=18, border_width=1, border_color=Palette.border)
            card.grid(row=0, column=i, sticky="nsew", padx=(0 if i == 0 else 10, 0), pady=(0, 10))
            ctk.CTkLabel(card, text=t, text_color=Palette.muted, font=ctk.CTkFont(size=13, weight="bold")).pack(
                anchor="w", padx=16, pady=(14, 0)
            )
            ctk.CTkLabel(card, text=val, text_color=Palette.text, font=ctk.CTkFont(size=34, weight="bold")).pack(
                anchor="w", padx=16, pady=(8, 0)
            )
            ctk.CTkLabel(card, text=sub, text_color=color, font=ctk.CTkFont(size=13, weight="bold")).pack(
                anchor="w", padx=16, pady=(10, 16)
            )

        note = self._card(
            grid,
            "How updates work (requirement)",
            "Enter key → Fetch → edit fields → Update. Results hide IDs; FK shown as names using JOINs.",
        )
        note.grid(row=1, column=0, columnspan=3, sticky="nsew")
        return grid

    # The CRUD screens in this first modern pass focus on:
    # - big fonts
    # - clean cards
    # - requirement for update-by-key via fetch
    # For brevity, each screen includes a "Quick view" + a compact CRUD form.
    def _build_generic_crud(
        self,
        host: ctk.CTkFrame,
        title: str,
        view_sql: str,
        pk_name: str,
        fetch_sql: str,
        insert_sql: str,
        update_sql: str,
        delete_sql: str,
        fields: list[tuple[str, str, str]],  # (label, key, placeholder)
    ) -> ctk.CTkFrame:
        assert self.conn is not None
        root = ctk.CTkFrame(host, fg_color="transparent")
        root.columnconfigure(0, weight=1)
        root.columnconfigure(1, weight=0)
        root.rowconfigure(1, weight=1)

        left = ctk.CTkFrame(root, fg_color=Palette.surface, corner_radius=18, border_width=1, border_color=Palette.border)
        left.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))
        ctk.CTkLabel(left, text="Quick view", text_color=Palette.text, font=ctk.CTkFont(size=16, weight="bold")).pack(
            anchor="w", padx=16, pady=(14, 0)
        )
        ctk.CTkLabel(
            left,
            text="(IDs hidden; joined values shown)",
            text_color=Palette.muted,
            font=ctk.CTkFont(size=12),
        ).pack(anchor="w", padx=16, pady=(6, 10))

        textbox = ctk.CTkTextbox(left, fg_color=Palette.table_bg, text_color=Palette.text, corner_radius=14)
        textbox.pack(fill="both", expand=True, padx=16, pady=(0, 16))

        def refresh_view() -> None:
            try:
                rows = fetch_all(self.conn, view_sql)
                textbox.configure(state="normal")
                textbox.delete("1.0", "end")
                if not rows:
                    textbox.insert("end", "(no rows)")
                else:
                    cols = list(rows[0].keys())
                    # pretty fixed-width table text
                    widths = {c: max(len(c), *(len(str(r.get(c, ""))) for r in rows[:50])) for c in cols}
                    header = " | ".join(c.ljust(widths[c]) for c in cols)
                    sep = "-+-".join("-" * widths[c] for c in cols)
                    body = "\n".join(" | ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols) for r in rows[:50])
                    textbox.insert("end", header + "\n" + sep + "\n" + body)
                textbox.configure(state="disabled")
            except Exception as e:
                textbox.configure(state="normal")
                textbox.delete("1.0", "end")
                textbox.insert("end", f"ERROR:\n{e}")
                textbox.configure(state="disabled")

        right = ctk.CTkFrame(root, fg_color="transparent")
        right.grid(row=0, column=1, sticky="new")

        form = ctk.CTkFrame(right, fg_color=Palette.surface, corner_radius=18, border_width=1, border_color=Palette.border)
        form.pack(fill="x")

        ctk.CTkLabel(form, text=f"{title} • CRUD", text_color=Palette.text, font=ctk.CTkFont(size=16, weight="bold")).pack(
            anchor="w", padx=16, pady=(14, 0)
        )
        ctk.CTkLabel(
            form,
            text=f"Update/Delete uses key: {pk_name}",
            text_color=Palette.muted,
            font=ctk.CTkFont(size=12),
        ).pack(anchor="w", padx=16, pady=(6, 12))

        pk_var = ctk.StringVar(value="")
        pk_entry = ctk.CTkEntry(
            form,
            textvariable=pk_var,
            fg_color=Palette.input_bg,
            border_color=Palette.border,
            text_color=Palette.text,
            height=40,
            corner_radius=12,
            placeholder_text=f"{pk_name} (for fetch/update/delete)",
        )
        pk_entry.pack(fill="x", padx=16, pady=(0, 10))

        vars_: dict[str, ctk.StringVar] = {k: ctk.StringVar(value="") for _, k, _ in fields}

        for lbl, k, ph in fields:
            ctk.CTkLabel(form, text=lbl, text_color=Palette.muted, font=ctk.CTkFont(size=12, weight="bold")).pack(
                anchor="w", padx=16, pady=(8, 0)
            )
            ctk.CTkEntry(
                form,
                textvariable=vars_[k],
                fg_color=Palette.input_bg,
                border_color=Palette.border,
                text_color=Palette.text,
                height=40,
                corner_radius=12,
                placeholder_text=ph,
            ).pack(fill="x", padx=16, pady=(6, 0))

        def fetch_by_key() -> None:
            key = pk_var.get().strip()
            if not key:
                messagebox.showwarning("Missing key", f"Please enter {pk_name}.")
                return
            row = fetch_one(self.conn, fetch_sql, (key,))
            if not row:
                messagebox.showinfo("Not found", "No row found for that key.")
                return
            for _, k, _ in fields:
                if k in row:
                    vars_[k].set("" if row[k] is None else str(row[k]))

        def insert() -> None:
            vals = [vars_[k].get().strip() or None for _, k, _ in fields]
            execute(self.conn, insert_sql, vals)
            refresh_view()

        def update() -> None:
            key = pk_var.get().strip()
            if not key:
                messagebox.showwarning("Missing key", f"Please enter {pk_name}.")
                return
            vals = [vars_[k].get().strip() or None for _, k, _ in fields] + [key]
            execute(self.conn, update_sql, vals)
            refresh_view()

        def delete() -> None:
            key = pk_var.get().strip()
            if not key:
                messagebox.showwarning("Missing key", f"Please enter {pk_name}.")
                return
            if not messagebox.askyesno("Confirm delete", "Delete this record?"):
                return
            execute(self.conn, delete_sql, (key,))
            refresh_view()

        actions = ctk.CTkFrame(form, fg_color="transparent")
        actions.pack(fill="x", padx=16, pady=(14, 16))

        ctk.CTkButton(
            actions,
            text="Refresh",
            fg_color=Palette.info,
            hover_color="#0EA5E9",
            corner_radius=12,
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=refresh_view,
        ).grid(row=0, column=0, sticky="ew", padx=(0, 8))
        ctk.CTkButton(
            actions,
            text="Fetch",
            fg_color=Palette.accent,
            hover_color="#5B4EE0",
            corner_radius=12,
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=fetch_by_key,
        ).grid(row=0, column=1, sticky="ew", padx=(0, 8))
        ctk.CTkButton(
            actions,
            text="Insert",
            fg_color=Palette.accent2,
            hover_color="#16A34A",
            corner_radius=12,
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=insert,
        ).grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(8, 0))
        ctk.CTkButton(
            actions,
            text="Update",
            fg_color=Palette.warn,
            hover_color="#D97706",
            corner_radius=12,
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=update,
        ).grid(row=1, column=1, sticky="ew", padx=(0, 8), pady=(8, 0))
        ctk.CTkButton(
            actions,
            text="Delete",
            fg_color=Palette.danger,
            hover_color="#DC2626",
            corner_radius=12,
            height=42,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=delete,
        ).grid(row=2, column=0, columnspan=2, sticky="ew", pady=(8, 0))

        actions.columnconfigure((0, 1), weight=1)
        refresh_view()
        return root

    def _build_patients(self, host: ctk.CTkFrame) -> ctk.CTkFrame:
        return self._build_generic_crud(
            host,
            "Patients",
            view_sql="""
SELECT first_name, last_name, date_of_birth, gender, phone, email, address
FROM public.patient
ORDER BY last_name, first_name;
""".strip(),
            pk_name="patient_id",
            fetch_sql="SELECT * FROM public.patient WHERE patient_id=%s",
            insert_sql="""
INSERT INTO public.patient (first_name,last_name,date_of_birth,gender,phone,email,address,patient_id)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
""".strip(),
            update_sql="""
UPDATE public.patient
SET first_name=%s,last_name=%s,date_of_birth=%s,gender=%s,phone=%s,email=%s,address=%s,patient_id=%s
WHERE patient_id=%s;
""".strip(),
            delete_sql="DELETE FROM public.patient WHERE patient_id=%s",
            fields=[
                ("first_name", "first_name", "e.g. Dana"),
                ("last_name", "last_name", "e.g. Cohen"),
                ("date_of_birth", "date_of_birth", "YYYY-MM-DD"),
                ("gender", "gender", "Male / Female / Other"),
                ("phone", "phone", "e.g. 050-1234567"),
                ("email", "email", "optional"),
                ("address", "address", "optional"),
                ("patient_id", "patient_id", "numeric key"),
            ],
        )

    def _build_admissions(self, host: ctk.CTkFrame) -> ctk.CTkFrame:
        return self._build_generic_crud(
            host,
            "Admissions",
            view_sql="""
SELECT (p.first_name || ' ' || p.last_name) AS patient_name,
       a.admission_date, a.discharge_date, a.admission_type, a.reason
FROM public.admission a
JOIN public.patient p ON p.patient_id=a.patient_id
ORDER BY a.admission_date DESC;
""".strip(),
            pk_name="admission_id",
            fetch_sql="SELECT * FROM public.admission WHERE admission_id=%s",
            insert_sql="""
INSERT INTO public.admission (admission_date,discharge_date,admission_type,reason,patient_id,admission_id)
VALUES (%s,%s,%s,%s,%s,%s);
""".strip(),
            update_sql="""
UPDATE public.admission
SET admission_date=%s,discharge_date=%s,admission_type=%s,reason=%s,patient_id=%s,admission_id=%s
WHERE admission_id=%s;
""".strip(),
            delete_sql="DELETE FROM public.admission WHERE admission_id=%s",
            fields=[
                ("admission_date", "admission_date", "YYYY-MM-DD"),
                ("discharge_date", "discharge_date", "YYYY-MM-DD or empty"),
                ("admission_type", "admission_type", "Emergency / Elective / Urgent"),
                ("reason", "reason", "optional"),
                ("patient_id", "patient_id", "numeric key"),
                ("admission_id", "admission_id", "numeric key"),
            ],
        )

    def _build_allergies(self, host: ctk.CTkFrame) -> ctk.CTkFrame:
        return self._build_generic_crud(
            host,
            "Allergies",
            view_sql="""
SELECT (p.first_name || ' ' || p.last_name) AS patient_name,
       pa.allergy_name, pa.severity, pa.notes
FROM public.patient_allergy pa
JOIN public.patient p ON p.patient_id=pa.patient_id
ORDER BY p.last_name, p.first_name, pa.allergy_name;
""".strip(),
            pk_name="allergy_id",
            fetch_sql="SELECT * FROM public.patient_allergy WHERE allergy_id=%s",
            insert_sql="""
INSERT INTO public.patient_allergy (allergy_name,severity,notes,patient_id,allergy_id)
VALUES (%s,%s,%s,%s,%s);
""".strip(),
            update_sql="""
UPDATE public.patient_allergy
SET allergy_name=%s,severity=%s,notes=%s,patient_id=%s,allergy_id=%s
WHERE allergy_id=%s;
""".strip(),
            delete_sql="DELETE FROM public.patient_allergy WHERE allergy_id=%s",
            fields=[
                ("allergy_name", "allergy_name", "e.g. Penicillin"),
                ("severity", "severity", "Mild / Moderate / Severe / Unknown"),
                ("notes", "notes", "optional"),
                ("patient_id", "patient_id", "numeric key"),
                ("allergy_id", "allergy_id", "numeric key"),
            ],
        )

    def _build_insurance(self, host: ctk.CTkFrame) -> ctk.CTkFrame:
        return self._build_generic_crud(
            host,
            "Insurance",
            view_sql="""
SELECT (p.first_name || ' ' || p.last_name) AS patient_name,
       pi.provider_name, pi.policy_number, pi.coverage_type, pi.expiration_date
FROM public.patient_insurance pi
JOIN public.patient p ON p.patient_id=pi.patient_id
ORDER BY p.last_name, p.first_name;
""".strip(),
            pk_name="insurance_id",
            fetch_sql="SELECT * FROM public.patient_insurance WHERE insurance_id=%s",
            insert_sql="""
INSERT INTO public.patient_insurance (provider_name,policy_number,coverage_type,expiration_date,patient_id,insurance_id)
VALUES (%s,%s,%s,%s,%s,%s);
""".strip(),
            update_sql="""
UPDATE public.patient_insurance
SET provider_name=%s,policy_number=%s,coverage_type=%s,expiration_date=%s,patient_id=%s,insurance_id=%s
WHERE insurance_id=%s;
""".strip(),
            delete_sql="DELETE FROM public.patient_insurance WHERE insurance_id=%s",
            fields=[
                ("provider_name", "provider_name", "e.g. Maccabi"),
                ("policy_number", "policy_number", "e.g. POL-123"),
                ("coverage_type", "coverage_type", "optional"),
                ("expiration_date", "expiration_date", "YYYY-MM-DD"),
                ("patient_id", "patient_id", "numeric key"),
                ("insurance_id", "insurance_id", "numeric key"),
            ],
        )

    def _build_history(self, host: ctk.CTkFrame) -> ctk.CTkFrame:
        return self._build_generic_crud(
            host,
            "Medical History",
            view_sql="""
SELECT (p.first_name || ' ' || p.last_name) AS patient_name,
       pmh.condition, pmh.diagnosis_date, pmh.notes
FROM public.patient_medical_history pmh
JOIN public.patient p ON p.patient_id=pmh.patient_id
ORDER BY p.last_name, p.first_name, pmh.diagnosis_date DESC;
""".strip(),
            pk_name="history_id",
            fetch_sql="SELECT * FROM public.patient_medical_history WHERE history_id=%s",
            insert_sql="""
INSERT INTO public.patient_medical_history (condition,diagnosis_date,notes,patient_id,history_id)
VALUES (%s,%s,%s,%s,%s);
""".strip(),
            update_sql="""
UPDATE public.patient_medical_history
SET condition=%s,diagnosis_date=%s,notes=%s,patient_id=%s,history_id=%s
WHERE history_id=%s;
""".strip(),
            delete_sql="DELETE FROM public.patient_medical_history WHERE history_id=%s",
            fields=[
                ("condition", "condition", "e.g. Chronic condition"),
                ("diagnosis_date", "diagnosis_date", "YYYY-MM-DD"),
                ("notes", "notes", "optional"),
                ("patient_id", "patient_id", "numeric key"),
                ("history_id", "history_id", "numeric key"),
            ],
        )

    def _build_contacts(self, host: ctk.CTkFrame) -> ctk.CTkFrame:
        return self._build_generic_crud(
            host,
            "Emergency Contacts",
            view_sql="""
SELECT (p.first_name || ' ' || p.last_name) AS patient_name,
       ec.name AS contact_name, ec.relationship, ec.phone
FROM public.emergency_contact ec
JOIN public.patient p ON p.patient_id=ec.patient_id
ORDER BY p.last_name, p.first_name, ec.name;
""".strip(),
            pk_name="contact_id",
            fetch_sql="SELECT * FROM public.emergency_contact WHERE contact_id=%s",
            insert_sql="""
INSERT INTO public.emergency_contact (name,relationship,phone,patient_id,contact_id)
VALUES (%s,%s,%s,%s,%s);
""".strip(),
            update_sql="""
UPDATE public.emergency_contact
SET name=%s,relationship=%s,phone=%s,patient_id=%s,contact_id=%s
WHERE contact_id=%s;
""".strip(),
            delete_sql="DELETE FROM public.emergency_contact WHERE contact_id=%s",
            fields=[
                ("name", "name", "e.g. Avi Cohen"),
                ("relationship", "relationship", "e.g. Parent"),
                ("phone", "phone", "e.g. 050-1234567"),
                ("patient_id", "patient_id", "numeric key"),
                ("contact_id", "contact_id", "numeric key"),
            ],
        )

    def _build_queries(self, host: ctk.CTkFrame) -> ctk.CTkFrame:
        assert self.conn is not None
        root = ctk.CTkFrame(host, fg_color="transparent")
        root.columnconfigure(0, weight=0)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)

        left = ctk.CTkFrame(root, fg_color=Palette.surface, corner_radius=18, border_width=1, border_color=Palette.border)
        left.grid(row=0, column=0, sticky="nsw", padx=(0, 10))
        ctk.CTkLabel(left, text="Actions", text_color=Palette.text, font=ctk.CTkFont(size=16, weight="bold")).pack(
            anchor="w", padx=16, pady=(14, 0)
        )
        ctk.CTkLabel(
            left,
            text="Step B queries + Step D programs",
            text_color=Palette.muted,
            font=ctk.CTkFont(size=12),
        ).pack(anchor="w", padx=16, pady=(6, 12))

        out = ctk.CTkTextbox(root, fg_color=Palette.table_bg, text_color=Palette.text, corner_radius=18)
        out.grid(row=0, column=1, sticky="nsew")

        def show_rows(title: str, rows: list[dict[str, Any]]) -> None:
            out.configure(state="normal")
            out.delete("1.0", "end")
            out.insert("end", title + "\n\n")
            if not rows:
                out.insert("end", "(no rows)")
            else:
                cols = list(rows[0].keys())
                widths = {c: max(len(c), *(len(str(r.get(c, ""))) for r in rows[:80])) for c in cols}
                header = " | ".join(c.ljust(widths[c]) for c in cols)
                sep = "-+-".join("-" * widths[c] for c in cols)
                body = "\n".join(" | ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols) for r in rows[:80])
                out.insert("end", header + "\n" + sep + "\n" + body)
            out.configure(state="disabled")

        def q1() -> None:
            sql = """
SELECT DISTINCT p.first_name, p.last_name, p.email
FROM public.patient p
JOIN public.admission a ON p.patient_id = a.patient_id
WHERE EXTRACT(YEAR FROM a.admission_date) = 2024
ORDER BY p.last_name;
""".strip()
            show_rows("Query 1: Admissions in 2024", fetch_all(self.conn, sql))

        def q2() -> None:
            sql = """
SELECT EXTRACT(YEAR FROM admission_date) as year_part, COUNT(*) as total_admissions
FROM public.admission
WHERE patient_id IN (SELECT patient_id FROM public.patient_allergy WHERE severity = 'Severe')
GROUP BY EXTRACT(YEAR FROM admission_date)
ORDER BY year_part DESC;
""".strip()
            show_rows("Query 2: Severe-allergy admissions per year", fetch_all(self.conn, sql))

        pid_var = ctk.StringVar(value="42001")
        days_var = ctk.StringVar(value="60")

        def run_risk() -> None:
            sql = "SELECT public.fn_patient_risk_score(%s) AS risk_score;"
            show_rows("Step D: fn_patient_risk_score", fetch_all(self.conn, sql, (pid_var.get().strip(),)))

        def call_close() -> None:
            sql = "CALL public.sp_close_long_open_admissions(%s);"
            execute(self.conn, sql, (days_var.get().strip(),))
            show_rows("Step D: sp_close_long_open_admissions", [{"status": "OK"}])

        def action_btn(text: str, color: str, cmd: Callable[[], None]) -> None:
            ctk.CTkButton(
                left,
                text=text,
                fg_color=color,
                hover_color=color,
                height=42,
                corner_radius=14,
                font=ctk.CTkFont(size=14, weight="bold"),
                command=cmd,
            ).pack(fill="x", padx=16, pady=8)

        action_btn("Run Query 1", Palette.accent, q1)
        action_btn("Run Query 2", Palette.accent, q2)

        ctk.CTkLabel(left, text="patient_id", text_color=Palette.muted, font=ctk.CTkFont(size=12, weight="bold")).pack(
            anchor="w", padx=16, pady=(10, 0)
        )
        ctk.CTkEntry(left, textvariable=pid_var, fg_color=Palette.input_bg, border_color=Palette.border, height=40, corner_radius=12).pack(
            fill="x", padx=16, pady=(6, 0)
        )
        action_btn("Run fn_patient_risk_score", Palette.accent2, run_risk)

        ctk.CTkLabel(left, text="days", text_color=Palette.muted, font=ctk.CTkFont(size=12, weight="bold")).pack(
            anchor="w", padx=16, pady=(10, 0)
        )
        ctk.CTkEntry(left, textvariable=days_var, fg_color=Palette.input_bg, border_color=Palette.border, height=40, corner_radius=12).pack(
            fill="x", padx=16, pady=(6, 0)
        )
        action_btn("Call sp_close_long_open_admissions", Palette.warn, call_close)

        out.configure(state="disabled")
        return root


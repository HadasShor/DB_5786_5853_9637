# from __future__ import annotations

# import tkinter as tk
# from tkinter import messagebox, ttk
# from typing import Any, Callable, Optional

# from psycopg2.extensions import connection as PGConnection

# from .db import DbConfig, connect, execute, fetch_all, fetch_one


# class AppTheme:
#     # Colorful + clean palette (light sidebar, strong accent)
#     bg = "#F4F7FF"
#     card = "#FFFFFF"
#     border = "#D7E0F2"
#     text = "#0B1220"
#     muted = "#475569"

#     primary = "#2563EB"  # blue
#     primary_dark = "#1E40AF"
#     success = "#16A34A"  # green
#     danger = "#DC2626"  # red
#     warn = "#D97706"  # amber

#     zebra_1 = "#FFFFFF"
#     zebra_2 = "#F3F6FF"

#     # Sidebar (light)
#     sidebar_bg = "#FFFFFF"
#     sidebar_card = "#F3F6FF"
#     sidebar_text = "#0B1220"
#     sidebar_muted = "#64748B"
#     sidebar_active = "#2563EB"
#     sidebar_active_text = "#FFFFFF"


# def apply_theme(root: tk.Tk) -> ttk.Style:
#     style = ttk.Style(root)
#     try:
#         style.theme_use("clam")
#     except Exception:
#         pass

#     root.configure(bg=AppTheme.bg)

#     # Base
#     style.configure(".", font=("Segoe UI", 11))
#     style.configure("TFrame", background=AppTheme.bg)
#     style.configure("Card.TFrame", background=AppTheme.card, relief="flat")
#     style.configure("TLabel", background=AppTheme.bg, foreground=AppTheme.text)
#     style.configure("Muted.TLabel", foreground=AppTheme.muted)
#     style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"), foreground=AppTheme.text)
#     style.configure("H1.TLabel", font=("Segoe UI", 16, "bold"), foreground=AppTheme.text)
#     style.configure("H2.TLabel", font=("Segoe UI", 12, "bold"), foreground=AppTheme.text)
#     style.configure("Big.TLabel", font=("Segoe UI", 13), foreground=AppTheme.text)

#     # Labelframe
#     style.configure(
#         "TLabelframe",
#         background=AppTheme.bg,
#         bordercolor=AppTheme.border,
#         relief="solid",
#     )
#     style.configure(
#         "TLabelframe.Label",
#         background=AppTheme.bg,
#         foreground=AppTheme.muted,
#         font=("Segoe UI", 11, "bold"),
#     )

#     # Buttons
#     style.configure("TButton", padding=(14, 10))
#     style.configure("Primary.TButton", background=AppTheme.primary, foreground="white", padding=(16, 10))
#     style.map(
#         "Primary.TButton",
#         background=[("active", AppTheme.primary_dark), ("pressed", AppTheme.primary_dark)],
#         foreground=[("disabled", "#E2E8F0")],
#     )
#     style.configure("Success.TButton", background=AppTheme.success, foreground="white")
#     style.map("Success.TButton", background=[("active", "#15803D")])
#     style.configure("Danger.TButton", background=AppTheme.danger, foreground="white")
#     style.map("Danger.TButton", background=[("active", "#B91C1C")])
#     style.configure("Warn.TButton", background=AppTheme.warn, foreground="white")
#     style.map("Warn.TButton", background=[("active", "#B45309")])

#     # Sidebar
#     style.configure("Sidebar.TFrame", background=AppTheme.sidebar_bg)
#     style.configure("SidebarCard.TFrame", background=AppTheme.sidebar_card)
#     style.configure("Sidebar.TLabel", background=AppTheme.sidebar_bg, foreground=AppTheme.sidebar_text)
#     style.configure("SidebarMuted.TLabel", background=AppTheme.sidebar_bg, foreground=AppTheme.sidebar_muted)
#     style.configure(
#         "SidebarTitle.TLabel",
#         background=AppTheme.sidebar_bg,
#         foreground=AppTheme.sidebar_text,
#         font=("Segoe UI", 18, "bold"),
#     )
#     style.configure(
#         "Nav.TButton",
#         background=AppTheme.sidebar_card,
#         foreground=AppTheme.sidebar_text,
#         padding=(14, 10),
#         anchor="w",
#     )
#     style.map(
#         "Nav.TButton",
#         background=[("active", "#E7EEFF"), ("pressed", "#E7EEFF")],
#     )
#     style.configure(
#         "NavActive.TButton",
#         background=AppTheme.sidebar_active,
#         foreground=AppTheme.sidebar_active_text,
#         padding=(14, 10),
#         anchor="w",
#     )
#     style.map("NavActive.TButton", background=[("active", AppTheme.sidebar_active), ("pressed", AppTheme.sidebar_active)])

#     # Entries
#     style.configure("TEntry", padding=(10, 8))

#     # Notebook tabs
#     style.configure("TNotebook", background=AppTheme.bg, borderwidth=0)
#     style.configure(
#         "TNotebook.Tab",
#         padding=(14, 8),
#         background="#E9EEFA",
#         foreground=AppTheme.text,
#     )
#     style.map(
#         "TNotebook.Tab",
#         background=[("selected", AppTheme.card), ("active", "#DDE6FF")],
#     )

#     # Treeview
#     style.configure(
#         "Treeview",
#         background=AppTheme.card,
#         fieldbackground=AppTheme.card,
#         foreground=AppTheme.text,
#         rowheight=30,
#         bordercolor=AppTheme.border,
#         lightcolor=AppTheme.border,
#         darkcolor=AppTheme.border,
#     )
#     style.configure(
#         "Treeview.Heading",
#         font=("Segoe UI", 11, "bold"),
#         background="#E9EEFA",
#         foreground=AppTheme.text,
#         padding=(8, 6),
#     )
#     style.map("Treeview.Heading", background=[("active", "#DDE6FF")])

#     return style


# class IconFactory:
#     """
#     Creates small colorful icons using Tk PhotoImage (no external files needed).
#     """

#     size = 20

#     @staticmethod
#     def _new(bg: str = "#00000000") -> tk.PhotoImage:
#         img = tk.PhotoImage(width=IconFactory.size, height=IconFactory.size)
#         # Transparent-ish background: Tk doesn't do alpha well everywhere; use bg matching card/sidebar.
#         img.put(bg, to=(0, 0, IconFactory.size, IconFactory.size))
#         return img

#     @staticmethod
#     def _rect(img: tk.PhotoImage, x0: int, y0: int, x1: int, y1: int, color: str) -> None:
#         img.put(color, to=(x0, y0, x1, y1))

#     @staticmethod
#     def _line(img: tk.PhotoImage, x0: int, y0: int, x1: int, y1: int, color: str, w: int = 1) -> None:
#         if x0 == x1:
#             for dx in range(w):
#                 IconFactory._rect(img, x0 + dx, min(y0, y1), x1 + dx + 1, max(y0, y1) + 1, color)
#             return
#         if y0 == y1:
#             for dy in range(w):
#                 IconFactory._rect(img, min(x0, x1), y0 + dy, max(x0, x1) + 1, y1 + dy + 1, color)
#             return
#         # simple diagonal
#         steps = max(abs(x1 - x0), abs(y1 - y0))
#         for i in range(steps + 1):
#             x = int(x0 + (x1 - x0) * i / steps)
#             y = int(y0 + (y1 - y0) * i / steps)
#             IconFactory._rect(img, x, y, x + w, y + w, color)

#     @staticmethod
#     def _circle(img: tk.PhotoImage, cx: int, cy: int, r: int, color: str) -> None:
#         for y in range(cy - r, cy + r + 1):
#             for x in range(cx - r, cx + r + 1):
#                 if 0 <= x < IconFactory.size and 0 <= y < IconFactory.size:
#                     if (x - cx) * (x - cx) + (y - cy) * (y - cy) <= r * r:
#                         img.put(color, (x, y))

#     @staticmethod
#     def home(bg: str) -> tk.PhotoImage:
#         img = IconFactory._new(bg)
#         IconFactory._rect(img, 4, 9, 16, 17, AppTheme.primary)
#         IconFactory._line(img, 4, 10, 10, 4, AppTheme.primary_dark, 2)
#         IconFactory._line(img, 10, 4, 16, 10, AppTheme.primary_dark, 2)
#         IconFactory._rect(img, 9, 13, 11, 17, "#FFFFFF")
#         return img

#     @staticmethod
#     def users(bg: str) -> tk.PhotoImage:
#         img = IconFactory._new(bg)
#         IconFactory._circle(img, 8, 8, 4, "#7C3AED")  # purple
#         IconFactory._circle(img, 14, 9, 3, "#A78BFA")
#         IconFactory._rect(img, 4, 13, 12, 18, "#7C3AED")
#         IconFactory._rect(img, 11, 13, 18, 18, "#A78BFA")
#         return img

#     @staticmethod
#     def calendar(bg: str) -> tk.PhotoImage:
#         img = IconFactory._new(bg)
#         IconFactory._rect(img, 4, 6, 16, 17, "#0EA5E9")  # sky
#         IconFactory._rect(img, 4, 6, 16, 9, "#0369A1")
#         IconFactory._rect(img, 6, 4, 8, 7, "#0369A1")
#         IconFactory._rect(img, 12, 4, 14, 7, "#0369A1")
#         IconFactory._rect(img, 6, 11, 8, 13, "#FFFFFF")
#         IconFactory._rect(img, 10, 11, 12, 13, "#FFFFFF")
#         IconFactory._rect(img, 12, 14, 14, 16, "#FFFFFF")
#         return img

#     @staticmethod
#     def alert(bg: str) -> tk.PhotoImage:
#         img = IconFactory._new(bg)
#         IconFactory._circle(img, 10, 10, 8, "#F59E0B")  # amber
#         IconFactory._rect(img, 9, 5, 11, 12, "#FFFFFF")
#         IconFactory._rect(img, 9, 14, 11, 16, "#FFFFFF")
#         return img

#     @staticmethod
#     def shield(bg: str) -> tk.PhotoImage:
#         img = IconFactory._new(bg)
#         IconFactory._rect(img, 6, 4, 14, 6, "#16A34A")
#         IconFactory._rect(img, 5, 6, 15, 15, "#22C55E")
#         IconFactory._line(img, 7, 10, 9, 12, "#FFFFFF", 2)
#         IconFactory._line(img, 9, 12, 13, 8, "#FFFFFF", 2)
#         return img

#     @staticmethod
#     def phone(bg: str) -> tk.PhotoImage:
#         img = IconFactory._new(bg)
#         IconFactory._rect(img, 6, 4, 14, 17, "#0F766E")
#         IconFactory._rect(img, 7, 6, 13, 13, "#CCFBF1")
#         IconFactory._rect(img, 9, 14, 11, 15, "#CCFBF1")
#         return img

#     @staticmethod
#     def doc(bg: str) -> tk.PhotoImage:
#         img = IconFactory._new(bg)
#         IconFactory._rect(img, 6, 4, 15, 17, "#EF4444")
#         IconFactory._rect(img, 8, 7, 13, 8, "#FFFFFF")
#         IconFactory._rect(img, 8, 10, 13, 11, "#FFFFFF")
#         IconFactory._rect(img, 8, 13, 12, 14, "#FFFFFF")
#         return img

#     @staticmethod
#     def play(bg: str) -> tk.PhotoImage:
#         img = IconFactory._new(bg)
#         IconFactory._circle(img, 10, 10, 9, "#111827")
#         IconFactory._line(img, 8, 6, 8, 14, "#FFFFFF", 2)
#         IconFactory._line(img, 8, 6, 14, 10, "#FFFFFF", 2)
#         IconFactory._line(img, 8, 14, 14, 10, "#FFFFFF", 2)
#         return img

#     @staticmethod
#     def refresh(bg: str) -> tk.PhotoImage:
#         img = IconFactory._new(bg)
#         IconFactory._circle(img, 10, 10, 8, "#2563EB")
#         IconFactory._rect(img, 9, 5, 12, 7, "#FFFFFF")
#         IconFactory._rect(img, 13, 9, 15, 12, "#FFFFFF")
#         return img

#     @staticmethod
#     def plus(bg: str) -> tk.PhotoImage:
#         img = IconFactory._new(bg)
#         IconFactory._circle(img, 10, 10, 8, "#16A34A")
#         IconFactory._rect(img, 9, 6, 11, 14, "#FFFFFF")
#         IconFactory._rect(img, 6, 9, 14, 11, "#FFFFFF")
#         return img

#     @staticmethod
#     def pencil(bg: str) -> tk.PhotoImage:
#         img = IconFactory._new(bg)
#         IconFactory._line(img, 5, 15, 15, 5, "#7C3AED", 3)
#         IconFactory._rect(img, 13, 4, 16, 7, "#FCD34D")
#         return img

#     @staticmethod
#     def trash(bg: str) -> tk.PhotoImage:
#         img = IconFactory._new(bg)
#         IconFactory._rect(img, 6, 7, 14, 17, "#DC2626")
#         IconFactory._rect(img, 5, 5, 15, 7, "#991B1B")
#         IconFactory._rect(img, 8, 9, 9, 16, "#FFFFFF")
#         IconFactory._rect(img, 11, 9, 12, 16, "#FFFFFF")
#         return img

#     @staticmethod
#     def key(bg: str) -> tk.PhotoImage:
#         img = IconFactory._new(bg)
#         IconFactory._circle(img, 7, 11, 4, "#D97706")
#         IconFactory._rect(img, 10, 10, 17, 12, "#D97706")
#         IconFactory._rect(img, 14, 8, 15, 10, "#D97706")
#         IconFactory._rect(img, 16, 8, 17, 10, "#D97706")
#         return img


# def _format_rows_as_text(rows: list[dict[str, Any]]) -> str:
#     if not rows:
#         return "(no rows)"
#     cols = list(rows[0].keys())
#     widths = {c: max(len(c), *(len(str(r.get(c, ""))) for r in rows)) for c in cols}
#     header = " | ".join(c.ljust(widths[c]) for c in cols)
#     sep = "-+-".join("-" * widths[c] for c in cols)
#     body = "\n".join(" | ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols) for r in rows)
#     return f"{header}\n{sep}\n{body}"


# class LoginFrame(ttk.Frame):
#     def __init__(self, master: tk.Widget, on_login: Callable[[PGConnection], None]) -> None:
#         super().__init__(master, padding=0)
#         self._on_login = on_login
#         cfg = DbConfig.from_env()

#         # Prefill connection inputs. Use environment values when present,
#         # otherwise fall back to the requested defaults.
#         # self.var_host = tk.StringVar(value=cfg.host or "localhost")
#         # self.var_port = tk.StringVar(value=str(cfg.port or 5432))
#         # self.var_db = tk.StringVar(value=cfg.port or"PATIENT_MANAGEMENT")
#         # self.var_user = tk.StringVar(value=cfg.port or"Myuser")
#         # self.var_pass = tk.StringVar(value=cfg.port or"pas1234")

#         # Prefill connection inputs. Use environment values when present,
#         # otherwise fall back to the requested defaults.
#         self.var_host = tk.StringVar(value=getattr(cfg, 'host', None) or "localhost")
#         self.var_port = tk.StringVar(value=str(getattr(cfg, 'port', None) or 5432))
#         self.var_db = tk.StringVar(value=getattr(cfg, 'database', None) or "PATIENT_MANAGEMENT")
#         self.var_user = tk.StringVar(value=getattr(cfg, 'user', None) or "Myuser")
#         self.var_pass = tk.StringVar(value=getattr(cfg, 'password', None) or "pas1234")

        
#         wrap = ttk.Frame(self)
#         wrap.pack(fill="both", expand=True, padx=22, pady=22)

#         hero = ttk.Frame(wrap, style="Card.TFrame", padding=18)
#         hero.grid(row=0, column=0, sticky="nsew")
#         hero.columnconfigure(0, weight=1)

#         ttk.Label(hero, text="MedFlow", style="Title.TLabel").grid(row=0, column=0, sticky="w")
#         ttk.Label(hero, text="Step E - Login", style="Muted.TLabel").grid(row=1, column=0, sticky="w", pady=(2, 0))

#         form = ttk.LabelFrame(wrap, text="Database Connection", padding=14)
#         form.grid(row=1, column=0, sticky="nsew", pady=(14, 0))
#         for i, (lbl, var, show) in enumerate(
#             [
#                 ("Host", self.var_host, None),
#                 ("Port", self.var_port, None),
#                 ("Database", self.var_db, None),
#                 ("User", self.var_user, None),
#                 ("Password", self.var_pass, "*"),
#             ]
#         ):
#             ttk.Label(form, text=lbl, style="H2.TLabel").grid(row=i, column=0, sticky="w", pady=6)
#             e = ttk.Entry(form, textvariable=var, width=44, show=show)
#             e.grid(row=i, column=1, sticky="w", pady=6, padx=(10, 0))

#         actions = ttk.Frame(wrap)
#         actions.grid(row=2, column=0, sticky="w", pady=(14, 0))
#         ttk.Button(actions, text="Connect", style="Primary.TButton", command=self._connect).grid(row=0, column=0, padx=(0, 10))
#         ttk.Label(
#             wrap,
#             text="Tip: you can also set PGHOST / PGPORT / PGDATABASE / PGUSER / PGPASSWORD as environment variables.",
#             style="Muted.TLabel",
#         ).grid(row=3, column=0, sticky="w", pady=(10, 0))

#         wrap.columnconfigure(0, weight=1)

#     def _connect(self) -> None:
#         try:
#             cfg = DbConfig(
#                 host=self.var_host.get().strip(),
#                 port=int(self.var_port.get().strip()),
#                 database=self.var_db.get().strip(),
#                 user=self.var_user.get().strip(),
#                 password=self.var_pass.get(),
#             )
#             conn = connect(cfg)
#             self._on_login(conn)
#         except Exception as e:
#             messagebox.showerror("Connection failed", str(e))


# class TableCrudFrame(ttk.Frame):
#     """
#     CRUD helper for a single table.

#     Requirement note:
#     - IDs are not shown in the results table (Treeview).
#     - For Update/Delete the user must provide the primary key value.
#     """

#     def __init__(
#         self,
#         master: tk.Widget,
#         conn: PGConnection,
#         title: str,
#         icons: dict[str, tk.PhotoImage],
#         pk: str,
#         select_sql: str,
#         insert_sql: str,
#         update_sql: str,
#         delete_sql: str,
#         fields: list[tuple[str, str]],  # (label, column_name)
#         pk_label: str,
#         pk_hint: str = "",
#         after_refresh: Optional[Callable[[], None]] = None,
#     ) -> None:
#         super().__init__(master, padding=0)
#         self.conn = conn
#         self.pk = pk
#         self.select_sql = select_sql
#         self.insert_sql = insert_sql
#         self.update_sql = update_sql
#         self.delete_sql = delete_sql
#         self.fields = fields
#         self.after_refresh = after_refresh
#         self._title = title
#         self._icons = icons

#         wrap = ttk.Frame(self)
#         wrap.pack(fill="both", expand=True, padx=16, pady=14)
#         wrap.columnconfigure(0, weight=1)
#         wrap.columnconfigure(1, weight=0)
#         wrap.rowconfigure(4, weight=1)

#         header = ttk.Frame(wrap, style="Card.TFrame", padding=(14, 12))
#         header.grid(row=0, column=0, columnspan=2, sticky="ew")
#         ttk.Label(header, text=title, style="H1.TLabel").grid(row=0, column=0, sticky="w")
#         ttk.Label(header, text="CRUD (Create / Read / Update / Delete)", style="Muted.TLabel").grid(
#             row=1, column=0, sticky="w", pady=(2, 0)
#         )

#         top = ttk.LabelFrame(wrap, text="Update / Delete (Key)", padding=12)
#         top.grid(row=1, column=0, sticky="ew", pady=(12, 0))

#         # PK controls
#         self.var_pk = tk.StringVar()
#         ttk.Label(top, text=f"{pk_label}:", style="H2.TLabel").grid(row=0, column=0, sticky="w")
#         ttk.Entry(top, textvariable=self.var_pk, width=22).grid(row=0, column=1, sticky="w", padx=(10, 0))
#         if pk_hint:
#             ttk.Label(top, text=pk_hint, style="Muted.TLabel").grid(row=0, column=2, sticky="w", padx=(10, 0))

#         # Form fields (scrollable)
#         self.vars: dict[str, tk.StringVar] = {}
#         form = ttk.LabelFrame(wrap, text="Form", padding=12)
#         form.grid(row=2, column=0, sticky="ew", pady=(12, 0))

#         # Create a canvas + vscrollbar so the form can scroll when many fields exist
#         form.columnconfigure(0, weight=1)
#         form.rowconfigure(0, weight=1)
#         _canvas = tk.Canvas(form, highlightthickness=0)
#         _vsb = ttk.Scrollbar(form, orient="vertical", command=_canvas.yview)
#         _canvas.configure(yscrollcommand=_vsb.set)
#         _canvas.grid(row=0, column=0, sticky="nsew")
#         _vsb.grid(row=0, column=1, sticky="ns")

#         _inner = ttk.Frame(_canvas)
#         _window = _canvas.create_window((0, 0), window=_inner, anchor="nw")

#         def _on_inner_config(event: tk.Event) -> None:
#             _canvas.configure(scrollregion=_canvas.bbox("all"))
#             # ensure inner frame width matches canvas width so widgets use full width
#             try:
#                 _canvas.itemconfigure(_window, width=_canvas.winfo_width())
#             except Exception:
#                 pass

#         _inner.bind("<Configure>", _on_inner_config)

#         # bind mousewheel when cursor is over canvas
#         def _on_mousewheel(event: tk.Event) -> None:
#             delta = 0
#             if event.num == 5 or event.delta < 0:
#                 delta = 1
#             elif event.num == 4 or event.delta > 0:
#                 delta = -1
#             _canvas.yview_scroll(delta, "units")

#         _canvas.bind("<Enter>", lambda e: _canvas.bind_all("<MouseWheel>", _on_mousewheel))
#         _canvas.bind("<Leave>", lambda e: _canvas.unbind_all("<MouseWheel>"))

#         # place form fields inside the scrolling inner frame
#         for i, (lbl, col) in enumerate(fields):
#             self.vars[col] = tk.StringVar()
#             ttk.Label(_inner, text=lbl, style="H2.TLabel").grid(row=i, column=0, sticky="w", pady=6)
#             ttk.Entry(_inner, textvariable=self.vars[col], width=56).grid(row=i, column=1, sticky="w", pady=6, padx=(10, 0))

#         btns = ttk.Frame(wrap)
#         btns.grid(row=3, column=0, sticky="w", pady=(12, 0))
#         ttk.Button(
#             btns,
#             text="Refresh",
#             image=self._icons["refresh"],
#             compound="left",
#             style="Primary.TButton",
#             command=self.refresh,
#         ).grid(row=0, column=0, padx=(0, 10))
#         ttk.Button(
#             btns,
#             text="Insert",
#             image=self._icons["plus"],
#             compound="left",
#             style="Success.TButton",
#             command=self.insert,
#         ).grid(row=0, column=1, padx=(0, 10))
#         ttk.Button(
#             btns,
#             text="Fetch by Key",
#             image=self._icons["key"],
#             compound="left",
#             command=self.fetch_by_key,
#         ).grid(row=0, column=2, padx=(0, 10))
#         ttk.Button(
#             btns,
#             text="Update",
#             image=self._icons["pencil"],
#             compound="left",
#             style="Primary.TButton",
#             command=self.update,
#         ).grid(row=0, column=3, padx=(0, 10))
#         ttk.Button(
#             btns,
#             text="Delete",
#             image=self._icons["trash"],
#             compound="left",
#             style="Danger.TButton",
#             command=self.delete,
#         ).grid(row=0, column=4, padx=(0, 10))

#         # Results
#         res = ttk.LabelFrame(wrap, text="Results", padding=10)
#         res.grid(row=4, column=0, sticky="nsew", pady=(12, 0))

#         self.tree = ttk.Treeview(res, columns=(), show="headings", height=14)
#         vsb = ttk.Scrollbar(res, orient="vertical", command=self.tree.yview)
#         hsb = ttk.Scrollbar(res, orient="horizontal", command=self.tree.xview)
#         self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

#         self.tree.grid(row=0, column=0, sticky="nsew")
#         vsb.grid(row=0, column=1, sticky="ns")
#         hsb.grid(row=1, column=0, sticky="ew")
#         res.columnconfigure(0, weight=1)
#         res.rowconfigure(0, weight=1)

#         # Side panel: stats & guidance
#         side = ttk.Frame(wrap, style="Card.TFrame", padding=12)
#         side.grid(row=1, column=1, rowspan=4, sticky="nsew", padx=(12, 0))
#         ttk.Label(side, text="Panel", style="H2.TLabel").grid(row=0, column=0, sticky="w")
#         self.lbl_stats = ttk.Label(side, text="Rows: -", style="Big.TLabel")
#         self.lbl_stats.grid(row=1, column=0, sticky="w", pady=(10, 0))
#         ttk.Separator(side).grid(row=2, column=0, sticky="ew", pady=12)
#         ttk.Label(side, text="How to update", style="H2.TLabel").grid(row=3, column=0, sticky="w")
#         ttk.Label(
#             side,
#             text="1) Enter the key\n2) Click Fetch by Key\n3) Edit fields\n4) Click Update",
#             style="Muted.TLabel",
#             justify="left",
#         ).grid(row=4, column=0, sticky="w", pady=(6, 0))
#         ttk.Separator(side).grid(row=5, column=0, sticky="ew", pady=12)
#         ttk.Label(side, text="Tip", style="H2.TLabel").grid(row=6, column=0, sticky="w")
#         ttk.Label(
#             side,
#             text="Results hide IDs.\nForeign keys are shown as names using JOINs.",
#             style="Muted.TLabel",
#             justify="left",
#         ).grid(row=7, column=0, sticky="w", pady=(6, 0))

#         wrap.columnconfigure(0, weight=1)
#         wrap.rowconfigure(4, weight=1)

#         self.refresh()

#     def _set_tree(self, rows: list[dict[str, Any]]) -> None:
#         self.tree.delete(*self.tree.get_children())
#         if not rows:
#             self.tree["columns"] = ("message",)
#             self.tree.heading("message", text="message")
#             self.tree.column("message", width=600, anchor="w")
#             self.tree.insert("", "end", values=("No rows",))
#             self.lbl_stats.configure(text="Rows: 0")
#             return

#         cols = list(rows[0].keys())
#         self.tree["columns"] = cols
#         for c in cols:
#             self.tree.heading(c, text=c)
#             self.tree.column(c, width=140, anchor="w")
#         self.tree.tag_configure("odd", background=AppTheme.zebra_1)
#         self.tree.tag_configure("even", background=AppTheme.zebra_2)
#         for i, r in enumerate(rows):
#             tag = "even" if i % 2 == 0 else "odd"
#             self.tree.insert("", "end", values=[r.get(c) for c in cols], tags=(tag,))
#         self.lbl_stats.configure(text=f"Rows: {len(rows)}")

#     def refresh(self) -> None:
#         try:
#             rows = fetch_all(self.conn, self.select_sql)
#             self._set_tree(rows)
#             if self.after_refresh:
#                 self.after_refresh()
#         except Exception as e:
#             messagebox.showerror("Refresh failed", str(e))

#     def insert(self) -> None:
#         try:
#             values = [self.vars[col].get().strip() or None for _, col in self.fields]
#             execute(self.conn, self.insert_sql, values)
#             self.refresh()
#         except Exception as e:
#             messagebox.showerror("Insert failed", str(e))

#     def fetch_by_key(self) -> None:
#         try:
#             key = self.var_pk.get().strip()
#             if not key:
#                 messagebox.showwarning("Missing key", "Please enter the key value first.")
#                 return
#             row = fetch_one(
#                 self.conn,
#                 f"SELECT * FROM {self._table_from_select()} WHERE {self.pk} = %s",
#                 (key,),
#             )
#             if not row:
#                 messagebox.showinfo("Not found", "No row found for the given key.")
#                 return
#             for _, col in self.fields:
#                 if col in row:
#                     self.vars[col].set("" if row[col] is None else str(row[col]))
#         except Exception as e:
#             messagebox.showerror("Fetch failed", str(e))

#     def update(self) -> None:
#         try:
#             key = self.var_pk.get().strip()
#             if not key:
#                 messagebox.showwarning("Missing key", "Please enter the key value first.")
#                 return
#             values = [self.vars[col].get().strip() or None for _, col in self.fields] + [key]
#             cnt = execute(self.conn, self.update_sql, values)
#             if cnt == 0:
#                 messagebox.showinfo("Update", "No rows were updated (check the key).")
#             self.refresh()
#         except Exception as e:
#             messagebox.showerror("Update failed", str(e))

#     def delete(self) -> None:
#         try:
#             key = self.var_pk.get().strip()
#             if not key:
#                 messagebox.showwarning("Missing key", "Please enter the key value first.")
#                 return
#             if not messagebox.askyesno("Confirm delete", "Are you sure you want to delete this record?"):
#                 return
#             cnt = execute(self.conn, self.delete_sql, (key,))
#             if cnt == 0:
#                 messagebox.showinfo("Delete", "No rows were deleted (check the key).")
#             self.refresh()
#         except Exception as e:
#             messagebox.showerror("Delete failed", str(e))

#     def _table_from_select(self) -> str:
#         # best-effort: expects "FROM public.<table>" in select_sql
#         lower = self.select_sql.lower()
#         idx = lower.find(" from ")
#         if idx == -1:
#             raise ValueError("select_sql must contain FROM ...")
#         after = lower[idx + 6 :].strip()
#         return after.split()[0]


# class QueriesAndProgramsFrame(ttk.Frame):
#     def __init__(self, master: tk.Widget, conn: PGConnection, icons: dict[str, tk.PhotoImage]) -> None:
#         super().__init__(master, padding=0)
#         self.conn = conn
#         self._icons = icons

#         wrap = ttk.Frame(self)
#         wrap.pack(fill="both", expand=True, padx=16, pady=14)
#         wrap.columnconfigure(1, weight=1)
#         wrap.rowconfigure(2, weight=1)

#         header = ttk.Frame(wrap, style="Card.TFrame", padding=(14, 12))
#         header.grid(row=0, column=0, columnspan=2, sticky="ew")
#         ttk.Label(header, text="Queries & Programs", style="H1.TLabel").grid(row=0, column=0, sticky="w")
#         ttk.Label(header, text="Run Step B queries and Step D programs", style="Muted.TLabel").grid(row=1, column=0, sticky="w")

#         left = ttk.Frame(wrap)
#         left.grid(row=2, column=0, sticky="nsw", pady=(12, 0))

#         # Step B queries (2)
#         qbox = ttk.LabelFrame(left, text="Step B Queries", padding=10)
#         qbox.grid(row=0, column=0, sticky="ew")
#         ttk.Button(
#             qbox,
#             text="Query 1: Admissions in 2024",
#             image=self._icons["doc"],
#             compound="left",
#             style="Primary.TButton",
#             command=self._q1,
#         ).grid(
#             row=0, column=0, sticky="w", pady=4
#         )
#         ttk.Button(
#             qbox,
#             text="Query 2: Severe-allergy per year",
#             image=self._icons["doc"],
#             compound="left",
#             style="Primary.TButton",
#             command=self._q2,
#         ).grid(
#             row=1, column=0, sticky="w", pady=4
#         )

#         # Step D programs (at least 2)
#         pbox = ttk.LabelFrame(left, text="Step D Programs", padding=10)
#         pbox.grid(row=1, column=0, sticky="ew", pady=(10, 0))

#         self.var_patient_id = tk.StringVar(value="42001")
#         ttk.Label(pbox, text="patient_id:", style="H2.TLabel").grid(row=0, column=0, sticky="w")
#         ttk.Entry(pbox, textvariable=self.var_patient_id, width=18).grid(row=0, column=1, sticky="w", padx=(8, 0))
#         ttk.Button(
#             pbox,
#             text="Run fn_patient_risk_score",
#             image=self._icons["play"],
#             compound="left",
#             style="Success.TButton",
#             command=self._run_risk,
#         ).grid(
#             row=0, column=2, sticky="w", padx=(12, 0)
#         )

#         self.var_days = tk.StringVar(value="60")
#         ttk.Label(pbox, text="days:", style="H2.TLabel").grid(row=1, column=0, sticky="w", pady=(8, 0))
#         ttk.Entry(pbox, textvariable=self.var_days, width=18).grid(row=1, column=1, sticky="w", padx=(8, 0), pady=(8, 0))
#         ttk.Button(
#             pbox,
#             text="Call sp_close_long_open_admissions",
#             image=self._icons["play"],
#             compound="left",
#             style="Warn.TButton",
#             command=self._call_close,
#         ).grid(
#             row=1, column=2, sticky="w", padx=(12, 0), pady=(8, 0)
#         )

#         # Output
#         outbox = ttk.LabelFrame(wrap, text="Output", padding=10)
#         outbox.grid(row=2, column=1, sticky="nsew", padx=(12, 0), pady=(12, 0))
#         self.txt = tk.Text(outbox, height=28, wrap="none", bg=AppTheme.card, fg=AppTheme.text, relief="flat")
#         ysb = ttk.Scrollbar(outbox, orient="vertical", command=self.txt.yview)
#         xsb = ttk.Scrollbar(outbox, orient="horizontal", command=self.txt.xview)
#         self.txt.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
#         self.txt.grid(row=0, column=0, sticky="nsew")
#         ysb.grid(row=0, column=1, sticky="ns")
#         xsb.grid(row=1, column=0, sticky="ew")
#         outbox.columnconfigure(0, weight=1)
#         outbox.rowconfigure(0, weight=1)

#         wrap.columnconfigure(0, weight=0)
#         wrap.columnconfigure(1, weight=1)
#         wrap.rowconfigure(2, weight=1)

#     def _write(self, title: str, rows: Optional[list[dict[str, Any]]] = None, text: str = "") -> None:
#         self.txt.delete("1.0", "end")
#         self.txt.insert("end", title + "\n\n")
#         if rows is not None:
#             self.txt.insert("end", _format_rows_as_text(rows))
#         if text:
#             self.txt.insert("end", "\n\n" + text)

#     def _q1(self) -> None:
#         sql = """
# SELECT DISTINCT p.first_name, p.last_name, p.email
# FROM public.patient p
# JOIN public.admission a ON p.patient_id = a.patient_id
# WHERE EXTRACT(YEAR FROM a.admission_date) = 2024
# ORDER BY p.last_name;
# """.strip()
#         rows = fetch_all(self.conn, sql)
#         self._write("Query 1: Admissions in 2024", rows=rows)

#     def _q2(self) -> None:
#         sql = """
# SELECT EXTRACT(YEAR FROM admission_date) as year_part, COUNT(*) as total_admissions
# FROM public.admission
# WHERE patient_id IN (
#     SELECT patient_id FROM public.patient_allergy WHERE severity = 'Severe'
# )
# GROUP BY EXTRACT(YEAR FROM admission_date)
# ORDER BY year_part DESC;
# """.strip()
#         rows = fetch_all(self.conn, sql)
#         self._write("Query 2: Severe-allergy admissions per year", rows=rows)

#     def _run_risk(self) -> None:
#         pid = self.var_patient_id.get().strip()
#         sql = "SELECT public.fn_patient_risk_score(%s) AS risk_score;"
#         try:
#             rows = fetch_all(self.conn, sql, (pid,))
#             self._write("Step D: fn_patient_risk_score", rows=rows)
#         except Exception as e:
#             self._write("Step D: fn_patient_risk_score (ERROR)", text=str(e))

#     def _call_close(self) -> None:
#         days = self.var_days.get().strip()
#         sql = "CALL public.sp_close_long_open_admissions(%s);"
#         try:
#             execute(self.conn, sql, (days,))
#             self._write("Step D: sp_close_long_open_admissions", text="Procedure executed successfully.")
#         except Exception as e:
#             self._write("Step D: sp_close_long_open_admissions (ERROR)", text=str(e))


# class MedFlowApp(ttk.Frame):
#     def __init__(self, master: tk.Widget) -> None:
#         super().__init__(master)
#         self.conn: Optional[PGConnection] = None
#         self._root = master.winfo_toplevel()
#         apply_theme(self._root)  # global ttk styles

#         self.container = ttk.Frame(self)
#         self.container.pack(fill="both", expand=True)

#         self._nav_buttons: dict[str, ttk.Button] = {}
#         self._content: Optional[ttk.Frame] = None
#         self._icons: dict[str, tk.PhotoImage] = {}

#         self._show_login()

#     def _show_login(self) -> None:
#         for w in self.container.winfo_children():
#             w.destroy()
#         LoginFrame(self.container, self._on_login).pack(fill="both", expand=True)

#     def _on_login(self, conn: PGConnection) -> None:
#         self.conn = conn
#         for w in self.container.winfo_children():
#             w.destroy()
#         self._build_main_ui()

#     def _build_main_ui(self) -> None:
#         assert self.conn is not None
#         root = ttk.Frame(self.container)
#         root.pack(fill="both", expand=True)
#         root.columnconfigure(1, weight=1)
#         root.rowconfigure(0, weight=1)

#         # Sidebar
#         sidebar = ttk.Frame(root, style="Sidebar.TFrame", padding=(14, 14))
#         sidebar.grid(row=0, column=0, sticky="nsw")

#         ttk.Label(sidebar, text="MedFlow", style="SidebarTitle.TLabel").grid(row=0, column=0, sticky="w")
#         ttk.Label(sidebar, text="Step E - GUI", style="SidebarMuted.TLabel").grid(row=1, column=0, sticky="w", pady=(2, 14))

#         nav = ttk.Frame(sidebar, style="Sidebar.TFrame")
#         nav.grid(row=2, column=0, sticky="nsew")

#         # Content area
#         content_host = ttk.Frame(root)
#         content_host.grid(row=0, column=1, sticky="nsew")
#         content_host.rowconfigure(1, weight=1)
#         content_host.columnconfigure(0, weight=1)

#         topbar = ttk.Frame(content_host, style="Card.TFrame", padding=(16, 12))
#         topbar.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 0))
#         self.lbl_top = ttk.Label(topbar, text="Dashboard", style="H1.TLabel")
#         self.lbl_top.grid(row=0, column=0, sticky="w")
#         ttk.Label(topbar, text="Navigation on the left • Results hide IDs • FK shown as names", style="Muted.TLabel").grid(
#             row=1, column=0, sticky="w", pady=(2, 0)
#         )

#         self._content = ttk.Frame(content_host)
#         self._content.grid(row=1, column=0, sticky="nsew")

#         # Icons (keep references!)
#         bg = AppTheme.sidebar_card
#         self._icons = {
#             "home": IconFactory.home(bg),
#             "users": IconFactory.users(bg),
#             "calendar": IconFactory.calendar(bg),
#             "alert": IconFactory.alert(bg),
#             "shield": IconFactory.shield(bg),
#             "phone": IconFactory.phone(bg),
#             "doc": IconFactory.doc(bg),
#             "play": IconFactory.play(bg),
#             "refresh": IconFactory.refresh(AppTheme.card),
#             "plus": IconFactory.plus(AppTheme.card),
#             "pencil": IconFactory.pencil(AppTheme.card),
#             "trash": IconFactory.trash(AppTheme.card),
#             "key": IconFactory.key(AppTheme.card),
#         }

#         def add_nav(key: str, label: str, cmd: Callable[[], None]) -> None:
#             icon = self._icons.get(key)
#             btn = ttk.Button(nav, text=label, image=icon, compound="left", style="Nav.TButton", command=cmd)
#             btn.grid(sticky="ew", pady=6)
#             self._nav_buttons[key] = btn

#         def set_active(key: str) -> None:
#             for k, b in self._nav_buttons.items():
#                 b.configure(style="NavActive.TButton" if k == key else "Nav.TButton")

#         def show(frame: ttk.Frame, title: str, key: str) -> None:
#             for w in self._content.winfo_children():
#                 w.destroy()
#             frame.pack(fill="both", expand=True)
#             self.lbl_top.configure(text=title)
#             set_active(key)

#         # Frames (build once)
#         patients = TableCrudFrame(
#             self._content,
#             self.conn,
#             title="Patients",
#             icons=self._icons,
#             pk="patient_id",
#             pk_label="patient_id",
#             pk_hint="(key field; not shown in results table)",
#             select_sql="""
# SELECT first_name, last_name, date_of_birth, gender, phone, email, address
# FROM public.patient
# ORDER BY last_name, first_name;
# """.strip(),
#             insert_sql="""
# INSERT INTO public.patient (first_name, last_name, date_of_birth, gender, phone, email, address, patient_id)
# VALUES (%s,%s,%s,%s,%s,%s,%s,%s);
# """.strip(),
#             update_sql="""
# UPDATE public.patient
# SET first_name=%s, last_name=%s, date_of_birth=%s, gender=%s, phone=%s, email=%s, address=%s
# WHERE patient_id=%s;
# """.strip(),
#             delete_sql="DELETE FROM public.patient WHERE patient_id=%s;",
#             fields=[
#                 ("first_name", "first_name"),
#                 ("last_name", "last_name"),
#                 ("date_of_birth (YYYY-MM-DD)", "date_of_birth"),
#                 ("gender (Male/Female/Other)", "gender"),
#                 ("phone", "phone"),
#                 ("email", "email"),
#                 ("address", "address"),
#                 ("patient_id (key for INSERT)", "patient_id"),
#             ],
#         )

#         admissions = TableCrudFrame(
#             self._content,
#             self.conn,
#             title="Admissions",
#             icons=self._icons,
#             pk="admission_id",
#             pk_label="admission_id",
#             pk_hint="(key field; not shown in results table)",
#             select_sql="""
# SELECT
#   (p.first_name || ' ' || p.last_name) AS patient_name,
#   a.admission_date,
#   a.discharge_date,
#   a.admission_type,
#   a.reason
# FROM public.admission a
# JOIN public.patient p ON p.patient_id = a.patient_id
# ORDER BY a.admission_date DESC;
# """.strip(),
#             insert_sql="""
# INSERT INTO public.admission (admission_date, discharge_date, admission_type, reason, patient_id, admission_id)
# VALUES (%s,%s,%s,%s,%s,%s);
# """.strip(),
#             update_sql="""
# UPDATE public.admission
# SET admission_date=%s, discharge_date=%s, admission_type=%s, reason=%s, patient_id=%s
# WHERE admission_id=%s;
# """.strip(),
#             delete_sql="DELETE FROM public.admission WHERE admission_id=%s;",
#             fields=[
#                 ("admission_date (YYYY-MM-DD)", "admission_date"),
#                 ("discharge_date (YYYY-MM-DD or empty)", "discharge_date"),
#                 ("admission_type (Emergency/Elective/Urgent)", "admission_type"),
#                 ("reason", "reason"),
#                 ("patient_id (key; will display as name in results)", "patient_id"),
#                 ("admission_id (key for INSERT)", "admission_id"),
#             ],
#         )

#         allergies = TableCrudFrame(
#             self._content,
#             self.conn,
#             title="Patient Allergies",
#             icons=self._icons,
#             pk="allergy_id",
#             pk_label="allergy_id",
#             pk_hint="(key field; not shown in results table)",
#             select_sql="""
# SELECT
#   (p.first_name || ' ' || p.last_name) AS patient_name,
#   pa.allergy_name,
#   pa.severity,
#   pa.notes
# FROM public.patient_allergy pa
# JOIN public.patient p ON p.patient_id = pa.patient_id
# ORDER BY p.last_name, p.first_name, pa.allergy_name;
# """.strip(),
#             insert_sql="""
# INSERT INTO public.patient_allergy (allergy_name, severity, notes, patient_id, allergy_id)
# VALUES (%s,%s,%s,%s,%s);
# """.strip(),
#             update_sql="""
# UPDATE public.patient_allergy
# SET allergy_name=%s, severity=%s, notes=%s, patient_id=%s
# WHERE allergy_id=%s;
# """.strip(),
#             delete_sql="DELETE FROM public.patient_allergy WHERE allergy_id=%s;",
#             fields=[
#                 ("allergy_name", "allergy_name"),
#                 ("severity (Mild/Moderate/Severe/Unknown)", "severity"),
#                 ("notes", "notes"),
#                 ("patient_id", "patient_id"),
#                 ("allergy_id (key for INSERT)", "allergy_id"),
#             ],
#         )

#         insurance = TableCrudFrame(
#             self._content,
#             self.conn,
#             title="Patient Insurance",
#             icons=self._icons,
#             pk="insurance_id",
#             pk_label="insurance_id",
#             pk_hint="(key field; not shown in results table)",
#             select_sql="""
# SELECT
#   (p.first_name || ' ' || p.last_name) AS patient_name,
#   pi.provider_name,
#   pi.policy_number,
#   pi.coverage_type,
#   pi.expiration_date
# FROM public.patient_insurance pi
# JOIN public.patient p ON p.patient_id = pi.patient_id
# ORDER BY p.last_name, p.first_name;
# """.strip(),
#             insert_sql="""
# INSERT INTO public.patient_insurance (provider_name, policy_number, coverage_type, expiration_date, patient_id, insurance_id)
# VALUES (%s,%s,%s,%s,%s,%s);
# """.strip(),
#             update_sql="""
# UPDATE public.patient_insurance
# SET provider_name=%s, policy_number=%s, coverage_type=%s, expiration_date=%s, patient_id=%s
# WHERE insurance_id=%s;
# """.strip(),
#             delete_sql="DELETE FROM public.patient_insurance WHERE insurance_id=%s;",
#             fields=[
#                 ("provider_name", "provider_name"),
#                 ("policy_number", "policy_number"),
#                 ("coverage_type", "coverage_type"),
#                 ("expiration_date (YYYY-MM-DD)", "expiration_date"),
#                 ("patient_id", "patient_id"),
#                 ("insurance_id (key for INSERT)", "insurance_id"),
#             ],
#         )

#         history = TableCrudFrame(
#             self._content,
#             self.conn,
#             title="Medical History",
#             icons=self._icons,
#             pk="history_id",
#             pk_label="history_id",
#             pk_hint="(key field; not shown in results table)",
#             select_sql="""
# SELECT
#   (p.first_name || ' ' || p.last_name) AS patient_name,
#   pmh.condition,
#   pmh.diagnosis_date,
#   pmh.notes
# FROM public.patient_medical_history pmh
# JOIN public.patient p ON p.patient_id = pmh.patient_id
# ORDER BY p.last_name, p.first_name, pmh.diagnosis_date DESC;
# """.strip(),
#             insert_sql="""
# INSERT INTO public.patient_medical_history (condition, diagnosis_date, notes, patient_id, history_id)
# VALUES (%s,%s,%s,%s,%s);
# """.strip(),
#             update_sql="""
# UPDATE public.patient_medical_history
# SET condition=%s, diagnosis_date=%s, notes=%s, patient_id=%s
# WHERE history_id=%s;
# """.strip(),
#             delete_sql="DELETE FROM public.patient_medical_history WHERE history_id=%s;",
#             fields=[
#                 ("condition", "condition"),
#                 ("diagnosis_date (YYYY-MM-DD)", "diagnosis_date"),
#                 ("notes", "notes"),
#                 ("patient_id", "patient_id"),
#                 ("history_id (key for INSERT)", "history_id"),
#             ],
#         )

#         contacts = TableCrudFrame(
#             self._content,
#             self.conn,
#             title="Emergency Contacts",
#             icons=self._icons,
#             pk="contact_id",
#             pk_label="contact_id",
#             pk_hint="(key field; not shown in results table)",
#             select_sql="""
# SELECT
#   (p.first_name || ' ' || p.last_name) AS patient_name,
#   ec.name AS contact_name,
#   ec.relationship,
#   ec.phone
# FROM public.emergency_contact ec
# JOIN public.patient p ON p.patient_id = ec.patient_id
# ORDER BY p.last_name, p.first_name, ec.name;
# """.strip(),
#             insert_sql="""
# INSERT INTO public.emergency_contact (name, relationship, phone, patient_id, contact_id)
# VALUES (%s,%s,%s,%s,%s);
# """.strip(),
#             update_sql="""
# UPDATE public.emergency_contact
# SET name=%s, relationship=%s, phone=%s, patient_id=%s
# WHERE contact_id=%s;
# """.strip(),
#             delete_sql="DELETE FROM public.emergency_contact WHERE contact_id=%s;",
#             fields=[
#                 ("name", "name"),
#                 ("relationship", "relationship"),
#                 ("phone", "phone"),
#                 ("patient_id", "patient_id"),
#                 ("contact_id (key for INSERT)", "contact_id"),
#             ],
#         )

#         qp = QueriesAndProgramsFrame(self._content, self.conn, self._icons)

#         # Dashboard
#         dash = ttk.Frame(self._content, padding=16)
#         card = ttk.Frame(dash, style="Card.TFrame", padding=18)
#         card.pack(fill="x", pady=(8, 0))
#         ttk.Label(card, text="Welcome", style="H1.TLabel").pack(anchor="w")
#         ttk.Label(
#             card,
#             text="Use the navigation on the left to manage all tables (CRUD), run queries, and run Step D programs.",
#             style="Big.TLabel",
#             wraplength=760,
#             justify="left",
#         ).pack(anchor="w", pady=(8, 0))

#         add_nav("home", "Dashboard", lambda: show(dash, "Dashboard", "home"))
#         add_nav("users", "Patients", lambda: show(patients, "Patients", "users"))
#         add_nav("calendar", "Admissions", lambda: show(admissions, "Admissions", "calendar"))
#         add_nav("alert", "Allergies", lambda: show(allergies, "Allergies", "alert"))
#         add_nav("shield", "Insurance", lambda: show(insurance, "Insurance", "shield"))
#         add_nav("doc", "Medical History", lambda: show(history, "Medical History", "doc"))
#         add_nav("phone", "Emergency Contacts", lambda: show(contacts, "Emergency Contacts", "phone"))
#         add_nav("play", "Queries & Programs", lambda: show(qp, "Queries & Programs", "play"))

#         ttk.Separator(sidebar).grid(row=3, column=0, sticky="ew", pady=14)
#         ttk.Button(sidebar, text="Logout", style="Nav.TButton", command=self._show_login).grid(row=4, column=0, sticky="ew")

#         # default view
#         show(dash, "Dashboard", "home")

#         # NOTE: Old Notebook-based navigation was replaced by Sidebar navigation above.

from __future__ import annotations

import tkinter as tk
from tkinter import messagebox, ttk
from typing import Any, Callable, Optional

from psycopg2.extensions import connection as PGConnection

from .db import DbConfig, connect, execute, fetch_all, fetch_one


class AppTheme:
    # Colorful + clean palette (light sidebar, strong accent)
    bg = "#F4F7FF"
    card = "#FFFFFF"
    border = "#D7E0F2"
    text = "#0B1220"
    muted = "#475569"

    primary = "#2563EB"  # blue
    primary_dark = "#1E40AF"
    success = "#16A34A"  # green
    danger = "#DC2626"  # red
    warn = "#D97706"  # amber

    zebra_1 = "#FFFFFF"
    zebra_2 = "#F3F6FF"

    # Sidebar (light)
    sidebar_bg = "#FFFFFF"
    sidebar_card = "#F3F6FF"
    sidebar_text = "#0B1220"
    sidebar_muted = "#64748B"
    sidebar_active = "#2563EB"
    sidebar_active_text = "#FFFFFF"


def apply_theme(root: tk.Tk) -> ttk.Style:
    style = ttk.Style(root)
    try:
        style.theme_use("clam")
    except Exception:
        pass

    root.configure(bg=AppTheme.bg)

    # Base
    style.configure(".", font=("Segoe UI", 11))
    style.configure("TFrame", background=AppTheme.bg)
    style.configure("Card.TFrame", background=AppTheme.card, relief="flat")
    style.configure("TLabel", background=AppTheme.bg, foreground=AppTheme.text)
    style.configure("Muted.TLabel", foreground=AppTheme.muted)
    style.configure("Title.TLabel", font=("Segoe UI", 22, "bold"), foreground=AppTheme.text)
    style.configure("H1.TLabel", font=("Segoe UI", 16, "bold"), foreground=AppTheme.text)
    style.configure("H2.TLabel", font=("Segoe UI", 12, "bold"), foreground=AppTheme.text)
    style.configure("Big.TLabel", font=("Segoe UI", 13), foreground=AppTheme.text)

    # Labelframe
    style.configure(
        "TLabelframe",
        background=AppTheme.bg,
        bordercolor=AppTheme.border,
        relief="solid",
    )
    style.configure(
        "TLabelframe.Label",
        background=AppTheme.bg,
        foreground=AppTheme.muted,
        font=("Segoe UI", 11, "bold"),
    )

    # Buttons
    style.configure("TButton", padding=(14, 10))
    style.configure("Primary.TButton", background=AppTheme.primary, foreground="white", padding=(16, 10))
    style.map(
        "Primary.TButton",
        background=[("active", AppTheme.primary_dark), ("pressed", AppTheme.primary_dark)],
        foreground=[("disabled", "#E2E8F0")],
    )
    style.configure("Success.TButton", background=AppTheme.success, foreground="white")
    style.map("Success.TButton", background=[("active", "#15803D")])
    style.configure("Danger.TButton", background=AppTheme.danger, foreground="white")
    style.map("Danger.TButton", background=[("active", "#B91C1C")])
    style.configure("Warn.TButton", background=AppTheme.warn, foreground="white")
    style.map("Warn.TButton", background=[("active", "#B45309")])

    # Sidebar
    style.configure("Sidebar.TFrame", background=AppTheme.sidebar_bg)
    style.configure("SidebarCard.TFrame", background=AppTheme.sidebar_card)
    style.configure("Sidebar.TLabel", background=AppTheme.sidebar_bg, foreground=AppTheme.sidebar_text)
    style.configure("SidebarMuted.TLabel", background=AppTheme.sidebar_bg, foreground=AppTheme.sidebar_muted)
    style.configure(
        "SidebarTitle.TLabel",
        background=AppTheme.sidebar_bg,
        foreground=AppTheme.sidebar_text,
        font=("Segoe UI", 18, "bold"),
    )
    style.configure(
        "Nav.TButton",
        background=AppTheme.sidebar_card,
        foreground=AppTheme.sidebar_text,
        padding=(14, 10),
        anchor="w",
    )
    style.map(
        "Nav.TButton",
        background=[("active", "#E7EEFF"), ("pressed", "#E7EEFF")],
    )
    style.configure(
        "NavActive.TButton",
        background=AppTheme.sidebar_active,
        foreground=AppTheme.sidebar_active_text,
        padding=(14, 10),
        anchor="w",
    )
    style.map("NavActive.TButton", background=[("active", AppTheme.sidebar_active), ("pressed", AppTheme.sidebar_active)])

    # Entries
    style.configure("TEntry", padding=(10, 8))

    # Notebook tabs
    style.configure("TNotebook", background=AppTheme.bg, borderwidth=0)
    style.configure(
        "TNotebook.Tab",
        padding=(14, 8),
        background="#E9EEFA",
        foreground=AppTheme.text,
    )
    style.map(
        "TNotebook.Tab",
        background=[("selected", AppTheme.card), ("active", "#DDE6FF")],
    )

    # Treeview
    style.configure(
        "Treeview",
        background=AppTheme.card,
        fieldbackground=AppTheme.card,
        foreground=AppTheme.text,
        rowheight=30,
        bordercolor=AppTheme.border,
        lightcolor=AppTheme.border,
        darkcolor=AppTheme.border,
    )
    style.configure(
        "Treeview.Heading",
        font=("Segoe UI", 11, "bold"),
        background="#E9EEFA",
        foreground=AppTheme.text,
        padding=(8, 6),
    )
    style.map("Treeview.Heading", background=[("active", "#DDE6FF")])

    return style


class IconFactory:
    """
    Creates small colorful icons using Tk PhotoImage (no external files needed).
    """

    size = 20

    @staticmethod
    def _new(bg: str = "#00000000") -> tk.PhotoImage:
        img = tk.PhotoImage(width=IconFactory.size, height=IconFactory.size)
        # Transparent-ish background: Tk doesn't do alpha well everywhere; use bg matching card/sidebar.
        img.put(bg, to=(0, 0, IconFactory.size, IconFactory.size))
        return img

    @staticmethod
    def _rect(img: tk.PhotoImage, x0: int, y0: int, x1: int, y1: int, color: str) -> None:
        img.put(color, to=(x0, y0, x1, y1))

    @staticmethod
    def _line(img: tk.PhotoImage, x0: int, y0: int, x1: int, y1: int, color: str, w: int = 1) -> None:
        if x0 == x1:
            for dx in range(w):
                IconFactory._rect(img, x0 + dx, min(y0, y1), x1 + dx + 1, max(y0, y1) + 1, color)
            return
        if y0 == y1:
            for dy in range(w):
                IconFactory._rect(img, min(x0, x1), y0 + dy, max(x0, x1) + 1, y1 + dy + 1, color)
            return
        # simple diagonal
        steps = max(abs(x1 - x0), abs(y1 - y0))
        for i in range(steps + 1):
            x = int(x0 + (x1 - x0) * i / steps)
            y = int(y0 + (y1 - y0) * i / steps)
            IconFactory._rect(img, x, y, x + w, y + w, color)

    @staticmethod
    def _circle(img: tk.PhotoImage, cx: int, cy: int, r: int, color: str) -> None:
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                if 0 <= x < IconFactory.size and 0 <= y < IconFactory.size:
                    if (x - cx) * (x - cx) + (y - cy) * (y - cy) <= r * r:
                        img.put(color, (x, y))

    @staticmethod
    def home(bg: str) -> tk.PhotoImage:
        img = IconFactory._new(bg)
        IconFactory._rect(img, 4, 9, 16, 17, AppTheme.primary)
        IconFactory._line(img, 4, 10, 10, 4, AppTheme.primary_dark, 2)
        IconFactory._line(img, 10, 4, 16, 10, AppTheme.primary_dark, 2)
        IconFactory._rect(img, 9, 13, 11, 17, "#FFFFFF")
        return img

    @staticmethod
    def users(bg: str) -> tk.PhotoImage:
        img = IconFactory._new(bg)
        IconFactory._circle(img, 8, 8, 4, "#7C3AED")  # purple
        IconFactory._circle(img, 14, 9, 3, "#A78BFA")
        IconFactory._rect(img, 4, 13, 12, 18, "#7C3AED")
        IconFactory._rect(img, 11, 13, 18, 18, "#A78BFA")
        return img

    @staticmethod
    def calendar(bg: str) -> tk.PhotoImage:
        img = IconFactory._new(bg)
        IconFactory._rect(img, 4, 6, 16, 17, "#0EA5E9")  # sky
        IconFactory._rect(img, 4, 6, 16, 9, "#0369A1")
        IconFactory._rect(img, 6, 4, 8, 7, "#0369A1")
        IconFactory._rect(img, 12, 4, 14, 7, "#0369A1")
        IconFactory._rect(img, 6, 11, 8, 13, "#FFFFFF")
        IconFactory._rect(img, 10, 11, 12, 13, "#FFFFFF")
        IconFactory._rect(img, 12, 14, 14, 16, "#FFFFFF")
        return img

    @staticmethod
    def alert(bg: str) -> tk.PhotoImage:
        img = IconFactory._new(bg)
        IconFactory._circle(img, 10, 10, 8, "#F59E0B")  # amber
        IconFactory._rect(img, 9, 5, 11, 12, "#FFFFFF")
        IconFactory._rect(img, 9, 14, 11, 16, "#FFFFFF")
        return img

    @staticmethod
    def shield(bg: str) -> tk.PhotoImage:
        img = IconFactory._new(bg)
        IconFactory._rect(img, 6, 4, 14, 6, "#16A34A")
        IconFactory._rect(img, 5, 6, 15, 15, "#22C55E")
        IconFactory._line(img, 7, 10, 9, 12, "#FFFFFF", 2)
        IconFactory._line(img, 9, 12, 13, 8, "#FFFFFF", 2)
        return img

    @staticmethod
    def phone(bg: str) -> tk.PhotoImage:
        img = IconFactory._new(bg)
        IconFactory._rect(img, 6, 4, 14, 17, "#0F766E")
        IconFactory._rect(img, 7, 6, 13, 13, "#CCFBF1")
        IconFactory._rect(img, 9, 14, 11, 15, "#CCFBF1")
        return img

    @staticmethod
    def doc(bg: str) -> tk.PhotoImage:
        img = IconFactory._new(bg)
        IconFactory._rect(img, 6, 4, 15, 17, "#EF4444")
        IconFactory._rect(img, 8, 7, 13, 8, "#FFFFFF")
        IconFactory._rect(img, 8, 10, 13, 11, "#FFFFFF")
        IconFactory._rect(img, 8, 13, 12, 14, "#FFFFFF")
        return img

    @staticmethod
    def play(bg: str) -> tk.PhotoImage:
        img = IconFactory._new(bg)
        IconFactory._circle(img, 10, 10, 9, "#111827")
        IconFactory._line(img, 8, 6, 8, 14, "#FFFFFF", 2)
        IconFactory._line(img, 8, 6, 14, 10, "#FFFFFF", 2)
        IconFactory._line(img, 8, 14, 14, 10, "#FFFFFF", 2)
        return img

    @staticmethod
    def refresh(bg: str) -> tk.PhotoImage:
        img = IconFactory._new(bg)
        IconFactory._circle(img, 10, 10, 8, "#2563EB")
        IconFactory._rect(img, 9, 5, 12, 7, "#FFFFFF")
        IconFactory._rect(img, 13, 9, 15, 12, "#FFFFFF")
        return img

    @staticmethod
    def plus(bg: str) -> tk.PhotoImage:
        img = IconFactory._new(bg)
        IconFactory._circle(img, 10, 10, 8, "#16A34A")
        IconFactory._rect(img, 9, 6, 11, 14, "#FFFFFF")
        IconFactory._rect(img, 6, 9, 14, 11, "#FFFFFF")
        return img

    @staticmethod
    def pencil(bg: str) -> tk.PhotoImage:
        img = IconFactory._new(bg)
        IconFactory._line(img, 5, 15, 15, 5, "#7C3AED", 3)
        IconFactory._rect(img, 13, 4, 16, 7, "#FCD34D")
        return img

    @staticmethod
    def trash(bg: str) -> tk.PhotoImage:
        img = IconFactory._new(bg)
        IconFactory._rect(img, 6, 7, 14, 17, "#DC2626")
        IconFactory._rect(img, 5, 5, 15, 7, "#991B1B")
        IconFactory._rect(img, 8, 9, 9, 16, "#FFFFFF")
        IconFactory._rect(img, 11, 9, 12, 16, "#FFFFFF")
        return img

    @staticmethod
    def key(bg: str) -> tk.PhotoImage:
        img = IconFactory._new(bg)
        IconFactory._circle(img, 7, 11, 4, "#D97706")
        IconFactory._rect(img, 10, 10, 17, 12, "#D97706")
        IconFactory._rect(img, 14, 8, 15, 10, "#D97706")
        IconFactory._rect(img, 16, 8, 17, 10, "#D97706")
        return img


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
        super().__init__(master, padding=0)
        self._on_login = on_login
        cfg = DbConfig.from_env()

        # Generate default values robustly
        default_values = {
            "Host": getattr(cfg, 'host', None) or "localhost",
            "Port": str(getattr(cfg, 'port', None) or 5432),
            "Database": getattr(cfg, 'database', None) or "PATIENT_MANAGEMENT",
            "User": getattr(cfg, 'user', None) or "Myuser",
            "Password": getattr(cfg, 'password', None) or "pas1234"
        }

        self.var_host = tk.StringVar(value=default_values["Host"])
        self.var_port = tk.StringVar(value=default_values["Port"])
        self.var_db = tk.StringVar(value=default_values["Database"])
        self.var_user = tk.StringVar(value=default_values["User"])
        self.var_pass = tk.StringVar(value=default_values["Password"])

        wrap = ttk.Frame(self)
        wrap.pack(fill="both", expand=True, padx=22, pady=22)

        hero = ttk.Frame(wrap, style="Card.TFrame", padding=18)
        hero.grid(row=0, column=0, sticky="nsew")
        hero.columnconfigure(0, weight=1)

        ttk.Label(hero, text="MedFlow", style="Title.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(hero, text="Step E - Login", style="Muted.TLabel").grid(row=1, column=0, sticky="w", pady=(2, 0))

        form = ttk.LabelFrame(wrap, text="Database Connection", padding=14)
        form.grid(row=1, column=0, sticky="nsew", pady=(14, 0))
        
        for i, (lbl, var, show) in enumerate(
            [
                ("Host", self.var_host, None),
                ("Port", self.var_port, None),
                ("Database", self.var_db, None),
                ("User", self.var_user, None),
                ("Password", self.var_pass, "*"),
            ]
        ):
            ttk.Label(form, text=lbl, style="H2.TLabel").grid(row=i, column=0, sticky="w", pady=6)
            e = ttk.Entry(form, textvariable=var, width=44, show=show)
            e.grid(row=i, column=1, sticky="w", pady=6, padx=(10, 0))
            
            # הזרקה ישירה לתוך הפקד כדי להבטיח הופעה של הטקסט
            e.delete(0, tk.END)
            e.insert(0, default_values[lbl])

        actions = ttk.Frame(wrap)
        actions.grid(row=2, column=0, sticky="w", pady=(14, 0))
        ttk.Button(actions, text="Connect", style="Primary.TButton", command=self._connect).grid(row=0, column=0, padx=(0, 10))
        ttk.Label(
            wrap,
            text="Tip: you can also set PGHOST / PGPORT / PGDATABASE / PGUSER / PGPASSWORD as environment variables.",
            style="Muted.TLabel",
        ).grid(row=3, column=0, sticky="w", pady=(10, 0))

        wrap.columnconfigure(0, weight=1)

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
        icons: dict[str, tk.PhotoImage],
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
        super().__init__(master, padding=0)
        self.conn = conn
        self.pk = pk
        self.select_sql = select_sql
        self.insert_sql = insert_sql
        self.update_sql = update_sql
        self.delete_sql = delete_sql
        self.fields = fields
        self.after_refresh = after_refresh
        self._title = title
        self._icons = icons

        wrap = ttk.Frame(self)
        wrap.pack(fill="both", expand=True, padx=16, pady=14)
        wrap.columnconfigure(0, weight=1)
        wrap.columnconfigure(1, weight=0)
        wrap.rowconfigure(4, weight=1)

        header = ttk.Frame(wrap, style="Card.TFrame", padding=(14, 12))
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        ttk.Label(header, text=title, style="H1.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(header, text="CRUD (Create / Read / Update / Delete)", style="Muted.TLabel").grid(
            row=1, column=0, sticky="w", pady=(2, 0)
        )

        top = ttk.LabelFrame(wrap, text="Update / Delete (Key)", padding=12)
        top.grid(row=1, column=0, sticky="ew", pady=(12, 0))

        # PK controls
        self.var_pk = tk.StringVar()
        ttk.Label(top, text=f"{pk_label}:", style="H2.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Entry(top, textvariable=self.var_pk, width=22).grid(row=0, column=1, sticky="w", padx=(10, 0))
        if pk_hint:
            ttk.Label(top, text=pk_hint, style="Muted.TLabel").grid(row=0, column=2, sticky="w", padx=(10, 0))

        # Form fields (scrollable)
        self.vars: dict[str, tk.StringVar] = {}

        # עטיפה עם גובה נעול כדי שהגלילה תופיע בפועל
        # (ה־height של ה־Canvas עצמו נקבע בנפרד ל־160, כדי למנוע גלילה שלא מופיעה בזמן)
        form_wrapper = ttk.Frame(wrap, height=220)
        form_wrapper.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        form_wrapper.grid_propagate(False)  # נועל את הגובה של הפריים
        form_wrapper.columnconfigure(0, weight=1)
        form_wrapper.rowconfigure(0, weight=1)

        form = ttk.LabelFrame(form_wrapper, text="Form", padding=12)
        form.grid(row=0, column=0, sticky="nsew")
        form.columnconfigure(0, weight=1)

        # Canvas מוגבל לגובה 160 כדי לכפות על פס גלילה כשיש יותר שורות
        _canvas = tk.Canvas(form, highlightthickness=0, bg=AppTheme.bg, height=160)
        _vsb = ttk.Scrollbar(form, orient="vertical", command=_canvas.yview, length=160)
        _canvas.configure(yscrollcommand=_vsb.set)
        # חשוב: לא למתוח אנכית את ה־Canvas, כדי להבטיח height=160 בפועל
        _canvas.grid(row=0, column=0, sticky="ew")
        _vsb.grid(row=0, column=1, sticky="ns")

        _inner = ttk.Frame(_canvas, style="TFrame")
        _window = _canvas.create_window((0, 0), window=_inner, anchor="nw")

        def _on_inner_config(event: tk.Event) -> None:
            # עדכון scrollregion כשה־inner משתנה (למשל שינוי גודל/תוכן)
            _canvas.configure(scrollregion=_canvas.bbox("all"))
            try:
                _canvas.itemconfigure(_window, width=_canvas.winfo_width())
            except Exception:
                pass

        _inner.bind("<Configure>", _on_inner_config)

        def _on_mousewheel(event: tk.Event) -> None:
            delta = 0
            if event.num == 5 or event.delta < 0:
                delta = 1
            elif event.num == 4 or event.delta > 0:
                delta = -1
            _canvas.yview_scroll(delta, "units")

        _canvas.bind("<Enter>", lambda e: _canvas.bind_all("<MouseWheel>", _on_mousewheel))
        _canvas.bind("<Leave>", lambda e: _canvas.unbind_all("<MouseWheel>"))

        for i, (lbl, col) in enumerate(fields):
            self.vars[col] = tk.StringVar()
            ttk.Label(_inner, text=lbl, style="H2.TLabel").grid(
                row=i, column=0, sticky="w", pady=6
            )
            ttk.Entry(
                _inner,
                textvariable=self.vars[col],
                width=56,
            ).grid(row=i, column=1, sticky="w", pady=6, padx=(10, 0))

        # חשוב: אחרי שכל השדות נוצרו
        _inner.update_idletasks()
        _canvas.configure(scrollregion=_canvas.bbox("all"))
        _canvas.update_idletasks()

        btns = ttk.Frame(wrap)
        btns.grid(row=3, column=0, sticky="w", pady=(12, 0))
        ttk.Button(
            btns,
            text="Refresh",
            image=self._icons["refresh"],
            compound="left",
            style="Primary.TButton",
            command=self.refresh,
        ).grid(row=0, column=0, padx=(0, 10))
        ttk.Button(
            btns,
            text="Insert",
            image=self._icons["plus"],
            compound="left",
            style="Success.TButton",
            command=self.insert,
        ).grid(row=0, column=1, padx=(0, 10))
        ttk.Button(
            btns,
            text="Fetch by Key",
            image=self._icons["key"],
            compound="left",
            command=self.fetch_by_key,
        ).grid(row=0, column=2, padx=(0, 10))
        ttk.Button(
            btns,
            text="Update",
            image=self._icons["pencil"],
            compound="left",
            style="Primary.TButton",
            command=self.update,
        ).grid(row=0, column=3, padx=(0, 10))
        ttk.Button(
            btns,
            text="Delete",
            image=self._icons["trash"],
            compound="left",
            style="Danger.TButton",
            command=self.delete,
        ).grid(row=0, column=4, padx=(0, 10))

        # Results
        res = ttk.LabelFrame(wrap, text="Results", padding=10)
        res.grid(row=4, column=0, sticky="nsew", pady=(12, 0))

        self.tree = ttk.Treeview(res, columns=(), show="headings", height=14)
        vsb = ttk.Scrollbar(res, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(res, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")
        hsb.grid(row=1, column=0, sticky="ew")
        res.columnconfigure(0, weight=1)
        res.rowconfigure(0, weight=1)

        # Side panel: stats & guidance
        side = ttk.Frame(wrap, style="Card.TFrame", padding=12)
        side.grid(row=1, column=1, rowspan=4, sticky="nsew", padx=(12, 0))
        ttk.Label(side, text="Panel", style="H2.TLabel").grid(row=0, column=0, sticky="w")
        self.lbl_stats = ttk.Label(side, text="Rows: -", style="Big.TLabel")
        self.lbl_stats.grid(row=1, column=0, sticky="w", pady=(10, 0))
        ttk.Separator(side).grid(row=2, column=0, sticky="ew", pady=12)
        ttk.Label(side, text="How to update", style="H2.TLabel").grid(row=3, column=0, sticky="w")
        ttk.Label(
            side,
            text="1) Enter the key\n2) Click Fetch by Key\n3) Edit fields\n4) Click Update",
            style="Muted.TLabel",
            justify="left",
        ).grid(row=4, column=0, sticky="w", pady=(6, 0))
        ttk.Separator(side).grid(row=5, column=0, sticky="ew", pady=12)
        ttk.Label(side, text="Tip", style="H2.TLabel").grid(row=6, column=0, sticky="w")
        ttk.Label(
            side,
            text="Results hide IDs.\nForeign keys are shown as names using JOINs.",
            style="Muted.TLabel",
            justify="left",
        ).grid(row=7, column=0, sticky="w", pady=(6, 0))

        wrap.columnconfigure(0, weight=1)
        wrap.rowconfigure(4, weight=1)

        self.refresh()

    def _set_tree(self, rows: list[dict[str, Any]]) -> None:
        self.tree.delete(*self.tree.get_children())
        if not rows:
            self.tree["columns"] = ("message",)
            self.tree.heading("message", text="message")
            self.tree.column("message", width=600, anchor="w")
            self.tree.insert("", "end", values=("No rows",))
            self.lbl_stats.configure(text="Rows: 0")
            return

        cols = list(rows[0].keys())
        self.tree["columns"] = cols
        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140, anchor="w")
        self.tree.tag_configure("odd", background=AppTheme.zebra_1)
        self.tree.tag_configure("even", background=AppTheme.zebra_2)
        for i, r in enumerate(rows):
            tag = "even" if i % 2 == 0 else "odd"
            self.tree.insert("", "end", values=[r.get(c) for c in cols], tags=(tag,))
        self.lbl_stats.configure(text=f"Rows: {len(rows)}")

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
    def __init__(self, master: tk.Widget, conn: PGConnection, icons: dict[str, tk.PhotoImage]) -> None:
        super().__init__(master, padding=0)
        self.conn = conn
        self._icons = icons

        wrap = ttk.Frame(self)
        wrap.pack(fill="both", expand=True, padx=16, pady=14)
        wrap.columnconfigure(1, weight=1)
        wrap.rowconfigure(2, weight=1)

        header = ttk.Frame(wrap, style="Card.TFrame", padding=(14, 12))
        header.grid(row=0, column=0, columnspan=2, sticky="ew")
        ttk.Label(header, text="Queries & Programs", style="H1.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(header, text="Run Step B queries and Step D programs", style="Muted.TLabel").grid(row=1, column=0, sticky="w")

        left = ttk.Frame(wrap)
        left.grid(row=2, column=0, sticky="nsw", pady=(12, 0))

        # Step B queries (2)
        qbox = ttk.LabelFrame(left, text="Step B Queries", padding=10)
        qbox.grid(row=0, column=0, sticky="ew")
        ttk.Button(
            qbox,
            text="Query 1: Admissions in 2024",
            image=self._icons["doc"],
            compound="left",
            style="Primary.TButton",
            command=self._q1,
        ).grid(
            row=0, column=0, sticky="w", pady=4
        )
        ttk.Button(
            qbox,
            text="Query 2: Severe-allergy per year",
            image=self._icons["doc"],
            compound="left",
            style="Primary.TButton",
            command=self._q2,
        ).grid(
            row=1, column=0, sticky="w", pady=4
        )

        # Step D programs (at least 2)
        pbox = ttk.LabelFrame(left, text="Step D Programs", padding=10)
        pbox.grid(row=1, column=0, sticky="ew", pady=(10, 0))

        self.var_patient_id = tk.StringVar(value="42001")
        ttk.Label(pbox, text="patient_id:", style="H2.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Entry(pbox, textvariable=self.var_patient_id, width=18).grid(row=0, column=1, sticky="w", padx=(8, 0))
        ttk.Button(
            pbox,
            text="Run fn_patient_risk_score",
            image=self._icons["play"],
            compound="left",
            style="Success.TButton",
            command=self._run_risk,
        ).grid(
            row=0, column=2, sticky="w", padx=(12, 0)
        )

        self.var_days = tk.StringVar(value="60")
        ttk.Label(pbox, text="days:", style="H2.TLabel").grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Entry(pbox, textvariable=self.var_days, width=18).grid(row=1, column=1, sticky="w", padx=(8, 0), pady=(8, 0))
        ttk.Button(
            pbox,
            text="Call sp_close_long_open_admissions",
            image=self._icons["play"],
            compound="left",
            style="Warn.TButton",
            command=self._call_close,
        ).grid(
            row=1, column=2, sticky="w", padx=(12, 0), pady=(8, 0)
        )

        # Output
        outbox = ttk.LabelFrame(wrap, text="Output", padding=10)
        outbox.grid(row=2, column=1, sticky="nsew", padx=(12, 0), pady=(12, 0))
        self.txt = tk.Text(outbox, height=28, wrap="none", bg=AppTheme.card, fg=AppTheme.text, relief="flat")
        ysb = ttk.Scrollbar(outbox, orient="vertical", command=self.txt.yview)
        xsb = ttk.Scrollbar(outbox, orient="horizontal", command=self.txt.xview)
        self.txt.configure(yscrollcommand=ysb.set, xscrollcommand=xsb.set)
        self.txt.grid(row=0, column=0, sticky="nsew")
        ysb.grid(row=0, column=1, sticky="ns")
        xsb.grid(row=1, column=0, sticky="ew")
        outbox.columnconfigure(0, weight=1)
        outbox.rowconfigure(0, weight=1)

        wrap.columnconfigure(0, weight=0)
        wrap.columnconfigure(1, weight=1)
        wrap.rowconfigure(2, weight=1)

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
        self._root = master.winfo_toplevel()
        apply_theme(self._root)  # global ttk styles

        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self._nav_buttons: dict[str, ttk.Button] = {}
        self._content: Optional[ttk.Frame] = None
        self._icons: dict[str, tk.PhotoImage] = {}

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
        root = ttk.Frame(self.container)
        root.pack(fill="both", expand=True)
        root.columnconfigure(1, weight=1)
        root.rowconfigure(0, weight=1)

        # Sidebar
        sidebar = ttk.Frame(root, style="Sidebar.TFrame", padding=(14, 14))
        sidebar.grid(row=0, column=0, sticky="nsw")

        ttk.Label(sidebar, text="MedFlow", style="SidebarTitle.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(sidebar, text="Step E - GUI", style="SidebarMuted.TLabel").grid(row=1, column=0, sticky="w", pady=(2, 14))

        nav = ttk.Frame(sidebar, style="Sidebar.TFrame")
        nav.grid(row=2, column=0, sticky="nsew")

        # Content area
        content_host = ttk.Frame(root)
        content_host.grid(row=0, column=1, sticky="nsew")
        content_host.rowconfigure(1, weight=1)
        content_host.columnconfigure(0, weight=1)

        topbar = ttk.Frame(content_host, style="Card.TFrame", padding=(16, 12))
        topbar.grid(row=0, column=0, sticky="ew", padx=16, pady=(14, 0))
        self.lbl_top = ttk.Label(topbar, text="Dashboard", style="H1.TLabel")
        self.lbl_top.grid(row=0, column=0, sticky="w")
        ttk.Label(topbar, text="Navigation on the left • Results hide IDs • FK shown as names", style="Muted.TLabel").grid(
            row=1, column=0, sticky="w", pady=(2, 0)
        )

        self._content = ttk.Frame(content_host)
        self._content.grid(row=1, column=0, sticky="nsew")

        # Icons (keep references!)
        bg = AppTheme.sidebar_card
        self._icons = {
            "home": IconFactory.home(bg),
            "users": IconFactory.users(bg),
            "calendar": IconFactory.calendar(bg),
            "alert": IconFactory.alert(bg),
            "shield": IconFactory.shield(bg),
            "phone": IconFactory.phone(bg),
            "doc": IconFactory.doc(bg),
            "play": IconFactory.play(bg),
            "refresh": IconFactory.refresh(AppTheme.card),
            "plus": IconFactory.plus(AppTheme.card),
            "pencil": IconFactory.pencil(AppTheme.card),
            "trash": IconFactory.trash(AppTheme.card),
            "key": IconFactory.key(AppTheme.card),
        }

        def add_nav(key: str, label: str, cmd: Callable[[], None]) -> None:
            icon = self._icons.get(key)
            btn = ttk.Button(nav, text=label, image=icon, compound="left", style="Nav.TButton", command=cmd)
            btn.grid(sticky="ew", pady=6)
            self._nav_buttons[key] = btn

        def set_active(key: str) -> None:
            for k, b in self._nav_buttons.items():
                b.configure(style="NavActive.TButton" if k == key else "Nav.TButton")

        def show(frame: ttk.Frame, title: str, key: str) -> None:
            for w in self._content.winfo_children():
                w.destroy()
            frame.pack(fill="both", expand=True)
            self.lbl_top.configure(text=title)
            set_active(key)

        # Frames (build once)
        patients = TableCrudFrame(
            self._content,
            self.conn,
            title="Patients",
            icons=self._icons,
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
        )

        admissions = TableCrudFrame(
            self._content,
            self.conn,
            title="Admissions",
            icons=self._icons,
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
        )

        allergies = TableCrudFrame(
            self._content,
            self.conn,
            title="Patient Allergies",
            icons=self._icons,
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
        )

        insurance = TableCrudFrame(
            self._content,
            self.conn,
            title="Patient Insurance",
            icons=self._icons,
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
        )

        history = TableCrudFrame(
            self._content,
            self.conn,
            title="Medical History",
            icons=self._icons,
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
        )

        contacts = TableCrudFrame(
            self._content,
            self.conn,
            title="Emergency Contacts",
            icons=self._icons,
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
        )

        qp = QueriesAndProgramsFrame(self._content, self.conn, self._icons)

        # Dashboard
        dash = ttk.Frame(self._content, padding=16)
        card = ttk.Frame(dash, style="Card.TFrame", padding=18)
        card.pack(fill="x", pady=(8, 0))
        ttk.Label(card, text="Welcome", style="H1.TLabel").pack(anchor="w")
        ttk.Label(
            card,
            text="Use the navigation on the left to manage all tables (CRUD), run queries, and run Step D programs.",
            style="Big.TLabel",
            wraplength=760,
            justify="left",
        ).pack(anchor="w", pady=(8, 0))

        add_nav("home", "Dashboard", lambda: show(dash, "Dashboard", "home"))
        add_nav("users", "Patients", lambda: show(patients, "Patients", "users"))
        add_nav("calendar", "Admissions", lambda: show(admissions, "Admissions", "calendar"))
        add_nav("alert", "Allergies", lambda: show(allergies, "Allergies", "alert"))
        add_nav("shield", "Insurance", lambda: show(insurance, "Insurance", "shield"))
        add_nav("doc", "Medical History", lambda: show(history, "Medical History", "doc"))
        add_nav("phone", "Emergency Contacts", lambda: show(contacts, "Emergency Contacts", "phone"))
        add_nav("play", "Queries & Programs", lambda: show(qp, "Queries & Programs", "play"))

        ttk.Separator(sidebar).grid(row=3, column=0, sticky="ew", pady=14)
        ttk.Button(sidebar, text="Logout", style="Nav.TButton", command=self._show_login).grid(row=4, column=0, sticky="ew")

        # default view
        show(dash, "Dashboard", "home")

        # NOTE: Old Notebook-based navigation was replaced by Sidebar navigation above.
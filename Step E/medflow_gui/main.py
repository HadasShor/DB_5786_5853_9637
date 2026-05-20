from __future__ import annotations

import customtkinter as ctk

from .modern_ui import ModernMedFlowApp


def main() -> None:
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("MedFlow - GUI (Step E)")
    root.geometry("1280x760")
    root.minsize(1180, 700)
    ModernMedFlowApp(root).pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()


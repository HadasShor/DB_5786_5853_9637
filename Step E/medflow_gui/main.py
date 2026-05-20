from __future__ import annotations

import tkinter as tk

from .ui import MedFlowApp


def main() -> None:
    root = tk.Tk()
    root.title("MedFlow - GUI (Step E)")
    root.geometry("1150x720")
    root.minsize(1050, 650)
    MedFlowApp(root).pack(fill="both", expand=True)
    root.mainloop()


if __name__ == "__main__":
    main()


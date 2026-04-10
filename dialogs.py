import tkinter as tk
from tkinter import ttk, messagebox

import chess


def open_load_fen_dialog(parent, current_fen: str, apply_callback):
  win = tk.Toplevel(parent)
  win.title("Load FEN")
  win.geometry("700x180")
  win.transient(parent)
  win.grab_set()

  fen_var = tk.StringVar(value=current_fen)
  ttk.Label(win, text="Paste a valid FEN:").pack(anchor="w", padx=12, pady=(12, 4))
  entry = ttk.Entry(win, textvariable=fen_var, width=100)
  entry.pack(fill=tk.X, padx=12)
  entry.focus_set()

  def apply_fen():
    fen = fen_var.get().strip()
    try:
      chess.Board(fen)
    except ValueError as exc:
      messagebox.showerror("Invalid FEN", str(exc), parent=win)
      return
    apply_callback(fen)
    win.destroy()

  btns = ttk.Frame(win)
  btns.pack(fill=tk.X, padx=12, pady=12)
  ttk.Button(btns, text="Apply", command=apply_fen).pack(side=tk.LEFT)
  ttk.Button(btns, text="Cancel", command=win.destroy).pack(side=tk.LEFT, padx=8)

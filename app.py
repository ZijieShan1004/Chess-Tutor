import tkinter as tk
from tkinter import ttk, filedialog, messagebox

import chess

from analysis_formatter import format_analysis
from board_view import display_to_square, draw_board
from constants import BOARD_SIZE, DEFAULT_ANALYSIS_TIME, DEFAULT_TOP_N, SQUARE_SIZE
from dialogs import open_load_fen_dialog
from engine_service import analyze_position, close_engine, load_engine, validate_engine_path


class ChessTutorApp:
  def __init__(self, root: tk.Tk):
    self.root = root
    self.root.title("Chess Tutor with Stockfish")
    self.root.geometry("1200x780")

    self.board = chess.Board()
    self.engine = None

    self.user_side = chess.WHITE
    self.selected_square = None
    self.legal_targets = []

    self.engine_path_var = tk.StringVar(value="")
    self.analysis_time_var = tk.StringVar(value=str(DEFAULT_ANALYSIS_TIME))
    self.top_n_var = tk.StringVar(value=str(DEFAULT_TOP_N))
    self.status_var = tk.StringVar(value="Please load Stockfish first.")

    self.turn_var = tk.StringVar()
    self.fen_var = tk.StringVar()
    self.moves_var = tk.StringVar()

    self._build_ui()
    self._refresh_all()

  def _build_ui(self):
    main = ttk.Frame(self.root, padding=10)
    main.pack(fill=tk.BOTH, expand=True)

    left = ttk.Frame(main)
    left.pack(side=tk.LEFT, fill=tk.Y)

    right = ttk.Frame(main)
    right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(14, 0))

    self.canvas = tk.Canvas(
      left,
      width=BOARD_SIZE,
      height=BOARD_SIZE,
      bg="white",
      highlightthickness=1,
    )
    self.canvas.pack()
    self.canvas.bind("<Button-1>", self._on_canvas_click)

    controls = ttk.Frame(left, padding=(0, 10, 0, 0))
    controls.pack(fill=tk.X)

    engine_frame = ttk.LabelFrame(controls, text="Engine", padding=10)
    engine_frame.pack(fill=tk.X)

    ttk.Label(engine_frame, text="Stockfish path:").grid(row=0, column=0, sticky="w")
    ttk.Entry(
      engine_frame,
      textvariable=self.engine_path_var,
      width=48,
    ).grid(row=1, column=0, sticky="ew", padx=(0, 8), pady=(4, 6))
    ttk.Button(engine_frame, text="Browse", command=self._browse_engine).grid(
      row=1, column=1, sticky="ew", pady=(4, 6)
    )
    ttk.Button(engine_frame, text="Load Engine", command=self.load_engine_action).grid(
      row=2, column=0, columnspan=2, sticky="ew"
    )
    engine_frame.columnconfigure(0, weight=1)

    game_frame = ttk.LabelFrame(controls, text="Game Controls", padding=10)
    game_frame.pack(fill=tk.X, pady=(10, 0))

    side_row = ttk.Frame(game_frame)
    side_row.pack(fill=tk.X)
    ttk.Label(side_row, text="Main operator side:").pack(side=tk.LEFT)
    ttk.Button(
      side_row,
      text="White",
      command=lambda: self.set_user_side(chess.WHITE),
    ).pack(side=tk.LEFT, padx=(8, 4))
    ttk.Button(
      side_row,
      text="Black",
      command=lambda: self.set_user_side(chess.BLACK),
    ).pack(side=tk.LEFT)

    button_row = ttk.Frame(game_frame)
    button_row.pack(fill=tk.X, pady=(8, 0))
    ttk.Button(button_row, text="New Game", command=self.new_game).pack(
      side=tk.LEFT, fill=tk.X, expand=True
    )
    ttk.Button(button_row, text="Undo", command=self.undo_move).pack(
      side=tk.LEFT, fill=tk.X, expand=True, padx=6
    )
    ttk.Button(button_row, text="Flip Board", command=self.flip_side).pack(
      side=tk.LEFT, fill=tk.X, expand=True
    )

    misc_row = ttk.Frame(game_frame)
    misc_row.pack(fill=tk.X, pady=(8, 0))
    ttk.Button(misc_row, text="Load FEN", command=self.load_fen_dialog).pack(
      side=tk.LEFT, fill=tk.X, expand=True
    )
    ttk.Button(misc_row, text="Copy FEN", command=self.copy_fen).pack(
      side=tk.LEFT, fill=tk.X, expand=True, padx=6
    )
    ttk.Button(misc_row, text="Reset Selection", command=self.reset_selection).pack(
      side=tk.LEFT, fill=tk.X, expand=True
    )

    analysis_frame = ttk.LabelFrame(controls, text="Analysis", padding=10)
    analysis_frame.pack(fill=tk.X, pady=(10, 0))

    row1 = ttk.Frame(analysis_frame)
    row1.pack(fill=tk.X)
    ttk.Label(row1, text="Time per analysis (sec):").pack(side=tk.LEFT)
    ttk.Entry(row1, textvariable=self.analysis_time_var, width=8).pack(
      side=tk.LEFT, padx=(8, 14)
    )
    ttk.Label(row1, text="Top N:").pack(side=tk.LEFT)
    ttk.Entry(row1, textvariable=self.top_n_var, width=6).pack(
      side=tk.LEFT, padx=(8, 0)
    )

    row2 = ttk.Frame(analysis_frame)
    row2.pack(fill=tk.X, pady=(8, 0))
    ttk.Button(
      row2,
      text="Suggest Best Moves",
      command=self.analyze_position_action,
    ).pack(side=tk.LEFT, fill=tk.X, expand=True)

    ttk.Label(
      controls,
      textvariable=self.status_var,
      foreground="#1f4e79",
      wraplength=620,
    ).pack(fill=tk.X, pady=(10, 0))

    summary_frame = ttk.LabelFrame(right, text="Position Summary", padding=10)
    summary_frame.pack(fill=tk.X)

    ttk.Label(summary_frame, textvariable=self.turn_var, font=("Arial", 13, "bold")).pack(anchor="w")
    ttk.Label(summary_frame, text="FEN:").pack(anchor="w", pady=(8, 0))
    ttk.Label(summary_frame, textvariable=self.fen_var, wraplength=500, font=("Consolas", 10)).pack(anchor="w")
    ttk.Label(summary_frame, text="Moves:").pack(anchor="w", pady=(8, 0))
    ttk.Label(summary_frame, textvariable=self.moves_var, wraplength=500, font=("Consolas", 10)).pack(anchor="w")

    analysis_box = ttk.LabelFrame(right, text="Best Move Suggestions", padding=10)
    analysis_box.pack(fill=tk.BOTH, expand=True, pady=(12, 0))

    self.analysis_text = tk.Text(
      analysis_box,
      wrap=tk.WORD,
      height=30,
      font=("Consolas", 11),
    )
    self.analysis_text.pack(fill=tk.BOTH, expand=True)
    self.analysis_text.config(state=tk.DISABLED)

  def _draw_board(self):
    draw_board(
      self.canvas,
      self.board,
      self.user_side,
      self.selected_square,
      self.legal_targets,
    )

  def _on_canvas_click(self, event):
    display_file = event.x // SQUARE_SIZE
    display_rank = event.y // SQUARE_SIZE

    if not (0 <= display_file < 8 and 0 <= display_rank < 8):
      return

    clicked_square = display_to_square(self.user_side, display_file, display_rank)
    piece = self.board.piece_at(clicked_square)

    if self.selected_square is None:
      if piece is None:
        return
      self.selected_square = clicked_square
      self.legal_targets = self._legal_targets_from(clicked_square)
      self._draw_board()
      return

    if clicked_square == self.selected_square:
      self.reset_selection()
      return

    move = self._build_move(self.selected_square, clicked_square)
    if move and move in self.board.legal_moves:
      self.board.push(move)
      self.reset_selection(redraw=False)
      self._refresh_all()
      return

    if piece is not None:
      self.selected_square = clicked_square
      self.legal_targets = self._legal_targets_from(clicked_square)
    else:
      self.reset_selection(redraw=False)

    self._draw_board()

  def _build_move(self, from_square: chess.Square, to_square: chess.Square):
    moving_piece = self.board.piece_at(from_square)
    if moving_piece is None:
      return None

    if moving_piece.piece_type == chess.PAWN:
      target_rank = chess.square_rank(to_square)
      if target_rank == 0 or target_rank == 7:
        return chess.Move(from_square, to_square, promotion=chess.QUEEN)

    return chess.Move(from_square, to_square)

  def _legal_targets_from(self, from_square: chess.Square):
    return [
      move.to_square
      for move in self.board.legal_moves
      if move.from_square == from_square
    ]

  def new_game(self):
    self.board.reset()
    self.reset_selection(redraw=False)
    self._refresh_all()
    self._set_analysis_text("New game started.\n")
    self.status_var.set("New game started.")

  def undo_move(self):
    if not self.board.move_stack:
      self.status_var.set("No move to undo.")
      return
    self.board.pop()
    self.reset_selection(redraw=False)
    self._refresh_all()
    self.status_var.set("Last move undone.")

  def set_user_side(self, side: chess.Color):
    self.user_side = side
    self._draw_board()
    self.status_var.set(f"Main operator side set to {'White' if side == chess.WHITE else 'Black'}.")

  def flip_side(self):
    self.user_side = not self.user_side
    self._draw_board()
    self.status_var.set(f"Board flipped. Main operator side is now {'White' if self.user_side == chess.WHITE else 'Black'}.")

  def reset_selection(self, redraw=True):
    self.selected_square = None
    self.legal_targets = []
    if redraw:
      self._draw_board()

  def load_fen_dialog(self):
    open_load_fen_dialog(self.root, self.board.fen(), self.apply_fen)

  def apply_fen(self, fen: str):
    self.board = chess.Board(fen)
    self.reset_selection(redraw=False)
    self._refresh_all()
    self.status_var.set("FEN loaded successfully.")

  def copy_fen(self):
    self.root.clipboard_clear()
    self.root.clipboard_append(self.board.fen())
    self.status_var.set("Current FEN copied to clipboard.")

  def _browse_engine(self):
    path = filedialog.askopenfilename(title="Choose Stockfish executable")
    if path:
      self.engine_path_var.set(path)

  def load_engine_action(self):
    path = self.engine_path_var.get().strip()
    is_valid, message = validate_engine_path(path)
    if not is_valid:
      if "does not exist" in message:
        messagebox.showerror("File not found", message)
      else:
        messagebox.showwarning("Missing path", message)
      return

    try:
      self.engine = load_engine(self.engine, path)
      self.status_var.set("Stockfish loaded successfully.")
      self._set_analysis_text(
        "Engine loaded successfully.\n"
        "Now click 'Suggest Best Moves' to analyze the current position.\n"
      )
    except Exception as exc:
      self.engine = None
      messagebox.showerror("Engine load failed", f"Could not start Stockfish.\n\n{exc}")

  def analyze_position_action(self):
    if self.engine is None:
      messagebox.showwarning("Engine not loaded", "Load Stockfish before analyzing.")
      return

    try:
      analysis_time = float(self.analysis_time_var.get().strip())
      top_n = int(self.top_n_var.get().strip())
      if analysis_time <= 0 or top_n <= 0:
        raise ValueError
    except ValueError:
      messagebox.showerror("Invalid analysis settings", "Time must be positive and Top N must be a positive integer.")
      return

    self.status_var.set("Running analysis...")
    self.root.update_idletasks()

    try:
      info_list = analyze_position(self.engine, self.board, analysis_time, top_n)
      text = format_analysis(self.board, info_list)
      self._set_analysis_text(text)
      self.status_var.set("Analysis complete.")
    except Exception as exc:
      messagebox.showerror("Analysis failed", str(exc))
      self.status_var.set("Analysis failed.")

  def _refresh_all(self):
    self._draw_board()
    self._update_labels()

  def _update_labels(self):
    turn_name = "White" if self.board.turn == chess.WHITE else "Black"
    check_text = " | Check" if self.board.is_check() else ""
    result_text = self._position_result_label()
    self.turn_var.set(f"Turn: {turn_name}{check_text}{result_text}")
    self.fen_var.set(self.board.fen())
    self.moves_var.set(self._move_list_string())

  def _position_result_label(self):
    if self.board.is_checkmate():
      winner = "Black" if self.board.turn == chess.WHITE else "White"
      return f" | Checkmate, {winner} wins"
    if self.board.is_stalemate():
      return " | Stalemate"
    if self.board.is_insufficient_material():
      return " | Draw by insufficient material"
    return ""

  def _move_list_string(self):
    replay_board = chess.Board()
    parts = []
    for move in self.board.move_stack:
      if replay_board.turn == chess.WHITE:
        parts.append(f"{replay_board.fullmove_number}.")
      try:
        parts.append(replay_board.san(move))
      except Exception:
        parts.append(move.uci())
      replay_board.push(move)
    return " ".join(parts) if parts else "(no moves yet)"

  def _set_analysis_text(self, text: str):
    self.analysis_text.config(state=tk.NORMAL)
    self.analysis_text.delete("1.0", tk.END)
    self.analysis_text.insert(tk.END, text)
    self.analysis_text.config(state=tk.DISABLED)

  def shutdown(self):
    close_engine(self.engine)
    self.root.destroy()

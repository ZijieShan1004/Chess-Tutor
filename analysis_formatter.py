import chess

from constants import PV_PREVIEW_PLIES


def format_analysis(board: chess.Board, info_list):
  if not info_list:
    return "No analysis result was returned by Stockfish.\n"

  lines = []
  side_to_move = "White" if board.turn == chess.WHITE else "Black"
  lines.append(f"Side to move: {side_to_move}")
  lines.append(f"Current FEN: {board.fen()}")
  lines.append("")

  for idx, info in enumerate(info_list, start=1):
    pv = info.get("pv", [])
    best_move = pv[0] if pv else None

    move_uci = best_move.uci() if best_move else "N/A"
    move_san = safe_san(board, move=best_move)
    score_text = format_score(board, info.get("score"))
    depth_text = str(info.get("depth", "?"))
    nodes_text = str(info.get("nodes", "?"))
    pv_text = format_pv(board, pv)
    note = basic_teaching_hint(board, best_move)

    lines.append(f"#{idx}")
    lines.append(f"Move (UCI): {move_uci}")
    lines.append(f"Move (SAN): {move_san}")
    lines.append(f"Evaluation: {score_text}")
    lines.append(f"Depth: {depth_text}")
    lines.append(f"Nodes: {nodes_text}")
    lines.append(f"PV: {pv_text}")
    lines.append(f"Teaching note: {note}")
    lines.append("")

  return "\n".join(lines)


def format_score(board: chess.Board, score_obj):
  if score_obj is None:
    return "Unavailable"

  pov_score = score_obj.pov(board.turn)
  mate = pov_score.mate()

  if mate is not None:
    if mate > 0:
      return f"Mate in {mate} for side to move"
    return f"Side to move gets mated in {abs(mate)}"

  cp = pov_score.score()
  if cp is None:
    return "Unavailable"

  return f"{cp / 100.0:+.2f} pawns for side to move"


def format_pv(board: chess.Board, pv_moves):
  if not pv_moves:
    return "Unavailable"

  preview_board = board.copy()
  san_moves = []

  for move in pv_moves[:PV_PREVIEW_PLIES]:
    try:
      san_moves.append(preview_board.san(move))
      preview_board.push(move)
    except Exception:
      san_moves.append(move.uci())
      break

  return " ".join(san_moves)


def safe_san(board: chess.Board, move):
  if move is None:
    return "N/A"
  temp = board.copy()
  try:
    return temp.san(move)
  except Exception:
    return move.uci()


def basic_teaching_hint(board: chess.Board, move):
  if move is None:
    return "No teaching note available."

  piece = board.piece_at(move.from_square)
  if piece is None:
    return "No teaching note available."

  target = move.to_square
  center = {chess.D4, chess.E4, chess.D5, chess.E5}

  if piece.piece_type == chess.KING and abs(
    chess.square_file(move.from_square) - chess.square_file(move.to_square)
  ) == 2:
    return "This move castles and usually improves king safety."

  if piece.piece_type in {chess.KNIGHT, chess.BISHOP} and board.fullmove_number <= 8:
    return "This develops a minor piece, which is usually good in the opening."

  if piece.piece_type == chess.PAWN and target in center:
    return "This move fights for central control."

  if board.is_capture(move):
    return "This move captures material or removes a defender."

  return "This move is favored by the engine in the current position."

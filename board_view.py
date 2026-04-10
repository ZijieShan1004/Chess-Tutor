import chess

from constants import (
  BOARD_SIZE,
  DARK_COLOR,
  LIGHT_COLOR,
  SELECT_COLOR,
  SQUARE_SIZE,
  TARGET_COLOR,
  UNICODE_PIECES,
)


def display_to_square(user_side: chess.Color, display_file: int, display_rank: int) -> chess.Square:
  if user_side == chess.WHITE:
    board_file = display_file
    board_rank = 7 - display_rank
  else:
    board_file = 7 - display_file
    board_rank = display_rank
  return chess.square(board_file, board_rank)


def draw_board(canvas, board: chess.Board, user_side: chess.Color, selected_square, legal_targets):
  canvas.delete("all")
  for display_rank in range(8):
    for display_file in range(8):
      square = display_to_square(user_side, display_file, display_rank)
      x1 = display_file * SQUARE_SIZE
      y1 = display_rank * SQUARE_SIZE
      x2 = x1 + SQUARE_SIZE
      y2 = y1 + SQUARE_SIZE

      color = LIGHT_COLOR if (display_file + display_rank) % 2 == 0 else DARK_COLOR

      if selected_square == square:
        color = SELECT_COLOR
      elif square in legal_targets:
        color = TARGET_COLOR

      canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

      piece = board.piece_at(square)
      if piece:
        canvas.create_text(
          x1 + SQUARE_SIZE // 2,
          y1 + SQUARE_SIZE // 2,
          text=UNICODE_PIECES[piece.symbol()],
          font=("Arial", 34),
        )

      if display_rank == 7:
        canvas.create_text(
          x1 + SQUARE_SIZE - 10,
          y2 - 10,
          text=chess.square_name(square)[0],
          font=("Arial", 9),
          fill="#333333",
        )

      if display_file == 0:
        canvas.create_text(
          x1 + 10,
          y1 + 10,
          text=chess.square_name(square)[1],
          font=("Arial", 9),
          fill="#333333",
        )

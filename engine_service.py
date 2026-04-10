import os

import chess.engine


def validate_engine_path(path: str):
  if not path:
    return False, "Please choose the Stockfish executable first."
  if not os.path.exists(path):
    return False, "The specified Stockfish path does not exist."
  return True, ""


def load_engine(existing_engine, path: str):
  if existing_engine is not None:
    try:
      existing_engine.quit()
    except Exception:
      pass
  return chess.engine.SimpleEngine.popen_uci(path)


def analyze_position(engine, board, analysis_time: float, top_n: int):
  limit = chess.engine.Limit(time=analysis_time)
  return engine.analyse(
    board,
    limit,
    multipv=top_n,
    info=chess.engine.INFO_ALL,
  )


def close_engine(engine):
  if engine is not None:
    try:
      engine.quit()
    except Exception:
      pass

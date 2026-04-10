# Chess Tutor

A modular Tkinter chess tutor app backed by Stockfish.

## Files

- `main.py`: program entry point
- `app.py`: main application controller and UI wiring
- `constants.py`: shared constants
- `engine_service.py`: Stockfish load/analyze/close helpers
- `analysis_formatter.py`: engine output formatting helpers
- `board_view.py`: board drawing and display-coordinate conversion
- `dialogs.py`: dialog windows

## Run

```bash
python -m pip install python-chess
python main.py
```

# Chess Tutor

Chess Tutor is a local desktop chess tutoring application built with Python, Tkinter, `python-chess`, and Stockfish. It provides an interactive chessboard where users can move pieces according to the rules of chess, inspect the current position, undo moves, switch board perspective, and request engine-based move suggestions for learning and analysis.

This project is designed as a lightweight educational tool rather than a full competitive chess GUI. Its main purpose is to help users understand positions and learn stronger candidate moves from the current board state.

## Features

- Interactive chessboard GUI built with Tkinter
- Legal move validation based on official chess rules
- Piece movement for both sides
- Undo the last move
- Start a new game
- Flip board orientation
- Choose White-side or Black-side main view
- Load a custom position from FEN
- Copy the current position FEN to the clipboard
- Connect to a local Stockfish engine executable
- Analyze the current position using Stockfish
- Show the top recommended moves
- Display evaluation, search depth, nodes, PV line, and a simple teaching note

## Project Purpose

This project is intended for:

- chess learners who want immediate move recommendations from a strong engine
- students building a Python desktop application with a real external engine
- developers interested in combining GUI programming with chess logic and engine integration
- portfolio use as a practical AI-assisted chess tutoring tool

The application does not train a chess model from data. Instead, it relies on the chess rules through `python-chess` and uses Stockfish as the external evaluation engine.

## Tech Stack

- Python 3
- Tkinter
- `python-chess`
- Stockfish (local executable)

## Project Structure

```text
chess_tutor/
  main.py
  app.py
  constants.py
  engine_service.py
  analysis_formatter.py
  board_view.py
  dialogs.py

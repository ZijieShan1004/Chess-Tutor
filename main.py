import tkinter as tk

from app import ChessTutorApp


def main():
  root = tk.Tk()
  app = ChessTutorApp(root)
  root.protocol("WM_DELETE_WINDOW", app.shutdown)
  root.mainloop()


if __name__ == "__main__":
  main()

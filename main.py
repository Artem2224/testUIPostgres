from tkinter import Tk
from ui.app import DBApp
from utils.logging_config import setup_logging

def main():
    setup_logging()
    root = Tk()
    app = DBApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
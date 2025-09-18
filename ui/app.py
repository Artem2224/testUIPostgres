import logging
from tkinter import ttk, Label, Entry, Listbox, END, Toplevel
from db.connection import create_connection
from db.inspector import get_tables
from ui.widgets import add_widget
from sqlalchemy import text

class DBApp:
    def __init__(self, root):
        self.logger = logging.getLogger(__name__)
        self.root = root
        self.style = ttk.Style()

        self.root.title('PostgresUI')
        self.root.geometry('600x500')

        self.entries = {}
        self.login_widgets = []

        fields = ['Host', 'Port', 'User', 'Password', 'Database']

        for i, field in enumerate(fields):
            label = Label(root, text=field)
            label.grid(row=i, column=0, padx=5, pady=5, sticky='w')
            entry = Entry(root, show='*' if field == 'Password' else '')
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[field.lower()] = entry
            self.login_widgets.extend([label, entry])


        self.connect_button = add_widget(root, ttk.Button, len(fields), text='Подключиться', command=self.connect_to_db)
        self.status_label = add_widget(root, ttk.Label, len(fields)+1, text='Статус: Не подключено')
        self.list_tables_button = add_widget(root, ttk.Button, len(fields)+2, text='Список таблиц', command=self.list_tables)
        self.tables_listbox = add_widget(root, Listbox, len(fields)+3, width=50, height=10)
        self.tables_listbox.bind('<Double-Button-1>', self.get_table_menu)
        self.login_widgets.append(self.connect_button)

        self.engine = None

    def connect_to_db(self):
        params = {key: entry.get() for key, entry in self.entries.items()}
        self.logger.info('Попытка подключения')
        try:
            self.engine = create_connection(
                user=params['user'],
                password=params['password'],
                host=params['host'],
                port=params['port'],
                database=params['database']
            )
            self.status_label.config(text='Успешное подключение')
            self.logger.info('Успешное подключение к бд')

            for widget in self.login_widgets:
                widget.grid_forget()
        except Exception as e:
            self.status_label.config(text='Ошибка подключения')
            self.logger.error(f'Ошибка при подключении: {e}')
            self.engine = None

    def list_tables(self):
        if not self.engine:
            self.status_label.config(text='Нет подключения')
            return

        try:
            tables = get_tables(self.engine)
            self.tables_listbox.delete(0, END)
            for table in tables:
                self.tables_listbox.insert(END, table)
            self.logger.info(f'Найдены таблицы: {tables}')
        except Exception as e:
            self.status_label.config(text='Ошибка при получении таблиц')
            self.logger.error(f'Ошибка при получении таблиц: {e}')

    def get_table_menu(self, event):
        selection = self.tables_listbox.curselection()
        if not selection:
            return
        table_name = self.tables_listbox.get(selection[0])

        window = Toplevel(self.root)
        window.geometry('600x400')

        tree = ttk.Treeview(window, show='headings')
        tree.pack(fill='both', expand=True)

        try:
            with self.engine.connect() as conn:
                result = conn.execute(text(f'SELECT * FROM {table_name}'))
                rows = result.fetchall()
                columns = list(result.keys())
                tree['columns'] = columns


                for col in columns:
                    tree.heading(col, text=col)
                    tree.column(col, width=100, anchor='w')
                for row in rows:
                    tree.insert('', 'end', values=list(row))
        except Exception as e:
            self.logger.error(f'Ошибка при получении строк из {table_name}: {e}')
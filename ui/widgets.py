def add_widget(root, widget_class, row, column=0, columnspan=2, pady=5, **kwargs):
    widget = widget_class(root, **kwargs)
    widget.grid(row=row, column=column, columnspan=columnspan, pady=pady)
    return widget
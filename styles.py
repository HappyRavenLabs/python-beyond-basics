from IPython.display import display, HTML

def apply_style():
    with open("./styles.html") as style_file:
        content = style_file.read()
    display(HTML(content))
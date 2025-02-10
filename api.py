import mainloop


def echo(text):
    """输出内容到控制台"""
    print(text)


def create_gui():
    """创造一个GUI对象"""
    return mainloop.GUI()

import tkinter as tk
import script_parse
from queue import Queue


class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("无标题")
        self.text = ""
        self.choice = []
        self.root.state('zoomed')  # 最大化窗口（显示标题栏）

        # 文本标签容器
        self.label = tk.Label(
            self.root,
            font=("TkDefaultFont", 24),
            wraplength=self.root.winfo_screenwidth() - 100
        )
        self.label.pack(side='top', expand=True, pady=50)

        # 按钮容器框架
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side='bottom', expand=True, pady=50)

        # 更新队列和事件循环
        self.update_queue = Queue()
        self.choice_index = None  # 用于存储用户选择的按钮索引

        self.check_updates()

    def window_title(self, title):
        """设置窗口标题"""
        self.root.title(title)

    def check_updates(self):
        """ 每100ms检查一次更新队列 """
        while not self.update_queue.empty():
            text, choices = self.update_queue.get()
            self._update_content(text, choices)
        self.root.after(100, self.check_updates)

    def _update_content(self, text, choices):
        """ 实际更新界面内容 """
        # 更新文本
        self.label.config(text=text)

        # 清空旧按钮
        for widget in self.button_frame.winfo_children():
            widget.destroy()

        # 添加新按钮，并绑定点击事件
        self.buttons = []
        for index, choice in enumerate(choices):
            btn = tk.Button(
                self.button_frame,
                text=choice,
                width=20,
                height=2,
                font=("TkDefaultFont", 24),
                command=lambda idx=index: self.on_button_click(idx)
            )
            btn.pack(pady=5)
            self.buttons.append(btn)

    def on_button_click(self, index):
        """ 处理按钮点击事件 """
        self.choice_index = index
        # 这里可以触发其他逻辑或通知主程序用户已做出选择

    def update_interface(self, text, choices):
        """ 外部调用接口 """
        self.update_queue.put((text, choices))

    def output(self, text, choices):
        """ 供外部调用的更新函数 """
        choices_list = [None for v in range(len(choices))]

        if len(choices) > 0:
            for i in range(len(choices)):
                choices_list[i] = script_parse.parse_string(choices[i])  # 处理选项文本

        self.update_interface(script_parse.parse_string(text), choices_list)  # 处理节点文本并输出节点文本与选项文本
        self.text = text
        self.choice = choices

    def input(self):
        """ 获取用户点击的按钮索引 """
        # 等待用户点击按钮
        while self.choice_index is None:
            self.root.update_idletasks()
            self.root.update()
        index = self.choice_index
        self.choice_index = None  # 重置索引以便下次使用
        return index

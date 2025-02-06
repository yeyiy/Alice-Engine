import tkinter as tk
import script_parse
from queue import Queue


class GUI:
    def __init__(self):
        """
        初始化GUI类的实例。

        此方法创建主窗口，设置窗口标题，初始化文本和选项属性，最大化窗口，
        创建文本标签和按钮容器框架，初始化更新队列和用户选择索引，
        并启动更新检查循环。
        """
        # 创建主窗口
        self.root = tk.Tk()
        # 设置窗口标题为 "无标题"
        self.root.title("无标题")
        # 初始化文本属性为空字符串
        self.text = ""
        # 初始化选项属性为空列表
        self.choice = []
        # 最大化窗口（显示标题栏）
        self.root.state('zoomed')  

        # 文本标签容器
        self.label = tk.Label(
            # 标签父容器为主窗口
            self.root,
            # 设置标签字体
            font=("TkDefaultFont", 24),
            # 设置标签文本换行宽度，为屏幕宽度减去100像素
            wraplength=self.root.winfo_screenwidth() - 100
        )
        # 将标签放置在窗口顶部，垂直方向扩展，上下边距为50像素
        self.label.pack(side='top', expand=True, pady=50)

        # 按钮容器框架
        self.button_frame = tk.Frame(self.root)
        # 将按钮框架放置在窗口底部，垂直方向扩展，上下边距为50像素
        self.button_frame.pack(side='bottom', expand=True, pady=50)

        # 更新队列和事件循环
        # 初始化更新队列，用于存储待更新的界面内容
        self.update_queue = Queue()
        # 用于存储用户选择的按钮索引，初始化为 None
        self.choice_index = None  

        # 启动更新检查循环，每100ms检查一次更新队列
        self.check_updates()

    def window_title(self, title):
        """
        设置窗口标题

        该方法用于修改当前GUI窗口的标题。

        :param title: 要设置的新窗口标题，类型为字符串。
        """
        # 调用Tkinter主窗口的title方法，将窗口标题设置为传入的title参数
        self.root.title(title)


    def check_updates(self):
        """
        每100ms检查一次更新队列

        该方法会在每次调用时检查更新队列中是否有新的更新内容。
        如果队列不为空，则从队列中取出更新内容并调用 _update_content 方法更新界面。
        之后，使用 after 方法在100ms后再次调用自身，实现定时检查。
        """
        # 检查更新队列是否不为空
        while not self.update_queue.empty():
            # 从更新队列中获取待更新的文本和选项列表
            text, choices = self.update_queue.get()
            # 调用 _update_content 方法更新界面内容
            self._update_content(text, choices)
        # 使用 after 方法在100ms后再次调用 check_updates 方法，实现定时检查
        self.root.after(100, self.check_updates)


    def _update_content(self, text, choices):
        """ 实际更新界面内容 """
        # 更新文本标签的内容为传入的文本
        self.label.config(text=text)

        # 清空按钮容器框架内的所有旧按钮
        for widget in self.button_frame.winfo_children():
            # 销毁每个子组件（即旧按钮）
            widget.destroy()

        # 初始化按钮列表，用于存储新创建的按钮
        self.buttons = []
        # 遍历传入的选项列表，同时获取每个选项的索引
        for index, choice in enumerate(choices):
            # 创建一个新的按钮组件
            btn = tk.Button(
                # 按钮的父容器为按钮容器框架
                self.button_frame,
                # 按钮显示的文本为当前选项
                text=choice,
                # 按钮的宽度为20
                width=20,
                # 按钮的高度为2
                height=2,
                # 按钮的字体设置
                font=("TkDefaultFont", 24),
                # 绑定按钮点击事件，点击时调用 on_button_click 方法并传入当前选项的索引
                command=lambda idx=index: self.on_button_click(idx)
            )
            # 将按钮添加到按钮容器框架中，并设置垂直方向的间距为5像素
            btn.pack(pady=5)
            # 将新创建的按钮添加到按钮列表中
            self.buttons.append(btn)

    def on_button_click(self, index):
        """
        处理按钮点击事件

        该方法在用户点击按钮时被调用，用于记录用户选择的按钮索引，并可触发其他逻辑或通知主程序用户已做出选择。

        :param index: 用户点击的按钮的索引，用于标识用户的选择。
        """
        # 将用户点击的按钮索引赋值给 choice_index 属性，以便后续获取用户选择
        self.choice_index = index
        # 这里可以触发其他逻辑或通知主程序用户已做出选择，例如更新界面状态、保存用户选择等
        # 示例：可以在这里添加代码来更新界面上的某些元素，或者调用其他方法来处理用户选择
        # self.update_some_ui_element()
        # self.notify_main_program()

    def update_interface(self, text, choices):
        """
        外部调用接口

        该方法作为一个外部调用的接口，用于将需要更新的文本和选项列表添加到更新队列中。
        后续 `check_updates` 方法会从队列中取出这些内容并更新界面。

        :param text: 要更新到界面上的文本内容。
        :param choices: 要更新到界面上的选项列表。
        """
        # 将传入的文本和选项列表作为一个元组添加到更新队列中
        self.update_queue.put((text, choices))

    def output(self, text, choices):
        """ 供外部调用的更新函数 """
        # 初始化一个长度与 choices 列表相同的列表，初始值都为 None
        choices_list = [None for v in range(len(choices))]

        # 检查 choices 列表是否包含元素
        if len(choices) > 0:
            # 遍历 choices 列表中的每个选项
            for i in range(len(choices)):
                # 调用 script_parse 模块中的 parse_string 函数处理选项文本
                # 并将处理后的结果存储在 choices_list 列表的对应位置
                choices_list[i] = script_parse.parse_string(choices[i])  

        # 调用 update_interface 方法，将处理后的节点文本和选项文本更新到界面上
        self.update_interface(script_parse.parse_string(text), choices_list)  
        # 将传入的节点文本赋值给实例属性 self.text
        self.text = text
        # 将传入的选项列表赋值给实例属性 self.choice
        self.choice = choices

    def input(self):
        """
        获取用户点击的按钮索引

        该方法会持续等待，直到用户点击了某个按钮，然后返回被点击按钮的索引。
        在用户点击按钮后，会将索引重置，以便下次使用。

        :return: 用户点击的按钮的索引
        """
        # 持续等待，直到用户点击了某个按钮，即 self.choice_index 不再为 None
        while self.choice_index is None:
            # 更新界面的空闲任务，确保界面能够响应用户操作
            self.root.update_idletasks()
            # 更新界面，处理所有待处理的事件
            self.root.update()
        # 将用户点击的按钮索引赋值给 index 变量
        index = self.choice_index
        # 重置索引，将 self.choice_index 设为 None，以便下次使用
        self.choice_index = None
        # 返回用户点击的按钮的索引
        return index


        self.choice_index = None  # 重置索引以便下次使用
        return index

import mainloop
import script_parse

if __name__ == "__main__":
    # 定义脚本文件的路径
    file = "script.as"
    # 初始化全局应用实例，创建一个 GUI 对象
    game = mainloop.GUI()
    # 设置窗口标题，从脚本文件中读取标题信息
    game.window_title(script_parse.read_script(file)[0])
    # 读取脚本文件，获取脚本中的节点信息
    points = script_parse.read_script(file)[1]

    try:
        while True:
            # 不断输出与更新节点，将当前节点的文本和选项显示在界面上
            game.output(points.text, [i[0] for i in points.choice])
            # 根据用户的输入选择下一个节点
            points = script_parse.choose(points, game.input())

        # noinspection PyUnreachableCode
        # 进入 Tkinter 的主事件循环，此代码实际上无法到达
        game.root.mainloop()

    except AttributeError as e:
        # 捕获属性错误异常，当游戏结束或遇到错误时，显示错误信息
        game.output(f"由于游戏结束或遇到了错误，游戏程序已经停止，详细的输出如下：\n{e}", ["确定"])

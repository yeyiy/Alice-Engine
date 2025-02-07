import mainloop
import script_parse

if __name__ == "__main__":
    file = "script.as"  # 脚本文件名

    # 初始化全局应用实例
    game = mainloop.GUI()  # 实例化GUI对象
    game.window_title(script_parse.read_script(file)[0])  # 设置窗口标题
    points = script_parse.read_script(file)[1]  # 读取脚本文件

    try:
        while True:
            game.output(points.text, [i[0] for i in points.choice])  # 输出节点文本，读取并输出选项文本
            points = script_parse.choose(points, game.input())  # 选择选项并更新节点

        # noinspection PyUnreachableCode
        game.root.mainloop()

    except AttributeError as e:
        game.output(f"由于游戏结束或遇到了错误，游戏程序已经停止，详细的输出如下：\n{e}", ["确定"])

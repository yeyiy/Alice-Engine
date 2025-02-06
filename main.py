import mainloop
import script_parse

if __name__ == "__main__":
    file = "script.as"

    # 初始化全局应用实例
    game = mainloop.GUI()
    game.window_title(script_parse.read_script(file)[0])  # 设置窗口标题
    points = script_parse.read_script(file)[1]  # 读取脚本文件

    try:
        while True:
            # 不断输出与更新节点
            game.output(points.text, [i[0] for i in points.choice])
            points = script_parse.choose(points, game.input())

        # noinspection PyUnreachableCode
        game.root.mainloop()

    except AttributeError as e:
        game.output(f"由于游戏结束或遇到了错误，游戏程序已经停止，详细的输出如下：\n{e}", ["确定"])

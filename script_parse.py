class Point:
    def __init__(self, text="", choice=None):
        if choice is None:
            choice = []

        self.text = text
        self.choice = choice

    def __repr__(self):
        name = 'unnamed'

        # 读取Point节点的名字
        for obj_name, value in globals().items():
            if value is self:
                name = obj_name

        return f"Point object '{name}', text='{self.text}', choice={self.choice}"


def choose(_point, _input):
    """对选项对应的节点进行链接"""
    return _point.choice[_input][1]


def parse_string(string: str):
    """输出字符串进行处理"""
    # 处理转义字符
    string = (string.replace("$n", "\n").replace("$s", " ")
                    .replace("$p", "#")).replace("$lb", "{").replace("$rb", "}")

    # 删除结尾冗余换行符和空格
    while string[-1] in {"\n", " "}:
        string = string[0:-1]

    return string


def read_script(file):
    with open(file, encoding="utf-8") as f:
        string = f.read()

    return string.split("&")[0], parse_script(string.split("&")[1])  # 解析脚本文件中定义的游戏名和游戏脚本（用“&”分隔）


def parse_script(string: str):
    """将脚本文件解析为Point对象"""

    # 删除冗余空格
    after_newline = False

    for v in range(string.count(" ")):
        for i in range(len(string)):
            try:
                if string[i] == "\n":
                    after_newline = True    # 位于换行符之后

                elif string[i] != " ":
                    after_newline = False   # 遇到非空格字符，停止处理冗余空格

                if after_newline and string[i] == " ":
                    string = string[:i] + string[i + 1:]  # 当处于换行符后且遇到空格时，删除此空格
                    break

            except IndexError:
                pass

    def _split(s: str, x: str):
        """分割字符串"""
        num = 0
        result = []
        start = 0

        # 判断是否位于嵌套节点内
        for j in range(len(s)):
            try:
                if s[j] == "{" and s[j - 1]:
                    num += 1  # 进入大括号嵌套，嵌套层数加一

                elif s[j] == "}" and s[j - 1]:
                    num -= 1  # 结束大括号嵌套，嵌套层数减一

            except IndexError:
                pass

            if num == 0 and s[j:j + len(x)] == x:
                result.append(s[start:j])  # 当不在嵌套的节点内且遇到要分割的字符串时，将分割的字符串加入列表
                start = j + len(x)

        result.append(s[start:])  # 将最后一个分割的字符串加入列表，以免被忽略

        return [d for d in result if d != ""]  # 删除结果中的空字符

    def parse_choice(choice):
        """解析选项"""
        choice = choice[1:]  # 删除选项脚本开头的“#”
        p = None
        q = None

        for c in range(len(choice)):
            if choice[c] == "{" and p is None:
                p = c  # 选项对应的节点（被大括号括起）的开始位置

            elif choice[c] == "}":
                q = c  # 选项对应的节点（被大括号括起）的结束位置

        if "{" in choice:
            return choice.split("{")[0], parse_point(choice[p:q + 1])  # 分别返回选项文本和选项文本对应的节点

        else:
            return choice, None  # 只返回选项文本

    def parse_point(point):
        """解析节点"""
        begin = None
        end = 0

        for k in range(len(point)):
            if point[k] == "{" and begin is None:
                begin = k  # 节点（被大括号括起）的开始位置

            elif point[k] == "}":
                end = k  # 节点（被大括号括起）的结束位置

        point = point[begin + 1:end]    # 截去大括号之外的冗余字符串
        string_list = _split(point, "#")    # 通过“#”分割节点文本和选项

        return Point(string_list[0],
                     [parse_choice("#" + string_list[a]) for a in range(len(string_list)) if a != 0])   # 返回Point节点，参数包括节点文本和选项列表

    return parse_point(string)  # 返回对脚本的解析

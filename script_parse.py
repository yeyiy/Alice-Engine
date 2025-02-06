class Point:
    def __init__(self, text="", choice=None):
        if choice is None:
            choice = []

        self.text = text
        self.choice = choice

    def __repr__(self):
        name = 'unnamed'
        for obj_name, value in globals().items():
            if value is self:
                name = obj_name

        return f"Point object '{name}', text='{self.text}', choice={self.choice}"


def choose(_point, _input):
    """对选项对应的节点进行链接"""
    return _point.choice[_input][1]


def parse_string(string: str):
    """输出字符串进行处理"""
    while string[-1] == "\n":
        string = string[0:-1]  # 删除结尾冗余换行符

    return string.replace("$n", "\n").replace("$s", " ")  # 处理转义字符


def read_script(file):
    with open(file, encoding="utf-8") as f:
        string = f.read()

    return string.split("&")[0], parse_script(string.split("&")[1])


def parse_script(string: str):
    """将脚本文件解析为Point对象"""

    # 删除冗余空格
    after_newline = False

    for v in range(string.count(" ")):
        for i in range(len(string)):
            try:
                if (string[i] == "\n") and string[i - 1] != "@":
                    after_newline = True

                elif string[i] != " ":
                    after_newline = False

                if after_newline and string[i] == " ":
                    string = string[:i] + string[i + 1:]
                    break

            except IndexError:
                pass

    def _split(s: str, x: str):
        """分割字符串"""
        num = 0
        result = []
        start = 0
        j = 0

        # 判断是否位于嵌套节点内
        for j in range(len(s)):
            try:
                if s[j] == "{" and s[j - 1] != "@":
                    num += 1

                elif s[j] == "}" and s[j - 1] != "@":
                    num -= 1

            except IndexError:
                pass

            if num == 0 and s[j:j + len(x)] == x:
                result.append(s[start:j])
                start = j + len(x)

        result.append(s[start:])

        return [d for d in result if d != ""]

    def parse_choice(choice):
        """解析选项"""
        choice = choice[1:]
        m = 0
        p = None
        q = None

        for c in range(len(choice)):
            try:
                if choice[c] == "{" and choice[c - 1] != "@":
                    m += 1

                elif choice[c] == "}" and choice[c - 1] != "@":
                    m -= 1

            except IndexError:
                pass

            if choice[c] == "{" and p is None:
                p = c

            elif choice[c] == "}":
                q = c

        if "{" in choice:
            return choice.split("{")[0], parse_point(choice[p:q + 1])

        else:
            return choice, None

    def parse_point(point):
        """解析节点"""
        n = 0
        begin = 0
        end = 0

        for k in range(len(point)):
            try:
                if point[k] == "{" and point[k - 1] != "@":
                    n += 1

                elif point[k] == "}" and point[k - 1] != "@":
                    n -= 1

            except IndexError:
                pass

            if point[k] == "{" and begin == 0:
                begin = k

            elif point[k] == "}":
                end = k

        point = point[begin + 1:end]
        string_list = _split(point, "#")

        return Point(string_list[0],
                     [parse_choice("#" + string_list[a]) for a in range(len(string_list)) if a != 0])

    return parse_point(string)

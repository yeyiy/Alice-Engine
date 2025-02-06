import pathlib#文件处理的内置库

class Point:
    def __init__(self, text="", choice=None):
        """
        初始化Point类的实例。

        :param text: 节点的文本内容，默认为空字符串。
        :param choice: 节点的选项列表，默认为None。如果为None，则初始化为空列表。
        """
        # 如果choice参数为None，则将其初始化为空列表
        if choice is None:
            choice = []

        # 将传入的text参数赋值给实例的text属性
        self.text = text
        # 将处理后的choice参数赋值给实例的choice属性
        self.choice = choice

    def __repr__(self):
        """
        返回Point对象的字符串表示形式，方便调试和打印对象信息。

        此方法会尝试在全局命名空间中查找当前对象的名称，如果找到则使用该名称，
        否则使用默认名称 'unnamed'。最终返回一个包含对象名称、文本内容和选项列表的字符串。

        :return: 表示Point对象的字符串。
        """
        # 初始化对象名称为 'unnamed'
        name = 'unnamed'
        # 遍历全局命名空间中的所有对象
        for obj_name, value in globals().items():
            # 如果找到与当前对象相同的对象
            if value is self:
                # 将该对象的名称赋值给 name
                name = obj_name

        # 返回包含对象名称、文本内容和选项列表的字符串
        return f"Point object '{name}', text='{self.text}', choice={self.choice}"


def choose(_point, _input):
    """
    对选项对应的节点进行链接

    该函数接收一个Point对象和一个输入索引，根据输入索引从Point对象的选项列表中
    选取对应的选项，并返回该选项关联的节点。

    :param _point: Point类的实例，代表当前节点，包含文本内容和选项列表。
    :param _input: 一个整数，代表用户选择的选项索引，用于从_point的选项列表中选取对应选项。
    :return: 返回_point的选项列表中，索引为_input的选项所关联的节点。
    """
    # 根据输入的索引从_point的选项列表中选取对应选项，并返回该选项关联的节点
    return _point.choice[_input][1]


def parse_string(string: str):
    """
    对输入的字符串进行处理，包括删除结尾冗余换行符和处理转义字符。

    :param string: 输入的待处理字符串。
    :return: 处理后的字符串。
    """
    # 循环检查字符串末尾是否为换行符
    while string[-1] == "\n":
        # 如果是，则删除末尾的换行符
        string = string[0:-1]  
    # 处理转义字符，将 $n 替换为换行符，$s 替换为空格
    return string.replace("$n", "\n").replace("$s", " ")  

def read_script(file):
    """
    读取脚本文件并解析其内容。

    该函数接收一个文件路径作为输入，读取文件内容，然后将内容按 '&' 分割成两部分。
    第一部分直接返回，第二部分传递给 parse_script 函数进行解析。

    :param file: 要读取的脚本文件的路径。
    :return: 一个元组，包含分割后的第一部分内容和解析后的 Point 对象。
    """
    # 以 UTF-8 编码打开指定文件
    with open(file, encoding="utf-8") as f:
        # 读取文件的全部内容
        string = f.read()

    # 将读取的内容按 '&' 分割成两部分
    # 返回分割后的第一部分内容和对第二部分内容调用 parse_script 函数解析后的结果
    return string.split("&")[0], parse_script(string.split("&")[1])

def parse_script(string: str):
    """
    将脚本文件解析为Point对象

    :param string: 待解析的脚本字符串
    :return: 解析后的Point对象
    """

    # 删除冗余空格
    after_newline = False

    # 循环删除字符串中的冗余空格
    for v in range(string.count(" ")):
        for i in range(len(string)):
            try:
                # 检查当前字符是否为换行符且前一个字符不是 @
                if (string[i] == "\n") and string[i - 1] != "@":
                    after_newline = True
                # 若当前字符不是空格，重置状态
                elif string[i] != " ":
                    after_newline = False
                # 如果处于换行后且当前字符是空格，则删除该空格
                if after_newline and string[i] == " ":
                    string = string[:i] + string[i + 1:]
                    break
            except IndexError:
                pass

    def _split(s: str, x: str):
        """
        分割字符串，考虑嵌套节点的情况

        :param s: 待分割的字符串
        :param x: 分割符
        :return: 分割后的字符串列表
        """
        num = 0  # 用于记录嵌套层级
        result = []
        start = 0
        j = 0

        # 判断是否位于嵌套节点内
        for j in range(len(s)):
            try:
                # 遇到 { 且前一个字符不是 @，嵌套层级加 1
                if s[j] == "{" and s[j - 1] != "@":
                    num += 1
                # 遇到 } 且前一个字符不是 @，嵌套层级减 1
                elif s[j] == "}" and s[j - 1] != "@":
                    num -= 1
            except IndexError:
                pass

            # 当嵌套层级为 0 且遇到分割符时，进行分割
            if num == 0 and s[j:j + len(x)] == x:
                result.append(s[start:j])
                start = j + len(x)

        result.append(s[start:])

        # 过滤掉空字符串
        return [d for d in result if d != ""]

    def parse_choice(choice):
        """
        解析选项

        :param choice: 待解析的选项字符串
        :return: 解析后的选项文本和对应的Point对象
        """
        choice = choice[1:]  # 去掉开头的 #
        m = 0  # 用于记录嵌套层级
        p = None  # 记录 { 的位置
        q = None  # 记录 } 的位置

        for c in range(len(choice)):
            try:
                # 遇到 { 且前一个字符不是 @，嵌套层级加 1
                if choice[c] == "{" and choice[c - 1] != "@":
                    m += 1
                # 遇到 } 且前一个字符不是 @，嵌套层级减 1
                elif choice[c] == "}" and choice[c - 1] != "@":
                    m -= 1
            except IndexError:
                pass

            # 记录第一个 { 的位置
            if choice[c] == "{" and p is None:
                p = c
            # 记录最后一个 } 的位置
            elif choice[c] == "}":
                q = c

        # 如果存在 {，则递归解析嵌套节点
        if "{" in choice:
            return choice.split("{")[0], parse_point(choice[p:q + 1])
        else:
            return choice, None

    def parse_point(point):
        """
        解析节点

        :param point: 待解析的节点字符串
        :return: 解析后的Point对象
        """
        n = 0  # 用于记录嵌套层级
        begin = 0  # 记录 { 的位置
        end = 0  # 记录 } 的位置

        for k in range(len(point)):
            try:
                # 遇到 { 且前一个字符不是 @，嵌套层级加 1
                if point[k] == "{" and point[k - 1] != "@":
                    n += 1
                # 遇到 } 且前一个字符不是 @，嵌套层级减 1
                elif point[k] == "}" and point[k - 1] != "@":
                    n -= 1
            except IndexError:
                pass

            # 记录第一个 { 的位置
            if point[k] == "{" and begin == 0:
                begin = k
            # 记录最后一个 } 的位置
            elif point[k] == "}":
                end = k

        # 提取节点内部的字符串
        point = point[begin + 1:end]
        # 按 # 分割字符串
        string_list = _split(point, "#")

        # 创建并返回Point对象
        return Point(string_list[0],
                     [parse_choice("#" + string_list[a]) for a in range(len(string_list)) if a != 0])

    # 调用 parse_point 函数解析整个字符串并返回结果
    return parse_point(string)
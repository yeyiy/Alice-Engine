import sys
import ast
import api
from types import ModuleType, FunctionType
from typing import Dict, Any


def _is_expression(code_str):
    """判断一段字符串能否被解析为表达式"""
    tree = ast.parse(code_str)
    return bool(tree.body) and isinstance(tree.body[-1], ast.Expr)


class Runner:
    def __init__(self):
        self.global_context = self._safe_globals()  # 储存全局上下文
        self.local_context = {}  # 储存局部上下文

    @staticmethod
    def _safe_globals() -> Dict[str, Any]:
        """创建一个安全的全局环境"""
        _globals = {
            '__builtins__': None,  # 禁用所有内置函数
        }
        allowed_builtins = [
            'abs', 'all', 'any', 'ascii', 'bin', 'bool', 'bytearray', 'bytes',
            'callable', 'chr', 'complex', 'dict', 'divmod', 'enumerate', 'filter',
            'float', 'format', 'frozenset', 'getattr', 'hasattr', 'hash', 'hex',
            'id', 'int', 'isinstance', 'issubclass', 'iter', 'len', 'list',
            'map', 'max', 'min', 'next', 'object', 'oct', 'ord', 'pow', 'range',
            'repr', 'reversed', 'round', 'set', 'slice', 'sorted', 'str', 'sum',
            'tuple', 'type', 'zip'
        ]  # 允许被调用的对象

        for name in allowed_builtins:
            if name in __builtins__:
                _globals[name] = __builtins__[name]  # 生成安全的执行环境

        _globals['api'] = api  # 添加api库为可调用库

        return _globals

    def run(self, code_str):
        """执行代码"""
        if _is_expression(code_str):
            result = eval(code_str, self.global_context, self.local_context)  # 判断代码为表达式，返回表达式求值结果

        else:
            result = None

        return '' if result is None else str(result)  # 如果无返回或返回结果None则返回空字符串


# 创建SafeContextRunner的单例实例以便所有run调用共享同一个上下文
runner = Runner()


def run_code(code_str):
    """暴露给外部使用的run函数"""
    return runner.run(code_str)

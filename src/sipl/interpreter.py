from .ast import *
from typing import Dict, Any

class Interpreter:
    def __init__(self):
        self.env: Dict[str, int] = {}
        self.step_limit = 10000
        self.steps = 0

    def eval_expr(self, node: ASTNode) -> int:
        if isinstance(node, Number):
            return node.value
        elif isinstance(node, Var):
            if node.name not in self.env:
                raise ValueError(f"Змінна {node.name} не визначена або не ініціалізована")
            return self.env[node.name]
        elif isinstance(node, BinOp):
            left = self.eval_expr(node.left)
            right = self.eval_expr(node.right)
            if node.op == '+': return left + right
            if node.op == '-': return left - right
            if node.op == '*': return left * right
            if node.op == '/': 
                if right == 0: raise ValueError("Ділення на нуль")
                return left // right
            if node.op == '>': return 1 if left > right else 0
            if node.op == '<': return 1 if left < right else 0
            if node.op == '==': return 1 if left == right else 0
            
        raise ValueError(f"Невідомий вираз: {type(node)}")

    def execute(self, node: ASTNode):
        self.steps += 1
        if self.steps > self.step_limit:
            raise RuntimeError("Перевищено ліміт кроків (можливий нескінченний цикл)!")

        if isinstance(node, Skip):
            pass
        elif isinstance(node, Assign):
            self.env[node.var_name] = self.eval_expr(node.expr)
        elif isinstance(node, Block):
            for stmt in node.statements:
                self.execute(stmt)
        elif isinstance(node, If):
            cond = self.eval_expr(node.condition)
            if cond != 0:
                self.execute(node.true_branch)
            else:
                self.execute(node.false_branch)
        elif isinstance(node, While):
            while self.eval_expr(node.condition) != 0:
                self.execute(node.body)
        else:
            raise ValueError(f"Невідомий оператор: {type(node)}")

def run_program(ast_root: ASTNode) -> Dict[str, int]:
    """Запускає AST-дерево і повертає кінцевий стан змінних."""
    interpreter = Interpreter()
    interpreter.execute(ast_root)
    return interpreter.env
from dataclasses import dataclass
from typing import List, Optional, Any

@dataclass
class SourceSpan:
    line: int
    column: int

class ASTNode:
    span: Optional[SourceSpan] = None

    def set_span(self, line: int, column: int):
        self.span = SourceSpan(line, column)
        return self

@dataclass
class Number(ASTNode):
    value: int

@dataclass
class Var(ASTNode):
    name: str

@dataclass
class BinOp(ASTNode):
    left: ASTNode
    op: str
    right: ASTNode

@dataclass
class Skip(ASTNode):
    pass

@dataclass
class Assign(ASTNode):
    var_name: str
    expr: ASTNode

@dataclass
class Block(ASTNode):
    statements: List[ASTNode]

@dataclass
class If(ASTNode):
    condition: ASTNode
    true_branch: ASTNode
    false_branch: ASTNode

@dataclass
class While(ASTNode):
    condition: ASTNode
    body: ASTNode
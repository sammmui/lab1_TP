import os
import importlib
from .ast import *

try:
    _lark = importlib.import_module("lark")
except ModuleNotFoundError as e:
    if e.name == "lark":
        raise ModuleNotFoundError(
            "The 'lark' package is required. Install it with: pip install lark"
        ) from e
    raise

GRAMMAR_PATH = os.path.join(os.path.dirname(__file__), '..', '..', 'grammar', 'sipl.lark')
with open(GRAMMAR_PATH, 'r', encoding='utf-8') as f:
    sipl_grammar = f.read()

lark_parser = _lark.Lark(sipl_grammar, parser='lalr', propagate_positions=True)

class SIPLTransformer(_lark.Transformer):
    def number(self, args):
        return Number(int(args[0].value)).set_span(args[0].line, args[0].column)
        
    def var(self, args):
        return Var(str(args[0].value)).set_span(args[0].line, args[0].column)
        
    def add(self, args): return BinOp(args[0], '+', args[1]).set_span(args[0].span.line, args[0].span.column)
    def sub(self, args): return BinOp(args[0], '-', args[1]).set_span(args[0].span.line, args[0].span.column)
    def mul(self, args): return BinOp(args[0], '*', args[1]).set_span(args[0].span.line, args[0].span.column)
    def div(self, args): return BinOp(args[0], '/', args[1]).set_span(args[0].span.line, args[0].span.column)
    def gt(self, args):  return BinOp(args[0], '>', args[1]).set_span(args[0].span.line, args[0].span.column)
    def lt(self, args):  return BinOp(args[0], '<', args[1]).set_span(args[0].span.line, args[0].span.column)
    def eq(self, args):  return BinOp(args[0], '==', args[1]).set_span(args[0].span.line, args[0].span.column)
    
    def skip_stmt(self, args):
        return Skip()
        
    def assign(self, args):
        var_token = args[0]
        return Assign(str(var_token.value), args[1]).set_span(var_token.line, var_token.column)
        
    def block(self, args):
       
        return Block(args[0])
        
    def stmt_list(self, args):
        return args
        
    def if_stmt(self, args):
        return If(args[0], args[1], args[2])
        
    def while_stmt(self, args):
        return While(args[0], args[1])

def parse_code(code: str) -> ASTNode:
    try:
        tree = lark_parser.parse(code)
        return SIPLTransformer().transform(tree)
    except _lark.exceptions.UnexpectedInput as e:
        error_msg = f"Синтаксична помилка: рядок {e.line}, колонка {e.column}"
        print(error_msg)
        raise ValueError(error_msg) from e
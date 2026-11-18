import sys
import os
import json

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from sipl.parser import lark_parser, SIPLTransformer
from sipl.ast import ASTNode
from lark.tree import Tree
from lark.lexer import Token

def parse_tree_to_dict(node):
    """Генерує JSON для Parse Tree (з прив'язкою до рядків/колонок)."""
    if isinstance(node, Tree):
        return {"node": str(node.data), "children": [parse_tree_to_dict(c) for c in node.children]}
    elif isinstance(node, Token):
        return {"token": node.type, "value": node.value, "line": node.line, "col": node.column}
    return str(node)

def ast_to_dict(node):
    """Генерує JSON для Abstract Syntax Tree."""
    if isinstance(node, ASTNode):
        d = {"AST_Node": type(node).__name__}
        if node.span:
            d["source_position"] = f"Line {node.span.line}, Col {node.span.column}"
        for k, v in vars(node).items():
            if k == 'span': continue
            if isinstance(v, list): d[k] = [ast_to_dict(i) for i in v]
            elif isinstance(v, ASTNode): d[k] = ast_to_dict(v)
            else: d[k] = v
        return d
    return node

def generate_dot(node, file, parent_id=None, counter=None):
    """Генерує DOT-формат для Parse Tree."""
    if counter is None: counter = [0]
    curr_id = counter[0]
    counter[0] += 1
    
    if isinstance(node, Tree):
        label = str(node.data)
        file.write(f'  node{curr_id} [label="{label}", shape=ellipse];\n')
        if parent_id is not None: file.write(f'  node{parent_id} -> node{curr_id};\n')
        for child in node.children: generate_dot(child, file, curr_id, counter)
    elif isinstance(node, Token):
        label = f"{node.type}\\n'{node.value}'\\n(L{node.line}:C{node.column})"
        file.write(f'  node{curr_id} [label="{label}", shape=box, color=lightblue, style=filled];\n')
        if parent_id is not None: file.write(f'  node{parent_id} -> node{curr_id};\n')

def main():
    if len(sys.argv) < 2:
        print("Вкажіть файл: python visualize.py tests/positive/test04.sipl")
        return
        
    filepath = sys.argv[1]
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()

    tree = lark_parser.parse(code)
    
    # VIS-01
    with open("parse_tree.txt", "w", encoding="utf-8") as f:
        f.write(tree.pretty())
        
    pt_dict = parse_tree_to_dict(tree)
    with open("parse_tree.json", "w", encoding="utf-8") as f:
        json.dump(pt_dict, f, indent=2, ensure_ascii=False)
        
    with open("parse_tree.dot", "w", encoding="utf-8") as f:
        f.write("digraph ParseTree {\n")
        generate_dot(tree, f)
        f.write("}\n")
        
    ast = SIPLTransformer().transform(tree)
    ast_dict = ast_to_dict(ast)
    
    # VIS-02
    html_content = f'''<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>Parse Tree vs AST</title></head>
<body style="display:flex; font-family:monospace; margin:0; height:100vh;">
    <div style="flex:1; padding:20px; overflow:auto; border-right:2px solid #ccc;">
        <h2>Parse Tree (Конкретний синтаксис)</h2>
        <pre>{json.dumps(pt_dict, indent=2, ensure_ascii=False)}</pre>
    </div>
    <div style="flex:1; padding:20px; overflow:auto; background:#f4f9f4;">
        <h2>AST (Абстрактний синтаксис)</h2>
        <pre>{json.dumps(ast_dict, indent=2, ensure_ascii=False)}</pre>
    </div>
</body></html>'''

    with open("comparison.html", "w", encoding="utf-8") as f:
        f.write(html_content)
        
    print("Готово! Згенеровано 4 файли згідно з критеріями VIS-01 та VIS-02.")

if __name__ == "__main__":
    main()
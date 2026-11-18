import argparse
import json
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from sipl.parser import parse_code
from sipl.interpreter import Interpreter

def main():
    parser = argparse.ArgumentParser(description="SIPL Language CLI")
    parser.add_argument("command", choices=["parse", "check", "run", "trace"], help="Команда для виконання")
    parser.add_argument("file", help="Шлях до файлу з кодом SIPL")
    parser.add_argument("--json", action="store_true", help="Вивести результат у форматі JSON")

    args = parser.parse_args()

    if not os.path.exists(args.file):
        print(f"Помилка: файл {args.file} не знайдено.")
        sys.exit(1)

    with open(args.file, 'r', encoding='utf-8') as f:
        code = f.read()

    try:
        ast = parse_code(code)
        
        if args.command in ("parse", "check"):
            if args.json:
                print(json.dumps({"status": "success", "message": "Syntax is correct"}))
            else:
                print("Синтаксис коректний. AST побудовано успішно.")
            sys.exit(0)

        elif args.command in ("run", "trace"):
            interpreter = Interpreter()
            interpreter.execute(ast)
            
            if args.json:
                print(json.dumps({"status": "success", "env": interpreter.env}))
            else:
                print("Виконання успішне!")
                print("Кінцевий стан змінних:", interpreter.env)
            sys.exit(0)

    except Exception as e:
        if args.json:
            print(json.dumps({"status": "error", "message": str(e)}))
        else:
            print(f"Помилка: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
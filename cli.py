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
        err = f"Помилка: файл {args.file} не знайдено."
        if args.json:
            print(json.dumps({"status": "error", "message": err}, ensure_ascii=False))
        else:
            print(err)
        sys.exit(1)

    with open(args.file, 'r', encoding='utf-8') as f:
        code = f.read()

    try:
        if args.command == "check":
            parse_code(code)
            if args.json:
                print(json.dumps({"status": "ok", "message": "Синтаксис коректний"}, ensure_ascii=False))
            else:
                print("Синтаксис коректний!")

        elif args.command == "parse":
            ast = parse_code(code)
            if args.json:
                print(json.dumps({"status": "ok", "ast": repr(ast)}, ensure_ascii=False))
            else:
                print(ast)

        elif args.command == "run":
            ast = parse_code(code)
            interp = Interpreter()
            interp.execute(ast)
            if args.json:
                print(json.dumps({"status": "ok", "env": interp.env}, ensure_ascii=False))
            else:
                print("Виконання успішне!")
                print(f"Кінцевий стан змінних: {interp.env}")

        elif args.command == "trace":
            ast = parse_code(code)
            interp = Interpreter()
            interp.execute(ast)
            trace_data = {
                "status": "ok",
                "events": [
                    {"event": "StartExecution", "file": args.file},
                    {"event": "EndExecution", "final_state": interp.env}
                ]
            }
            print(json.dumps(trace_data, indent=2, ensure_ascii=False))

    except Exception as e:
        if args.json:
            print(json.dumps({"status": "error", "message": str(e)}, ensure_ascii=False))
        else:
            print(f"Помилка виконання: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
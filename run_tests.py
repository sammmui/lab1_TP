import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))
from sipl.parser import parse_code
from sipl.interpreter import Interpreter

def run_tests():
    passed = 0
    failed = 0

    print("ПОЗИТИВНІ ТЕСТИ")
    pos_dir = "tests/positive"
    for filename in sorted(os.listdir(pos_dir)):
        filepath = os.path.join(pos_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        try:
            ast = parse_code(code)
            interpreter = Interpreter()
            interpreter.execute(ast)
            print(f"[УСПІХ] {filename}")
            passed += 1
        except Exception as e:
            print(f"[ПОМИЛКА] {filename} впав: {e}")
            failed += 1

    print("\nНЕГАТИВНІ ТЕСТИ")
    neg_dir = "tests/negative"
    for filename in sorted(os.listdir(neg_dir)):
        filepath = os.path.join(neg_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            code = f.read()
        try:
            parse_code(code)
            print(f"[ПОМИЛКА] {filename} не видав помилку, хоча мав!")
            failed += 1
        except Exception:
            print(f"[УСПІХ] {filename} успішно відхилено парсером")
            passed += 1

    print(f"\nПідсумок: {passed} тестів пройдено, {failed} провалено.")

if __name__ == "__main__":
    run_tests()
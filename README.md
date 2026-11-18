# SIPL Language Toolkit (`lab1_TP`)

![CI Tests](https://github.com/sammmui/lab1_TP/actions/workflows/ci.yml/badge.svg)

**Обрані завдання:** `CORE-01`, `CORE-02`, `CORE-03`, `CORE-05`, `CORE-06`, `VIS-01`, `VIS-02`, `REL-01`, `REL-02`, `REL-03`  
**Очікувана кількість балів:** **10.0**

Курсовий проєкт з дисципліни **«Теорія програмування»**
---

## Заявлений набір завдань та розподіл балів

| ID | Назва модуля / завдання | Бали | Реалізація у репозиторії |
| :--- | :--- | :---: | :--- |
| **CORE-01** | Формальна специфікація SIPL | 0.5 | `grammar/sipl.lark`, 10 позитивних та 10 негативних тестів |
| **CORE-02** | Парсер та типізоване AST з `SourceSpan` | 1.5 | `src/sipl/ast.py`, `src/sipl/parser.py`[cite: 10] |
| **CORE-03** | Інтерпретатор SIPL | 2.0 | `src/sipl/interpreter.py` (змінні, `if`, `while`, `begin/end`, `skip`, ліміт кроків)[cite: 10] |
| **CORE-05** | CLI з підтримкою JSON-режиму | 1.0 | `cli.py` (`parse`, `check`, `run`, `trace`, `--json`)[cite: 10] |
| **CORE-06** | Conformance suite (набір тестів) | 1.0 | `run_tests.py`, директорія `tests/` |
| **VIS-01** | Візуалізація Parse Tree | 1.5 | `visualize.py` (генерація Text, JSON та DOT із прив'язкою до коду) |
| **VIS-02** | Візуалізація AST та порівняння | 1.0 | `visualize.py` → інтерактивний `comparison.html`[cite: 12] |
| **REL-01** | CI (автоматичні тести в GitHub Actions) | 0.5 | `.github/workflows/ci.yml` |
| **REL-02** | GitHub Release + SemVer + Changelog | 0.5 | Тег `v1.0.0`, реліз на GitHub та `CHANGELOG.md`[cite: 14] |
| **REL-03** | Пакування Python-пакета | 0.5 | `pyproject.toml` (встановлення через `pip`)[cite: 14] |
| **Разом** | | **10.0** | |

---

## Архітектура проєкту

```text
lab1_TP/
├── .github/workflows/
│   └── ci.yml               # Конфігурація GitHub Actions (CI)
├── grammar/
│   └── sipl.lark            # Формальна граматика мови SIPL (EBNF / Lark)
├── src/sipl/
│   ├── __init__.py
│   ├── ast.py               # Типізовані вузли AST та клас SourceSpan
│   ├── parser.py            # Парсер та SIPLTransformer (Parse Tree -> AST)
│   └── interpreter.py       # Інтерпретатор мови та середовище змінних
├── tests/
│   ├── positive/            # 10 коректних SIPL-програм (вкл. приклади з практикуму)
│   └── negative/            # 10 програм із синтаксичними помилками
├── cli.py                   # Інтерфейс командного рядка
├── run_tests.py             # Скрипт запуску автоматичних тестів
├── visualize.py             # Генератор візуалізацій Parse Tree та AST
├── pyproject.toml           # Специфікація Python-пакета
├── CHANGELOG.md             # Історія змін версій
└── README.md                # Документація проєкту

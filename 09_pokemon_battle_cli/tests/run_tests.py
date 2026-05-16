"""Ejecuta TODOS los tests SIN necesitar pytest (asserts planos).

Uso (desde la carpeta del proyecto):

    python tests/run_tests.py

Es una alternativa simple a `python -m pytest -q` para cuando todavia
no tienes pytest instalado. Recorre los modulos de test, llama a cada
funcion que empiece por `test_` y cuenta cuantas pasan y fallan.
"""

import importlib
import os
import sys
import traceback

# Anade la raiz del proyecto a sys.path para poder importar `pokemon`.
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

TEST_MODULES = [
    "tests.test_types",
    "tests.test_move",
    "tests.test_pokemon",
    "tests.test_battle",
]


def main():
    passed = 0
    failed = 0
    for modname in TEST_MODULES:
        mod = importlib.import_module(modname)
        for attr in sorted(dir(mod)):
            if not attr.startswith("test_"):
                continue
            fn = getattr(mod, attr)
            if not callable(fn):
                continue
            try:
                fn()
                passed += 1
                print(f"PASS  {modname}.{attr}")
            except Exception:
                failed += 1
                print(f"FAIL  {modname}.{attr}")
                traceback.print_exc()

    print(f"\n{passed} passed, {failed} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

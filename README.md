# Curso Python con Pokemon

Aprende Python **desde cero** (sin saber nada de programacion)
construyendo una **batalla Pokemon por terminal**: tipos y debilidades,
movimientos, PP, dano y combate por turnos. Solo libreria estandar de
Python, nada de bases de datos ni cosas avanzadas.

Documentacion navegable: **https://danielmf31.github.io/Curso_Python_Pokemon/**

## Instalacion en un solo paso (Ubuntu virgen)

No necesitas saber git ni GitHub. Descarga el instalador con el
navegador y ejecutalo:

```bash
bash ~/Descargas/bootstrap.sh
```

(El fichero esta en `scripts/bootstrap.sh`. Instala Python, VS Code,
el entorno virtual, y descarga el proyecto en `~/Curso_Python_Pokemon`.)

Atajo para quien ya tiene `curl` y confia en la fuente:

```bash
curl -fsSL https://raw.githubusercontent.com/DanielMf31/Curso_Python_Pokemon/main/scripts/bootstrap.sh | bash
```

## Estructura

```
Curso_Python_Pokemon/
├── 09_pokemon_battle_cli/            # MODELO: juego completo + docs (referencia)
│   ├── pokemon/  main.py  tests/  scripts/setup.sh
│   └── docs/                         # 00..12 + glosario + challenges + index
├── 09_pokemon_battle_cli_practica/   # PRACTICA: igual pero con huecos TODO
├── scripts/
│   ├── bootstrap.sh                  # instalador de un paso
│   └── wikilinks_to_md.py            # (solo CI) convierte [[wikilinks]]
├── mkdocs.yml                        # config de la web de docs
├── requirements-docs.txt
└── .github/workflows/deploy.yml      # publica la web en GitHub Pages
```

## Como se usa el curso

1. Abre las dos carpetas en VS Code (modelo + practica) en vista
   dividida.
2. Lee la teoria (web de docs o `09_pokemon_battle_cli/docs/`).
3. Implementa los `TODO` de la **practica** guiandote por los mensajes
   de `NotImplementedError` y la documentacion.
4. Verifica:

   ```bash
   cd 09_pokemon_battle_cli_practica
   python -m pytest -q          # o, sin pytest:  python tests/run_tests.py
   ```

   Cuando todo este en verde, juega:

   ```bash
   python main.py               # tu contra la IA
   python main.py --demo        # batalla automatica
   ```

El **modelo** ya viene completo y con 17 tests en verde: es la solucion
de referencia para mirar solo si te atascas.

## Publicar / actualizar la documentacion

La web se construye y publica sola con GitHub Actions al hacer `push` a
`main` (workflow `.github/workflows/deploy.yml`). Hay que activar
**Settings -> Pages -> Source: GitHub Actions** una vez en el repo.

Probar la web en local (opcional):

```bash
pip install -r requirements-docs.txt
python scripts/wikilinks_to_md.py 09_pokemon_battle_cli/docs
mkdocs serve
```

## Licencia

MIT — ver [LICENSE](LICENSE).

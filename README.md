# Proyecto Final – Framework de Automatización de Pruebas

Framework de testing automatizado en Python que combina pruebas de **UI** (Selenium WebDriver sobre [SauceDemo](https://www.saucedemo.com)) y pruebas de **API** (Requests sobre [JSONPlaceholder](https://jsonplaceholder.typicode.com)), con reportes HTML, logging y capturas de pantalla automáticas en los fallos.

## Tecnologías
- Python 3.10+
- Pytest + pytest-html
- Selenium WebDriver (Chrome)
- Requests
- Git / GitHub (y GitHub Actions para CI)

## Estructura del proyecto
```
├── pages/            # Page Object Model (BasePage, Login, Inventory, Cart, Checkout)
├── tests/
│   ├── ui/           # Tests de interfaz (login, inventario/carrito, checkout)
│   └── api/          # Tests de API (GET, POST, DELETE, encadenamiento)
├── data/             # Datos de prueba externos (CSV y JSON)
├── utils/            # Config, logger y lector de datos
├── reports/          # Reporte HTML, log y screenshots de fallos
├── conftest.py       # Fixtures (driver) y hook de screenshots en fallos
├── pytest.ini        # Configuración de pytest y reporte HTML
└── .github/workflows # Pipeline de GitHub Actions
```

## Instalación
```bash
git clone <https://github.com/danieloliveros96/proyecto-final-automation-testing-daniel-oliveros>
cd proyecto-final-automation-testing-daniel-oliveros
python -m venv .venv
# Windows (Git Bash): source .venv/Scripts/activate
# Linux/Mac:          source .venv/bin/activate
pip install -r requirements.txt
```
Requiere Google Chrome instalado (Selenium Manager descarga el driver automáticamente).

## Ejecución
```bash
pytest                    # todos los tests
pytest -m ui              # solo UI
pytest -m api             # solo API
pytest -m negative        # solo escenarios negativos
HEADLESS=true pytest      # navegador sin ventana
```

## Reportes y logs
- Reporte HTML: `reports/report.html` (estado, duración y screenshots de los tests fallidos)
- Log detallado: `reports/test_run.log`
- Screenshots: `reports/screenshots/<fecha_hora>_<nombre_test>.png`

## Casos cubiertos
**UI:** login data-driven (CSV, incluye casos negativos), logout, agregar/quitar productos del carrito, ordenamiento por precio, checkout completo y checkout con datos faltantes (JSON).
**API:** GET exitoso, GET 404, POST, DELETE y encadenamiento de peticiones.

## Decisiones de diseño
- Cada test UI abre su propio navegador, por lo que son independientes entre sí.
- La lógica de interacción vive en las páginas; los tests solo contienen acciones de alto nivel y assertions.
- Para agregar una prueba nueva: crear/ampliar un page object en `pages/` y un archivo en `tests/`.

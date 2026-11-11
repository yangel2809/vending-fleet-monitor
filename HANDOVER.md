# Handover — vending-fleet-monitor

> Última actualización: 2026-11-11 · Rama por defecto: `main`

## 1. Resumen
CLI en Python que lee telemetría de máquinas expendedoras desde un CSV, genera alertas (sin stock, stock bajo, errores de pago, offline) y propone una ruta de reabastecimiento (vecino más cercano + haversine) desde un depósito. Según el README es una **demo de portafolio** con datos ficticios; no se conecta a ninguna fuente real de telemetría. Estado: demo terminada, 1 solo commit (2026-09-12).

## 2. Stack
- Python 3.10+ (usa `X | None` en anotaciones; se usa `from __future__ import annotations`). Solo stdlib (`csv`, `math`, `dataclasses`, `enum`).
- `pytest>=8.0` (única dependencia, solo para tests).
- Sin BD.

## 3. Estructura del repositorio
```
src/main.py                         # Entry point CLI (load_data → evaluate → summarize/CSV → build_route)
src/models.py                       # Dataclasses frozen: Machine, TelemetryReading, Alert; enums AlertType, AlertSeverity
src/monitoring/alert_rules.py       # Reglas puras + tupla RULES; umbrales LOW_STOCK_THRESHOLD=20, PAYMENT_ERROR_THRESHOLD=3
src/routing/route_optimizer.py      # haversine_distance_km, build_route (nearest neighbor), total_distance_km
src/reports/report_generator.py     # summarize() a texto, write_alerts_csv()
data/sample_machines.csv            # 6 máquinas ficticias + fila DEPOT
tests/                              # test_alert_rules.py, test_route_optimizer.py
```
Los imports son absolutos `from src....`; `main.py` y los tests hacen `sys.path.insert` del directorio raíz.

## 4. Puesta en marcha local
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python src/main.py data/sample_machines.csv   # arg opcional; default data/sample_machines.csv (relativo al cwd)
pytest
```
Ejecutar desde la raíz del repo. Genera `alerts_report.csv` en el directorio actual.

## 5. Configuración y variables de entorno
No usa variables de entorno ni archivos de config. Los umbrales son constantes en `src/monitoring/alert_rules.py`.

| Elemento | Propósito |
|---|---|
| Argumento CLI 1 | Ruta del CSV de entrada |
| `LOW_STOCK_THRESHOLD`, `PAYMENT_ERROR_THRESHOLD` | Umbrales de alerta (constantes en código) |

## 6. Base de datos
No aplica. Formato de entrada CSV: `machine_id,name,latitude,longitude,stock_percentage,payment_errors_last_hour,is_online`. La fila con `machine_id == "DEPOT"` es obligatoria (punto de partida de la ruta) y se excluye de las alertas.

## 7. Despliegue
No hay empaquetado (sin `pyproject.toml`/`setup.py`, Dockerfile ni CI). Se usa como script local.

## 8. Integraciones externas
Ninguna. La lectura de telemetría real (API/MQTT/BD) no existe; habría que sustituir `load_data()` en `src/main.py`.

## 9. Funcionalidades principales
- `evaluate(reading)`: aplica `check_stock`, `check_payment_errors`, `check_connectivity`. Añadir una regla = nueva función + añadirla a `RULES`.
- Ruta: solo incluye máquinas con `OUT_OF_STOCK`/`LOW_STOCK`. No vuelve al depósito (la distancia total no incluye el retorno).
- Reporte: resumen por consola + `alerts_report.csv`.

## 10. Estado actual y pendientes
- Un único commit "first commit" (2026-09-12). Sin TODO/FIXME en el código.
- Pendientes naturales: fuente de telemetría real, retorno al depósito en la ruta, umbrales configurables.

## 11. Riesgos y deuda técnica
- `src/main.py`: `machines["DEPOT"]` lanza `KeyError` si el CSV no trae fila DEPOT; no hay validación de columnas/valores del CSV.
- `src/main.py`: la ruta se construye desde un `set` (`needs_restock_ids`), así que en empates el orden puede no ser determinista.
- `write_alerts_csv` escribe siempre `alerts_report.csv` en el cwd y no hay `.gitignore` en el repo: riesgo de commitear el reporte.
- Sin CI; los tests (`tests/`) cubren reglas y ruteo, pero no `main.py` ni `report_generator.py`.
> Por confirmar: los tests no se ejecutaron en este traspaso (pytest no estaba instalado en el entorno).

## 12. Accesos y contactos
> Por confirmar: no hay servidores ni cuentas asociadas. Repo: `github.com/yangel2809/vending-fleet-monitor`. Responsable/propietario del proyecto por confirmar.

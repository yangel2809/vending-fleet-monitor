# Vending Fleet Monitor

Herramienta en Python para **monitoreo de una red de máquinas expendedoras** y **optimización de rutas de reabastecimiento** — las dos áreas que, en mi experiencia real gestionando una red de máquinas, más dolores de cabeza generan cuando se hacen manualmente.

> ⚠️ Este repositorio es una **demostración con fines de portafolio**, con datos ficticios (`data/sample_machines.csv`). No contiene código, datos ni lógica de ningún cliente — refleja el patrón general del problema, no una implementación específica.

## Problema que resuelve

Una red de máquinas expendedoras reporta telemetría (nivel de stock, estado del pago, si está online) de forma periódica. Dos preguntas se repiten todos los días:

1. **¿Qué máquinas necesitan atención ahora?** (sin stock, con error de pago, fuera de línea)
2. **¿En qué orden debería visitarlas el técnico de reabastecimiento** para minimizar el recorrido?

Este proyecto responde ambas con lógica simple, explicable y sin dependencias pesadas.

## Estructura

```
src/
├── models.py                     # Machine, TelemetryReading, Alert (dataclasses)
├── monitoring/
│   └── alert_rules.py            # Reglas para detectar problemas a partir de la telemetría
├── routing/
│   └── route_optimizer.py        # Ruta de reabastecimiento (vecino más cercano, distancia haversine)
├── reports/
│   └── report_generator.py       # Resumen diario en texto/CSV
└── main.py                       # CLI: une todo el flujo
data/sample_machines.csv          # Datos ficticios para probar
tests/                            # Tests unitarios de las reglas y el ruteo
```

## Decisiones de diseño (a propósito, para mostrar criterio)

- **Reglas de alerta separadas del modelo de datos** — agregar una alerta nueva (ej. "temperatura fuera de rango" en máquinas refrigeradas) no toca `models.py`.
- **Ruteo con vecino más cercano (nearest neighbor)** — no es óptimo matemáticamente, pero es simple, rápido y suficientemente bueno para rutas de 10-30 paradas; documentado el trade-off en el código en vez de sobre-ingenierizar con un solver exacto que nadie necesita en este tamaño de problema.
- **Sin dependencias externas** para la lógica core (solo `stdlib`) — el reporte en CSV usa `csv` nativo. Esto hace el proyecto trivial de instalar y correr en cualquier lado.

## Uso

```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt   # solo pytest, para los tests
python src/main.py data/sample_machines.csv
```

## Tests

```bash
pytest
```

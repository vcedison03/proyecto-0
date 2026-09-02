
# Proyecto Consolidador de Ventas - Sucursales

Este proyecto automatiza el proceso de ETL (Extracción, Transformación y Carga) para consolidar los reportes de ventas de cuatro sucursales (Barranquilla, Bogotá, Cali y Medellín).

## Estructura del Proyecto

- `data/`: Contiene los archivos de entrada `.csv` y `.xlsx` de cada sucursal.
- `resultados/`: Almacena los entregables finales:
  - `consolidado_limpio.xlsx`: Reporte general unificado y depurado.
  - `grafico_categoria.png`: Gráfico de ventas por categoría.
  - `grafico_vendedor.png`: Gráfico de participación por vendedor.
- `main.py`: Script principal ejecutable.

## Ejecución

Para realizar la inspección y consolidación completa, ejecuta en la terminal:

```bash
python main.py
```

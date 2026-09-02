import glob
import pandas as pd

# Buscar los archivos de las 4 sucursales
archivos = glob.glob("sucursal_*.csv") + glob.glob("sucursal_*.xlsx")

if not archivos:
    print("Error: No se encontraron archivos de sucursales.")
    exit()

# Iterar e inspeccionar CADA UNO de los 4 archivos por separado
for archivo in archivos:
    print("=" * 60)
    print(f" ARCHIVO: {archivo}")
    print("=" * 60)

    # Cargar según extensión
    if archivo.endswith(".csv"):
        df = pd.read_csv(archivo)
    else:
        df = pd.read_excel(archivo, engine="openpyxl")

    # Mostrar resultados requeridos para este archivo
    print("\n--- 1. VISTA PREVIA (head) ---")
    print(df.head())

    print("\n--- 2. INFORMACIÓN GENERAL (info) ---")
    print(df.info())

    print("\n--- 3. VALORES NULOS (isnull) ---")
    print(df.isnull().sum())
    print("\n\n")


    // Para tres gráficas




    import glob
import os
import matplotlib.pyplot as plt
import pandas as pd

# 1. CREAR CARPETA DE RESULTADOS AUTOMÁTICAMENTE
CARPETA_RESULTADOS = "resultados"
if not os.path.exists(CARPETA_RESULTADOS):
    os.makedirs(CARPETA_RESULTADOS)

# 2. CARGAR ARCHIVOS DE SUCURSALES
archivos = glob.glob("sucursal_*.csv") + glob.glob("sucursal_*.xlsx")
lista_informes = []

for archivo in archivos:
    if archivo.endswith(".csv"):
        df = pd.read_csv(archivo)
    else:
        df = pd.read_excel(archivo, engine="openpyxl")
    lista_informes.append(df)

if not lista_informes:
    print("Error: No se encontraron archivos de sucursales.")
    exit()

# 3. HOMOLOGAR NOMBRES DE COLUMNAS
for i, df_item in enumerate(lista_informes):
    renombradas = {}
    for col in df_item.columns:
        c_lower = col.strip().lower()
        if "fecha" in c_lower:
            renombradas[col] = "fecha"
        elif "producto" in c_lower:
            renombradas[col] = "producto"
        elif "categoria" in c_lower or "categoría" in c_lower:
            renombradas[col] = "categoria"
        elif "cant" in c_lower:
            renombradas[col] = "cantidad"
        elif "valor" in c_lower or "precio" in c_lower:
            renombradas[col] = "precio_unitario"
        elif "vendedor" in c_lower:
            renombradas[col] = "vendedor"
        elif "pago" in c_lower:
            renombradas[col] = "metodo_pago"
    lista_informes[i] = df_item.rename(columns=renombradas)

df_consolidado = pd.concat(lista_informes, ignore_index=True)

# 4. LIMPIEZA DE DATOS
df_consolidado = df_consolidado.drop_duplicates()

if "metodo_pago" in df_consolidado.columns:
    df_consolidado["metodo_pago"] = df_consolidado["metodo_pago"].fillna(
        "No especificado"
    )

if "precio_unitario" in df_consolidado.columns:
    df_consolidado["precio_unitario"] = pd.to_numeric(
        df_consolidado["precio_unitario"], errors="coerce"
    )
    promedio = df_consolidado["precio_unitario"].mean()
    df_consolidado["precio_unitario"] = df_consolidado[
        "precio_unitario"
    ].fillna(promedio)

# ARCHIVO 1: Guardar consolidado_limpio.xlsx
ruta_excel = os.path.join(CARPETA_RESULTADOS, "consolidado_limpio.xlsx")
df_consolidado.to_excel(ruta_excel, index=False)

# 5. GENERAR LAS 2 GRÁFICAS REQUERIDAS

# ARCHIVO 2: grafico_categoria.png
if (
    "categoria" in df_consolidado.columns
    and "precio_unitario" in df_consolidado.columns
):
    plt.figure(figsize=(8, 5))
    ventas_cat = df_consolidado.groupby("categoria")["precio_unitario"].sum()
    ventas_cat.plot(kind="bar", color="skyblue")
    plt.title("Ventas por Categoría")
    plt.xlabel("Categoría")
    plt.ylabel("Ventas Totales")
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_RESULTADOS, "grafico_categoria.png"))
    plt.close()

# ARCHIVO 3: grafico_vendedor.png
if (
    "vendedor" in df_consolidado.columns
    and "precio_unitario" in df_consolidado.columns
):
    plt.figure(figsize=(6, 6))
    ventas_ven = df_consolidado.groupby("vendedor")["precio_unitario"].sum()
    ventas_ven.plot(kind="pie", autopct="%1.1f%%")
    plt.title("Participación por Vendedor")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(os.path.join(CARPETA_RESULTADOS, "grafico_vendedor.png"))
    plt.close()

print(
    "¡Proceso finalizado! Se generaron únicamente los 3 archivos requeridos en 'resultados/'."
)
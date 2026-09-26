import pandas as pd

archivo = "ventas.xlsx"

df = pd.read_excel(archivo)

print("Primeras filas del archivo:")
print(df.head())

print("\nTotal de columnas:", list(df.columns))

df["total"] = df["cantidad"] * df["precio_unitario"]

print("\nVenta total:", df["total"].sum())
print("Producto más vendido (por cantidad):", df.groupby("producto")["cantidad"].sum().idxmax())
print("Promedio de venta por operación:", df["total"].mean())
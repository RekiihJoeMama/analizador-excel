import pandas as pd

datos = {
    "producto": ["Remera", "Pantalón", "Remera", "Gorra", "Pantalón"],
    "cantidad": [5, 3, 8, 10, 2],
    "precio_unitario": [1200, 2500, 1200, 800, 2500],
    "fecha": ["2026-09-01", "2026-09-03", "2026-09-10", "2026-09-15", "2026-09-20"]
}

df = pd.DataFrame(datos)
df.to_excel("ventas.xlsx", index=False)

print("Archivo ventas.xlsx creado con éxito")
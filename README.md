🍒 Analizador de Excel

Aplicación web hecha con Flask que permite subir dos archivos Excel de ventas, compararlos, y descargar el resultado en PDF. Tema visual inspirado en Kasane Teto.

¿Qué hace?
Sube dos archivos .xlsx con columnas producto, cantidad, precio_unitario y fecha
Calcula el total de ventas, producto más vendido y promedio por operación de cada archivo
Muestra la diferencia y variación porcentual entre ambos
Muestra los datos completos de cada Excel en formato de tabla
Permite descargar un resumen comparativo en PDF
Tecnologías
Python
Flask
pandas + openpyxl (lectura de Excel)
fpdf2 (generación de PDF)
Cómo correrlo
Instalar dependencias: pip install pandas openpyxl flask fpdf2
Ejecutar la app: python app.py
Abrir en el navegador: http://127.0.0.1:5000
Formato esperado del Excel

Columnas: producto, cantidad, precio_unitario, fecha
Ejemplo de fila: Remera, 5, 1200, 2026-09-01
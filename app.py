from flask import Flask, render_template, request, send_file
import pandas as pd
from fpdf import FPDF
import io

app = Flask(__name__)

ultimo_resultado = None  # guardamos el último resultado para poder exportarlo a PDF

def analizar_excel(archivo):
    df = pd.read_excel(archivo)
    df["total"] = df["cantidad"] * df["precio_unitario"]

    # convertir fechas a texto simple, para que se vean prolijas en la tabla
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col] = df[col].dt.strftime("%Y-%m-%d")

    return {
        "total": round(df["total"].sum(), 2),
        "mas_vendido": df.groupby("producto")["cantidad"].sum().idxmax(),
        "columnas": list(df.columns),
        "filas": df.to_dict(orient="records")
    }
    
@app.route("/", methods=["GET", "POST"])
def home():
    global ultimo_resultado
    resultado = None
    error = None

    if request.method == "POST":
        archivo1 = request.files.get("archivo1")
        archivo2 = request.files.get("archivo2")

        if archivo1 and archivo1.filename.endswith(".xlsx") and archivo2 and archivo2.filename.endswith(".xlsx"):
            try:
                datos1 = analizar_excel(archivo1)
                datos2 = analizar_excel(archivo2)

                diferencia = round(datos2["total"] - datos1["total"], 2)
                variacion = round((diferencia / datos1["total"]) * 100, 1) if datos1["total"] else 0

                resultado = {
                    "archivo1": archivo1.filename,
                    "archivo2": archivo2.filename,
                    "datos1": datos1,
                    "datos2": datos2,
                    "diferencia": diferencia,
                    "variacion": variacion
                }
                ultimo_resultado = resultado
            except Exception:
                error = "No se pudieron procesar los archivos. Revisá que ambos tengan las columnas correctas (producto, cantidad, precio_unitario)."
        else:
            error = "Subí dos archivos .xlsx válidos."

    return render_template("index.html", resultado=resultado, error=error)

@app.route("/exportar-pdf")
def exportar_pdf():
    if not ultimo_resultado:
        return "Todavía no hay ningún resultado para exportar.", 400

    r = ultimo_resultado
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "Comparacion de Ventas", ln=True, align="C")
    pdf.ln(5)

    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Archivo 1: {r['archivo1']}", ln=True)
    pdf.cell(0, 8, f"  Total: ${r['datos1']['total']}  |  Producto top: {r['datos1']['mas_vendido']}", ln=True)
    pdf.ln(2)
    pdf.cell(0, 8, f"Archivo 2: {r['archivo2']}", ln=True)
    pdf.cell(0, 8, f"  Total: ${r['datos2']['total']}  |  Producto top: {r['datos2']['mas_vendido']}", ln=True)
    pdf.ln(5)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 8, f"Diferencia: ${r['diferencia']}  ({r['variacion']}%)", ln=True)

    buffer = io.BytesIO(pdf.output())
    buffer.seek(0)
    return send_file(buffer, mimetype="application/pdf", as_attachment=True, download_name="comparacion_ventas.pdf")

if __name__ == "__main__":
    app.run(debug=True)
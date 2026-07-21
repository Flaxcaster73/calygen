"""
Mi Sitio - Backend con Flask
-------------------------------------
Combina 2 herramientas en un solo servidor:
  1. Calculadora (operaciones básicas + gráfica de parábolas)
  2. Generador de contraseñas seguras

Para correrlo localmente:
    pip install -r requirements.txt
    python app.py
Luego abre: http://127.0.0.1:5000
"""

import io
import base64

import matplotlib
matplotlib.use("Agg")  # necesario para generar gráficas sin pantalla (en un servidor)
import matplotlib.pyplot as plt
import numpy as np

from flask import Flask, render_template, request, jsonify

from generador import generar_password  # código original del cliente, sin modificar la lógica

app = Flask(__name__)


# ======================================================================
# LÓGICA: Calculadora
# ======================================================================

def calcular(a, b, operacion):
    """Operaciones básicas de la calculadora."""
    if operacion == "sumar":
        return a + b
    elif operacion == "restar":
        return a - b
    elif operacion == "multiplicar":
        return a * b
    elif operacion == "dividir":
        if b == 0:
            raise ValueError("No se puede dividir entre cero")
        return a / b
    elif operacion == "potencia":
        return a ** b
    else:
        raise ValueError("Operación no reconocida")


def generar_grafica(a, b, c):
    """Grafica y = a*x^2 + b*x + c y regresa la imagen como base64."""
    x = np.linspace(-10, 10, 400)
    y = a * x**2 + b * x + c

    fig, ax = plt.subplots(figsize=(5, 3.5))
    ax.plot(x, y, color="#E8B94F", linewidth=2.5)
    ax.axhline(0, color="#F5F3E7", linewidth=0.8, alpha=0.4)
    ax.axvline(0, color="#F5F3E7", linewidth=0.8, alpha=0.4)
    ax.set_facecolor("#1E3A2F")
    fig.patch.set_facecolor("#1E3A2F")
    ax.tick_params(colors="#F5F3E7")
    for spine in ax.spines.values():
        spine.set_color("#F5F3E7")
    ax.set_title(f"y = {a}x² + {b}x + {c}", color="#F5F3E7")

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png", bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    return base64.b64encode(buffer.read()).decode("utf-8")


# ======================================================================
# RUTAS: páginas
# ======================================================================

@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/calculadora")
def calculadora():
    return render_template("calculadora.html")


@app.route("/generador")
def generador():
    return render_template("generador.html")


# ======================================================================
# RUTAS: API (las que llama el JavaScript)
# ======================================================================

@app.route("/api/calcular", methods=["POST"])
def api_calcular():
    datos = request.get_json()
    try:
        a = float(datos.get("a"))
        b = float(datos.get("b"))
        operacion = datos.get("operacion")
        resultado = calcular(a, b, operacion)
        return jsonify({"ok": True, "resultado": resultado})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400


@app.route("/api/graficar", methods=["POST"])
def api_graficar():
    datos = request.get_json()
    try:
        a = float(datos.get("a", 0))
        b = float(datos.get("b", 0))
        c = float(datos.get("c", 0))
        imagen_base64 = generar_grafica(a, b, c)
        return jsonify({"ok": True, "imagen": imagen_base64})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400


@app.route("/api/generar-password", methods=["POST"])
def api_generar_password():
    datos = request.get_json()
    try:
        longitud = int(datos.get("longitud", 18))
        especiales = bool(datos.get("especiales", True))
        password = generar_password(incluir_especiales=especiales, nn=longitud)
        return jsonify({"ok": True, "password": password})
    except Exception as e:
        return jsonify({"ok": False, "error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True)

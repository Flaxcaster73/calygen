// Cambiar entre pestañas (Operaciones / Graficar)
document.querySelectorAll(".tab").forEach((tab) => {
  tab.addEventListener("click", () => {
    document.querySelectorAll(".tab").forEach((t) => t.classList.remove("activo"));
    document.querySelectorAll(".panel").forEach((p) => p.classList.remove("activo"));
    tab.classList.add("activo");
    document.getElementById("panel-" + tab.dataset.tab).classList.add("activo");
  });
});

// ---- Operaciones básicas ----
const resultadoValor = document.querySelector("#resultado-operacion .resultado-valor");

document.querySelectorAll(".op").forEach((boton) => {
  boton.addEventListener("click", async () => {
    const a = document.getElementById("valor-a").value;
    const b = document.getElementById("valor-b").value;
    const operacion = boton.dataset.op;

    resultadoValor.textContent = "...";
    resultadoValor.classList.remove("error");

    try {
      const respuesta = await fetch("/api/calcular", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ a, b, operacion }),
      });
      const datos = await respuesta.json();

      if (datos.ok) {
        resultadoValor.textContent = datos.resultado;
      } else {
        resultadoValor.textContent = datos.error;
        resultadoValor.classList.add("error");
      }
    } catch (error) {
      resultadoValor.textContent = "Error de conexión";
      resultadoValor.classList.add("error");
    }
  });
});

// ---- Graficar parábola ----
const btnGraficar = document.getElementById("btn-graficar");
const contenedorGrafica = document.getElementById("contenedor-grafica");

btnGraficar.addEventListener("click", async () => {
  const a = document.getElementById("g-a").value;
  const b = document.getElementById("g-b").value;
  const c = document.getElementById("g-c").value;

  btnGraficar.disabled = true;
  btnGraficar.textContent = "Dibujando...";

  try {
    const respuesta = await fetch("/api/graficar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ a, b, c }),
    });
    const datos = await respuesta.json();

    if (datos.ok) {
      contenedorGrafica.innerHTML = `<img src="data:image/png;base64,${datos.imagen}" alt="Gráfica de la parábola">`;
    } else {
      contenedorGrafica.innerHTML = `<p class="placeholder-grafica">${datos.error}</p>`;
    }
  } catch (error) {
    contenedorGrafica.innerHTML = `<p class="placeholder-grafica">Error de conexión</p>`;
  } finally {
    btnGraficar.disabled = false;
    btnGraficar.textContent = "Dibujar gráfica";
  }
});

const sliderLongitud = document.getElementById("longitud");
const longitudValor = document.getElementById("longitud-valor");
const checkboxEspeciales = document.getElementById("incluir-especiales");
const btnGenerar = document.getElementById("btn-generar");
const passwordValor = document.getElementById("password-valor");
const btnCopiar = document.getElementById("btn-copiar");

sliderLongitud.addEventListener("input", () => {
  longitudValor.textContent = sliderLongitud.value;
});

btnGenerar.addEventListener("click", async () => {
  btnGenerar.disabled = true;
  btnGenerar.textContent = "Generando...";

  try {
    const respuesta = await fetch("/api/generar-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        longitud: sliderLongitud.value,
        especiales: checkboxEspeciales.checked,
      }),
    });
    const datos = await respuesta.json();

    if (datos.ok) {
      passwordValor.textContent = datos.password;
    } else {
      passwordValor.textContent = datos.error;
    }
  } catch (error) {
    passwordValor.textContent = "Error de conexión";
  } finally {
    btnGenerar.disabled = false;
    btnGenerar.textContent = "Generar contraseña";
  }
});

btnCopiar.addEventListener("click", () => {
  const texto = passwordValor.textContent;
  if (!texto || texto === "—") return;

  navigator.clipboard.writeText(texto).then(() => {
    const original = btnCopiar.textContent;
    btnCopiar.textContent = "¡Copiado!";
    setTimeout(() => (btnCopiar.textContent = original), 1500);
  });
});

// Generar una al cargar la página, para que no se vea vacío
btnGenerar.click();

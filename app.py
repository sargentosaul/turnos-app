import streamlit as st

# 👇 USUARIO Y CONTRASEÑA (puedes cambiarlos)
USUARIO = "admin"
PASSWORD = "1234"

# 👇 CONTROL DE SESIÓN
if "login_ok" not in st.session_state:
    st.session_state.login_ok = False

# 👇 FORM LOGIN
if not st.session_state.login_ok:
    st.title("🔐 Acceso al sistema")

    user = st.text_input("Usuario")
    pwd = st.text_input("Contraseña", type="password")

    if st.button("Ingresar"):
        if user == USUARIO and pwd == PASSWORD:
            st.session_state.login_ok = True
            st.success("✅ Acceso permitido")
            st.rerun()
        else:
            st.error("❌ Usuario o contraseña incorrectos")

    st.stop()  # 🔥 BLOQUEA TODO LO DEMÁS

import streamlit as st
import pandas as pd
import io

st.title("📅 Sistema de Turnos Automático")

# 👇 INPUT DE USUARIO
st.subheader("👥 Ingreso de trabajadores")

texto = st.text_area(
    "Escribe los nombres (uno por línea)",
    "Juan\nPedro\nLuis\nAna\nCarlos"
)

trabajadores = [t.strip() for t in texto.split("\n") if t.strip() != ""]

dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"]

# Horarios
horario_normal = "08:30-17:54 (1h colación)"
horario_ajustado = "08:30-17:06 (1h colación)"
horario_sabado = "09:30-13:30"

# Horas reales
horas_normal = 8.4
horas_ajustada = 7.6
horas_sabado = 4

# Semana rotativa
semana = st.number_input("Semana de rotación", min_value=1, value=1)

tabla = []

for i, trabajador in enumerate(trabajadores):

    fila = {"Trabajador": trabajador}

    trabaja_sabado = ((i + semana) % len(trabajadores)) < 5

    horas_totales = 0

    for dia in dias:

        if dia == "Sábado":
            if trabaja_sabado:
                fila[dia] = horario_sabado
                horas_totales += horas_sabado
            else:
                fila[dia] = "Libre"

        else:
            if trabaja_sabado:
                fila[dia] = horario_ajustado
                horas_totales += horas_ajustada
            else:
                fila[dia] = horario_normal
                horas_totales += horas_normal

    fila["Horas Semanales"] = round(horas_totales, 1)
    tabla.append(fila)

df = pd.DataFrame(tabla)

# Mostrar tabla
st.dataframe(df)

# Exportar Excel
st.subheader("📥 Descargar planificación")

def convertir_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    return output.getvalue()

st.download_button(
    label="⬇ Descargar Excel",
    data=convertir_excel(df),
    file_name="turnos.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# Validación
st.subheader("🔍 Control de horas")

if not df.empty:
    exceso = df[df["Horas Semanales"] > 42]

    if not exceso.empty:
        st.error("⚠ Hay trabajadores con más de 42 horas")
        st.dataframe(exceso)
    else:
        st.success("✅ Todo correcto")
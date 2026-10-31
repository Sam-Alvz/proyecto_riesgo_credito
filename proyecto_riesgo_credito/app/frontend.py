import streamlit as st
import requests

st.set_page_config(page_title="Riesgo Crediticio IA", layout="wide")
st.title("Sistema de Evaluación de Riesgo Crediticio")
st.markdown("Interfaz conectada vía API REST al modelo calibrado (Umbral = 0.46).")

c1, c2 = st.columns(2)

with c1:
    st.subheader("Condiciones Financieras")
    credit_amount = st.number_input("Monto solicitado (DM):", 100, 50000, 2500)
    month_duration = st.number_input("Duración (meses):", 4, 72, 18)
    payment_to_income_ratio = st.slider("Tasa cuota/ingresos (%):", 1, 4, 2)
    purpose = st.selectbox("Propósito:", ["radio/television", "car (new)", "furniture/equipment", "education", "repairs", "business"])
    status_account = st.selectbox("Estado de cuenta corriente:", ["< 0 DM", "0 to < 200 DM", ">= 200 DM", "no checking account"])
    status_savings = st.selectbox("Estado de cuenta de ahorros:", ["< 100 DM", "100 to < 500 DM", "500 to < 1000 DM", ">= 1000 DM", "unknown/ no savings account"])
    credit_history = st.selectbox("Historial crediticio:", [
        "critical account/ other credits existing (not at this bank)",
        "existing credits paid back duly till now",
        "delay in paying off in the past",
        "all credits at this bank paid back duly",
        "no credits taken/ all credits paid back duly"
    ])

with c2:
    st.subheader("Datos del Solicitante")
    age = st.number_input("Edad:", 18, 100, 35)
    years_employment = st.selectbox("Años empleo actual:", ["unemployed", "< 1 year", "1 to < 4 years", "4 to < 7 years", ">= 7 years"])
    job = st.selectbox("Categoría laboral:", ["unskilled - non-resident", "unskilled - resident", "skilled employee/ official", "management/ highly qualified employee"])
    housing = st.selectbox("Vivienda:", ["own", "rent", "for free"])
    status_and_sex = st.selectbox("Estado civil / sexo:", ["male : single", "female : divorced/separated/married", "male : married/widowed", "male : divorced/separated"])
    secondary_obligor = st.selectbox("Deudores / Avales:", ["none", "guarantor", "co-applicant"])
    collateral = st.selectbox("Garantía:", ["none", "car", "savings agreement/life insurance", "real estate"])
    residence_since = st.slider("Años en residencia actual:", 1, 4, 2)
    n_credits = st.number_input("Créditos vigentes en el banco:", 1, 4, 1)
    other_installment_plans = st.selectbox("Otros planes de pago:", ["none", "bank", "stores"])
    n_guarantors = st.number_input("Dependientes a su cargo:", 1, 2, 1)
    telephone = st.selectbox("Teléfono registrado:", ["yes, registered under the customers name", "none"])
    is_foreign_worker = st.selectbox("Trabajador extranjero:", ["yes", "no"])

st.markdown("---")

if st.button("Evaluar Solicitud de Crédito", type="primary"):
    payload = {
        "status_account": status_account,
        "month_duration": int(month_duration),
        "credit_history": credit_history,
        "purpose": purpose,
        "credit_amount": int(credit_amount),
        "status_savings": status_savings,
        "years_employment": years_employment,
        "payment_to_income_ratio": int(payment_to_income_ratio),
        "status_and_sex": status_and_sex,
        "secondary_obligor": secondary_obligor,
        "residence_since": int(residence_since),
        "collateral": collateral,
        "age": int(age),
        "other_installment_plans": other_installment_plans,
        "housing": housing,
        "n_credits": int(n_credits),
        "job": job,
        "n_guarantors": int(n_guarantors),
        "telephone": telephone,
        "is_foreign_worker": is_foreign_worker
    }
    
    url_api = "http://127.0.0.1:8000/predecir"
    try:
        resp = requests.post(url_api, json=payload)
        if resp.status_code == 200:
            resultado = resp.json()
            st.success("Dictamen procesado correctamente.")
            col_a, col_b, col_c = st.columns(3)
            col_a.metric("Dictamen Final", resultado["dictamen"])
            col_b.metric("Probabilidad de Impago", f"{resultado['probabilidad_impago'] * 100:.2f}%")
            col_c.metric("Umbral de Decisión", resultado["umbral_aplicado"])
            st.info(f"Acción Operativa: {resultado['accion_sugerida']}")
        else:
            st.error(f"Error {resp.status_code}: {resp.text}")
    except Exception as err:
        st.error(f"No hay conexión con la API en {url_api}. Verifica que el backend esté en ejecución.")
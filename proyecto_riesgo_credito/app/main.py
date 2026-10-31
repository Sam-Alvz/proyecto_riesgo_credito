import os
import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(
    title="API de Evaluación de Riesgo Crediticio",
    description="Servicio backend para inferencia de riesgo crediticio usando Random Forest calibrado",
    version="1.0"
)

# Carga directa del modelo sin usar _file_
ruta_fija_docker = "/app/modelo/modelo_credito.joblib"
ruta_local = os.path.join("modelo", "modelo_credito.joblib")

if os.path.exists(ruta_fija_docker):
    paquete = joblib.load(ruta_fija_docker)
elif os.path.exists(ruta_local):
    paquete = joblib.load(ruta_local)
else:
    raise RuntimeError("No se encontro el archivo modelo_credito.joblib")

modelo = paquete['pipeline']
umbral = paquete['umbral_operativo']

class SolicitudCredito(BaseModel):
    status_account: str
    month_duration: int
    credit_history: str
    purpose: str
    credit_amount: int
    status_savings: str
    years_employment: str
    payment_to_income_ratio: int
    status_and_sex: str
    secondary_obligor: str
    residence_since: int
    collateral: str
    age: int
    other_installment_plans: str
    housing: str
    n_credits: int
    job: str
    n_guarantors: int
    telephone: str
    is_foreign_worker: str

@app.get("/")
def verificar_salud():
    return {
        "estado": "Activo",
        "mensaje": "Servicio de Inferencia Crediticia Operativo",
        "umbral_configurado": umbral
    }

@app.post("/predecir")
def clasificar_solicitud(solicitud: SolicitudCredito):
    try:
        df_entrada = pd.DataFrame([solicitud.model_dump()])
        prob_impago = float(modelo.predict_proba(df_entrada)[0][1])
        es_riesgoso = prob_impago >= umbral

        return {
            "dictamen": "Rechazado / Riesgo Alto" if es_riesgoso else "Aprobado / Riesgo Bajo",
            "probabilidad_impago": round(prob_impago, 4),
            "umbral_aplicado": umbral,
            "accion_sugerida": "Enviar a comite para revision manual y garantia" if es_riesgoso else "Aprobacion directa de linea"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
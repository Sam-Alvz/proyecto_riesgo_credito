# Sistema de Evaluación de Riesgo Crediticio con Machine Learning

Este repositorio contiene la solución contenerizada para la inferencia y consumo en tiempo real de un modelo de clasificación binaria entrenado con el dataset German Credit Data. El sistema evalúa el riesgo crediticio de solicitantes y determina la viabilidad de aprobación o rechazo con base en un umbral operativo calibrado.

---

## 1. Arquitectura Técnica

El proyecto integra un pipeline desacoplado compuesto por:
- *Backend (FastAPI):* Expone un servicio REST con validación de esquemas vía Pydantic (/predecir y /) para recibir perfiles financieros y calcular la probabilidad de impago.
- *Frontend (Streamlit):* Proporciona una interfaz web interactiva para capturar variables socioeconómicas y consultar el dictamen del modelo.
- *Modelo de Clasificación:* Random Forest calibrado con preprocesamiento (ColumnTransformer con StandardScaler y OneHotEncoder).
- *Umbral Operativo de Decisión:* *0.46* (optimizado para penalizar los falsos negativos y reducir pérdidas por impago frente al corte estándar de 0.50).
- *Contenerización (Docker):* Empaqueta ambos componentes en un contenedor único basado en Python 3.10 para garantizar portabilidad y reproducibilidad.

---

## 2. Requisitos Previos

- Tener instalado [Docker Desktop](https://www.docker.com/products/docker-desktop/) con soporte WSL 2 en Windows.
- O bien, un entorno local con Python 3.10+.

---

## 3. Despliegue con Docker

### Paso 1: Clonar el repositorio
```bash
git clone https://github.com/Sam-Alvz/proyecto_riesgo_credito.git
cd proyecto_riesgo_credito
```
### Paso 2: Construir la imagen del contenedor
```bash
docker build -t evaluador-credito-ia:v1 .
```
### Paso 3: Ejecutar el contenedor
```bash
docker run -d -p 8000:8000 -p 8501:8501 --name contenedor_credito evaluador-credito-ia:v1
```
---
## 4. Acceso a los Servicios
Interfaz Gráfica (Streamlit): http://localhost:8501

Documentación Interactiva de la API (Swagger UI): http://localhost:8000/docs

Verificación de Salud de la API: http://localhost:8000/

---
## 5. Ejecución Local sin Docker (Alternativa)
Si deseas probar el entorno sin contenedor:

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Iniciar la API (terminal 1):**
```bash
uvicorn app.main:app --reload --port 8000
```

3. **Iniciar Streamlit (terminal 2):**
```bash
streamlit run app/frontend.py
```

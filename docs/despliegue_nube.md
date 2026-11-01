# Manual de Despliegue en la Nube

**Guía operativa para la publicación de la solución contenerizada (FastAPI + Streamlit)**

## 1. Propósito y Alcance del Manual
Este manual describe los pasos técnicos y requerimientos operativos necesarios para llevar el sistema de evaluación de riesgo crediticio desde un entorno local hacia una plataforma en la nube. La solución está empaquetada mediante Docker, lo que garantiza que pueda desplegarse de manera idéntica en cualquier servicio de hosting que soporte contenedores sin necesidad de reconfigurar dependencias ni modificar el código fuente.

---

## 2. Requerimientos Técnicos del Sistema
Antes de iniciar el aprovisionamiento en la nube, se debe verificar que la infraestructura cumpla con las siguientes especificaciones:

* **Recursos de cómputo mínimos:** 1 CPU virtual (vCPU) y 1 GB de memoria RAM (recomendado 2 GB para soportar la ejecución concurrente del pipeline de `scikit-learn` y la interfaz gráfica de `Streamlit`).
* **Runtime / Motor de ejecución:** Soporte para contenedores compatibles con OCI/Docker (o Linux con Python 3.10).
* **Configuración de red:** Exposición de puertos para tráfico web. En local se emplean el puerto `8000` (FastAPI) y el puerto `8501` (Streamlit). En la nube, la plataforma debe mapear el puerto `8501` hacia el puerto `80/443` con certificado SSL/HTTPS activo.
* **Variables de entorno:** `PYTHONUNBUFFERED=1` y `PYTHONDONTWRITEBYTECODE=1` (configuradas por defecto en el `Dockerfile`).
* **Control de versiones:** Acceso al repositorio público en GitHub ([https://github.com/Sam-Alvz/proyecto_riesgo_credito.git](https://github.com/Sam-Alvz/proyecto_riesgo_credito.git)) para habilitar integración y despliegue continuo (CI/CD).

---

## 3. Estrategia de Despliegue
Para este proyecto se definió una estrategia de despliegue basada en contenedores sobre una plataforma PaaS (Platform as a Service), como Render, Google Cloud Run o AWS App Runner, por los siguientes motivos operativos:

* **Aislamiento absoluto:** Al empaquetar el sistema con una imagen oficial de Python 3.10, todas las dependencias científicas (`scikit-learn`, `pandas`, `joblib`) quedan fijadas dentro de la imagen, eliminando cualquier inconsistencia entre entornos.
* **Simplicidad de mantenimiento:** A diferencia de un servidor virtual dedicado (IaaS), un entorno PaaS se encarga de la seguridad del sistema operativo base, certificados SSL automáticos y reinicio en caso de caídas, permitiendo concentrarse en la operación del modelo.
* **Despliegue continuo (CI/CD):** Cualquier actualización realizada en el repositorio de GitHub desencadena automáticamente una reconstrucción de la imagen y su puesta en marcha sin intervención manual.

---

## 4. Procedimiento de Despliegue Paso a Paso

### Paso 1: Preparación y validación del repositorio
Verificar que la rama principal (`main`) del repositorio en GitHub cuente con los siguientes componentes en la raíz:
* `Dockerfile`: Define la imagen base, instalación de requerimientos y comando de arranque doble.
* `requirements.txt`: Lista de dependencias limpias (`fastapi`, `uvicorn`, `streamlit`, `scikit-learn`, `pandas`, etc.).
* Carpeta `app/`: Contiene `main.py` (backend) y `frontend.py` (interfaz de usuario).
* Carpeta `modelo/`: Contiene el artefacto binario `modelo_credito.joblib`.

### Paso 2: Conexión del servicio en la nube
1. Iniciar sesión en la plataforma seleccionada (por ejemplo, Render.com).
2. Seleccionar la opción de crear un nuevo **Web Service**.
3. Vincular la cuenta con GitHub y seleccionar el repositorio: `Sam-Alvz/proyecto_riesgo_credito`.

### Paso 3: Configuración del entorno de ejecución
Configurar los parámetros del servicio en el panel de la plataforma:
* **Entorno de ejecución (Environment):** Docker.
* **Rama (Branch):** `main`.
* **Región:** Seleccionar la más cercana al usuario final (por ejemplo, US East / Ohio).
* **Plan de cómputo:** Seleccionar un plan con al menos 1 GB o 2 GB de RAM.

### Paso 4: Compilación y aprovisionamiento automático
Hacer clic en **Create Web Service**. La plataforma ejecutará automáticamente las instrucciones del `Dockerfile`:

```dockerfile
FROM python:3.10
RUN pip install --no-cache-dir -r requirements.txt
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port 8000 & sleep 2 && streamlit run app/frontend.py --server.port 8501 --server.address 0.0.0.0"]

import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier

# 1. Cargar el dataset desde la misma carpeta local
print("Leyendo dataset local german_credit_data.csv...")
df = pd.read_csv("german_credit_data.csv")

# 2. Mapear la columna target: 1 = bad (alto riesgo / impago), 0 = good (bajo riesgo)
df['target_num'] = df['target'].map({'good': 0, 'bad': 1})
X = df.drop(columns=['target', 'target_num'])
y = df['target_num']

# 3. Separar columnas por tipo
numeric_cols = X.select_dtypes(include=['int64', 'float64']).columns.tolist()
categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()

# 4. Preprocesamiento: estandarización para numéricas y One-Hot para categóricas
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_cols),
        ('cat', OneHotEncoder(drop='first', handle_unknown='ignore', sparse_output=False), categorical_cols)
    ]
)

# 5. Pipeline con los hiperparámetros validados
rf_pipeline = Pipeline([
    ('prep', preprocessor),
    ('clf', RandomForestClassifier(n_estimators=150, max_depth=6, class_weight='balanced', random_state=42))
])

# 6. Entrenamiento con el conjunto de datos
print("Entrenando el modelo...")
rf_pipeline.fit(X, y)

# 7. Empaquetar pipeline y umbral óptimo calibrado (0.46)
paquete_modelo = {
    'pipeline': rf_pipeline,
    'umbral_operativo': 0.46,
    'columnas_numericas': numeric_cols,
    'columnas_categoricas': categorical_cols
}

# 8. Guardar archivo del modelo
joblib.dump(paquete_modelo, "modelo_credito.joblib")
print("Listo. Se creo el archivo modelo_credito.joblib con exito.")
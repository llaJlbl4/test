from fastapi import FastAPI, HTTPException
import pandas as pd
import joblib
from pydantic import BaseModel
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder

app = FastAPI()

# Загружаем данные
DATA_PATH = "new1.csv"
df = pd.read_csv(DATA_PATH, sep=";")

DATA_PATH_2 = "new2.csv"
df2 = pd.read_csv(DATA_PATH_2, sep=";")

DATA_PATH_3 = "new3.csv"
df3 = pd.read_csv(DATA_PATH_3, sep=";")

# Загружаем обученную модель
MODEL_PATH = "model.pkl"
model = joblib.load(MODEL_PATH)

MODEL_PATH_2 = "model1.pkl"
model2 = joblib.load(MODEL_PATH_2)

MODEL_PATH_3 = "model2.pkl"
model3 = joblib.load(MODEL_PATH_3)

# Добавляем прогноз на 2024 год в DataFrame
if "year" in df.columns and "indicator_value" in df.columns:
    df_2024 = df.copy()
    df_2024["year"] = 2024  # Устанавливаем год 2024
    df_2024["indicator_value"] = model.predict(df_2024.drop(columns=["indicator_value", "object_name"]))  # Делаем прогноз
    df = pd.concat([df, df_2024], ignore_index=True, axis=0)
else:
    raise ValueError("В данных отсутствуют необходимые столбцы (year, target)")

le = LabelEncoder()
df2["age"] = le.fit_transform(df2["age"])

class PredictionRequest(BaseModel):
    model: str
    sex: str  # Будем принимать строковые значения
    age: str
    object_name: str
    year: int

@app.post("/predict")
def predict(request: PredictionRequest):
    sex_mapping = {"Оба пола": 0, "Мужчины": 1, "Женщины": 2}
    if request.sex not in sex_mapping:
        raise HTTPException(status_code=400, detail="Некорректное значение для пола")
    """Возвращает прогноз на 2024 год по заданным характеристикам."""
    if request.model == "Средняя продолжительность жизни":
        filtered_df = df[(df["object_name"] == request.object_name) & (df["sex"] == sex_mapping[request.sex]) & (df["age"] == int(request.age)) & (df["year"] == request.year)]
    elif request.model == "Возрастной коэффицент смертности":
        age_mapping = {"0 лет": 0, "1-4 года": 1, "5-9 лет": 2, "10-14 лет": 3, "15-19 лет": 4, "20-24 лет": 5, "25-29 лет": 6, "30-34 лет": 7, "35-39 лет": 8, "40-44 лет": 9, "45-49 лет": 10, "50-54 лет": 11, "55-59 лет": 12, "60-64 лет": 13, "65-69 лет": 14, "70-74 лет": 15, "75-79 лет": 16, "80-84 лет": 17, "85 лет и более": 18}
        filtered_df = df2[(df2["object_name"] == request.object_name) & (df2["sex"] == sex_mapping[request.sex]) & (df2["age"] == int(age_mapping[request.age])) & (df2["year"] == request.year)]
    elif request.model == "Стандартизированный возрастной коэффициент смертности":
        age_mapping = {"0-14 лет": 0, "15-49 лет": 1, "50-64 лет": 2, "65 лет и более": 3, "Все возраста": 4}
        filtered_df = df3[(df3["object_name"] == request.object_name) & (df3["sex"] == sex_mapping[request.sex]) & (df3["age"] == int(age_mapping[request.age])) & (df3["year"] == request.year)]
    if filtered_df.empty:
        raise HTTPException(status_code=404, detail="Нет данных для заданных параметров")
    
    return {"prediction": filtered_df["indicator_value"].values[0]}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
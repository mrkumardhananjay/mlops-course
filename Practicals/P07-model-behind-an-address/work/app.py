"The delivery-time prediction service."

from pathlib import Path

import joblib
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel, Field

HERE = Path(__file__).resolve().parent
FEATURES = ["distance_km", "prep_time_min", "traffic_level", "rain"]

app = FastAPI(
    title="Delivery Time Predictor",
    description="Predicts how many minutes a food order will take.",
    version="1.0.0",
)

model = joblib.load(HERE / "model.joblib")


class Order(BaseModel):
    "One food order waiting to be delivered."

    distance_km: float = Field(..., gt=0, le=50, examples=[4.2])
    prep_time_min: int = Field(..., ge=0, le=120, examples=[12])
    traffic_level: int = Field(..., ge=1, le=3, examples=[2])
    rain: int = Field(..., ge=0, le=1, examples=[0])


class Prediction(BaseModel):
    delivery_min: float
    model_version: str


@app.get("/health")
def health():
    "Is the service up, and is a model loaded?"
    return {"status": "ok", "model_loaded": model is not None}


@app.post("/predict", response_model=Prediction)
def predict(order: Order):
    "Predict the delivery time for one order, in minutes."
    row = pd.DataFrame([order.model_dump()])[FEATURES]
    minutes = float(model.predict(row)[0])
    return Prediction(delivery_min=round(minutes, 1),
                      model_version=app.version)



@app.get("/model-info")
def model_info():
    "Describe the model this service is running."
    # TODO: return the three keys described in the task
    return {}

from pathlib import Path

import joblib
import pandas as pd
import streamlit as st


@st.cache_resource
def load_model():
    model_path = Path(__file__).resolve().parents[2] / 'artifacts' / 'flight_price_model.joblib'
    return joblib.load(model_path)


def predict_price(features):
    data = pd.DataFrame([features])
    return float(load_model().predict(data)[0])

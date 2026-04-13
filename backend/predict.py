import numpy as np
import joblib
import cv2
from tensorflow.keras.models import load_model

fog_model = load_model("../Models/fog_model.h5")
accident_model = joblib.load("../Models/accident_model.pkl")
le_y = joblib.load("../Models/accident_label_encoder.pkl")
encoders = joblib.load("../Models/feature_encoders.pkl")

FOG_CLASSES = {
    0: "Dense Fog",
    1: "Medium Fog",
    2: "No Fog"
}

ACCIDENT_CLASSES = {
    0: "Fatal",
    1: "Serious",
    2: "Slight"
}

def predict_fog(image):
    image = image.resize((128, 128))
    image = np.array(image)

    if image.shape[-1] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2RGB)

    image = image / 255.0

    gray = cv2.cvtColor((image * 255).astype('uint8'), cv2.COLOR_RGB2GRAY)
    edges = cv2.Canny(gray, 50, 150)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    gray = gray / 255.0
    edges = edges / 255.0
    blur = blur / 255.0

    image_6ch = np.stack([
        image[:,:,0],
        image[:,:,1],
        image[:,:,2],
        gray,
        edges,
        blur
    ], axis=-1)

    image_6ch = np.expand_dims(image_6ch, axis=0)

    pred = fog_model.predict(image_6ch)
    class_idx = int(np.argmax(pred))
    return class_idx, FOG_CLASSES[class_idx]


def predict_accident(speed, weather, road, time):

    weather_map = {
        "Clear":   "Fine no high winds",
        "Rainy":   "Raining no high winds",
        "Cloudy":  "Fine + high winds",
        "Snowing": "Snowing no high winds"
    }

    road_map = {
        "Dry": "Dry",
        "Wet": "Wet or damp",
        "Icy": "Frost or ice"
    }

    time_map = {
        "Day":   "Daylight",
        "Night": "Darkness - lights lit"
    }

    w_str = weather_map.get(weather, "Fine no high winds")
    r_str = road_map.get(road, "Dry")
    t_str = time_map.get(time, "Daylight")

    w_enc = encoders['Weather_Conditions']
    r_enc = encoders['Road_Surface_Conditions']
    t_enc = encoders['Light_Conditions']

    w = int(w_enc.transform([w_str])[0])
    r = int(r_enc.transform([r_str])[0])
    t = int(t_enc.transform([t_str])[0])

    features = np.array([[speed, w, r, t]])

    raw = accident_model.predict(features)[0]
    acc_idx = int(raw)
    return acc_idx, ACCIDENT_CLASSES.get(acc_idx, "Slight")


def final_risk(fog_idx, accident_idx, speed=60, weather="Clear", road="Dry"):

    # Fog risk score
    fog_score_map = {0: 3, 1: 2, 2: 0}
    fog_score = fog_score_map.get(fog_idx, 0)

    # Accident severity score
    acc_score_map = {0: 3, 1: 2, 2: 1}
    acc_score = acc_score_map.get(accident_idx, 0)

    # Speed bonus
    if speed > 90:
        speed_bonus = 1.5
    elif speed > 60:
        speed_bonus = 0.8
    else:
        speed_bonus = 0.0

    # Weather bonus
    if weather in ["Rainy", "Snowing"]:
        weather_bonus = 0.8
    else:
        weather_bonus = 0.0

    # Road bonus
    if road == "Icy":
        road_bonus = 0.6
    elif road == "Wet":
        road_bonus = 0.3
    else:
        road_bonus = 0.0

    score = (fog_score * 0.5 + 
             acc_score * 0.2 + 
             speed_bonus * 0.3 + 
             weather_bonus * 0.2 + 
             road_bonus * 0.1)

    if score >= 2.0:
        return "HIGH RISK 🚨"
    elif score >= 1.0:
        return "MEDIUM RISK ⚠️"
    else:
        return "LOW RISK ✅"
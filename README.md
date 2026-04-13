# 🌫️ FOGVISION — AI-Based Fog Detection & Accident Risk Prediction System

## 🔍 What Does This Project Do?
FOGVISION ek intelligent road safety system hai jo AI use karke:
- 📸 Road image se **fog level detect** karta hai
- 🚗 Driving conditions analyze karke **accident risk predict** karta hai
- ⚠️ Driver ko **real-time HIGH / MEDIUM / LOW alert** deta hai

---

## 🚀 Key Features

### 🌫️ 1. Fog Detection (CNN Model)
- Road image upload karo — system batayega kitna fog hai
- 3 classes: **Dense Fog / Medium Fog / No Fog**
- 86.67% accuracy ke saath detect karta hai

### 🚗 2. Accident Risk Prediction (ML Model)
- Speed, weather, road surface, light conditions input lo
- **Fatal / Serious / Slight** severity predict karta hai
- 100,000 real UK accident records pe trained

### 📊 3. Risk Analysis Dashboard
- Dono models ka combined score
- Visual risk meter — GREEN / YELLOW / RED
- Saare factors ek jagah dikhata hai

### 🆘 4. Emergency Links
- 🚑 Nearby Hospital finder
- 🚔 Police / SOS button
- 🔧 Roadside Assistance
- 🏨 Safe Stay nearby

### 💡 5. Safety Tips Module
- Fog mein driving protocol
- Speed recommendations
- Headlight & braking tips
- Step-by-step fog safety guide

---

## 🧠 AI Models

### Fog Detection — CNN (Convolutional Neural Network)
| Parameter | Detail |
|-----------|--------|
| Framework | TensorFlow / Keras |
| Input | 128x128 image (6-channel: RGB + Grayscale + Edge + Blur) |
| Output | Dense Fog / Medium Fog / No Fog |
| Accuracy | **86.67%** |
| Architecture | Conv2D → MaxPooling → Dropout → Dense |
| Epochs | 20 |

### Accident Severity — Gradient Boosting Classifier
| Parameter | Detail |
|-----------|--------|
| Framework | Scikit-learn |
| Input Features | Speed limit, Weather, Road surface, Light conditions |
| Output | Fatal / Serious / Slight |
| Dataset Size | 100,000 records |
| Balancing | SMOTE (86,341 samples per class) |

---

## 📊 Dataset Details

### 🌫️ Fog Dataset — Foggy Cityscapes
| Class | Images |
|-------|--------|
| Dense Fog | 500 images |
| Medium Fog | 500 images |
| No Fog | 500 images |
| **Total** | **1500 images** |

### 🚗 Accident Dataset — UK Road Safety Data
| Detail | Value |
|--------|-------|
| Total Records | 1,00,000 |
| Features Used | Speed, Weather, Road, Light |
| Classes | Fatal, Serious, Slight |
| Source | UK Government Road Safety Dataset |

---

## 📈 Model Performance

### Fog Model
| Metric | Value |
|--------|-------|
| Validation Accuracy | **86.67%** |
| Epochs | 20 |
| Input Size | 128×128×6 |

### Accident Model
| Class | Precision | Recall | F1-Score |
|-------|-----------|--------|----------|
| Fatal | 0.54 | 0.55 | 0.54 |
| Serious | 0.39 | 0.17 | 0.24 |
| Slight | 0.43 | 0.66 | 0.52 |

---

## ⚙️ Tech Stack
| Component | Technology |
|-----------|-----------|
| Frontend UI | Streamlit |
| Fog Detection | TensorFlow / Keras CNN |
| Accident Prediction | Scikit-learn Gradient Boosting |
| Image Processing | OpenCV |
| Class Balancing | SMOTE (imbalanced-learn) |
| Language | Python 3.12 |

---

## 🗂️ Project Structure
FOGVISION/
├── frontend/
│   └── app.py                    # Streamlit UI (4 pages)
├── backend/
│   └── predict.py                # Model inference logic
├── Models/
│   ├── fog_model.h5              # CNN fog model (86.67% acc)
│   ├── accident_model.pkl        # Gradient Boosting model
│   ├── accident_label_encoder.pkl
│   └── feature_encoders.pkl
├── requirements.txt
└── README.md

---

## 🛠️ How to Run Locally
git clone https://github.com/anyayadav98-stack/Fogvision.git
cd Fogvision
pip install -r requirements.txt
cd frontend
streamlit run app.py

---



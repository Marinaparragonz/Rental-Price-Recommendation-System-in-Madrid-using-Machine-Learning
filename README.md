# 🏠 Madrid Property Price Prediction System

A machine learning system for predicting rental prices in Madrid using Random Forest algorithm, selected after comprehensive model comparison for its superior performance.

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Model Selection](#model-selection)
- [Results](#results)
- [License](#license)

## 🎯 Overview

End-to-end ML solution for Madrid rental price prediction combining data analysis, model evaluation, and interactive visualization.

**Key Features:**
- Multi-model evaluation and comparison
- Random Forest as optimal selected model
- Interactive Streamlit dashboard
- Real-time price predictions
- Market insights and analytics

## ✨ Features

- **🤖 ML Models**: Random Forest, Linear Regression, XGBoost, LightGBM comparison
- **📊 Dashboard**: Interactive price predictions with property filters
- **🗺️ Maps**: District-based visualization and selection
- **📈 Analytics**: Market insights and model performance metrics

## 🛠️ Technology Stack

- **Backend**: Python, Pandas, NumPy, Scikit-learn
- **Frontend**: Streamlit, Plotly, Folium
- **ML**: Random Forest Regression (final model)

## 📂 Project Structure

```
Rental-Price-Recommendation-System-in-Madrid-using-Machine-Learning/
│
├── 📁 data/                           
│   ├── data_clean.csv               
│   └── madrid-districts.geojson     
│
├── 📁 models/                        
│   ├── random_forest_model.pkl      
│   ├── model_features.pkl            
│   ├── model_info.pkl               
│   └── district_mapping.pkl          
│
├── 📁 notebooks/                     
│   ├── 01_EDA.ipynb                 
│   ├── 02_Linear_Regression.ipynb    
│   ├── 03_Random_Forest.ipynb       
│   └── 04_XGBoost_LightGBM.ipynb     
│
├── 📁 dashboard/                     
│   ├── main.py                       
│   ├── 📁 components/               
│   ├── 📁 utils/                     
│   └── 📁 config/                    
│
├── 📄 requirements.txt               
└── 📄 README.md                      
```

## 🚀 Installation

```bash
# Clone repository
git clone https://github.com/yourusername/Rental-Price-Recommendation-System-in-Madrid-using-Machine-Learning.git
cd Rental-Price-Recommendation-System-in-Madrid-using-Machine-Learning

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

## 🎮 Usage

### Launch Dashboard
```bash
cd dashboard
streamlit run main.py
```
Access at `http://localhost:8501`

### Model Development
```bash
# Explore different models
jupyter notebook notebooks/01_EDA.ipynb                  # Data exploration
jupyter notebook notebooks/02_Linear_Regression.ipynb   # Baseline model
jupyter notebook notebooks/03_Random_Forest.ipynb       # Selected model
jupyter notebook notebooks/04_XGBoost_LightGBM.ipynb    # Advanced models
```

## 🔍 Model Selection

### Performance Comparison

| Model | RMSE | R² Score | MAE |
|-------|------|----------|-----|
| **Random Forest** | **€85,674** | **0.9251** | **€47,701** |
| Linear Regression | €142,503 | 0.7928 | €94,840 |
| XGBoost | €102,980 | 0.8918 | €62,270 |
| LightGBM | €87,227 | 0.9224 | €51,280 |

### Why Random Forest?
- ✅ **Highest accuracy**: 92.51% (R² Score)
- ✅ **Lowest error**: €85,674 RMSE
- ✅ **Best MAE**: €47,701 mean absolute error
- ✅ **Robust performance**: Stable across property types
- ✅ **Feature interpretability**: Clear importance rankings

## 📝 License

MIT License - see [LICENSE](LICENSE) file for details.

---

<div align="center">

🏠 Accurate • 📊 Interactive • 🤖 AI



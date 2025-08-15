# Madrid Property Price Prediction System

A machine learning system for predicting rental prices in Madrid using Random Forest algorithm, selected after comprehensive model comparison for its superior performance.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Model Selection](#model-selection)
- [Results](#results)
- [License](#license)

## Overview

End-to-end machine learning solution for Madrid rental price prediction combining data analysis, model evaluation, and interactive visualization.

**Key Features:**
- Multi-model evaluation and comparison
- Random Forest as optimal selected model
- Interactive Streamlit dashboard
- Real-time price predictions
- Market insights and analytics

## Features

- **Machine Learning Models**: Random Forest, Linear Regression, XGBoost, LightGBM comparison
- **Interactive Dashboard**: Real-time price predictions with property filters
- **Geographic Visualization**: District-based maps and property selection
- **Market Analytics**: Comprehensive insights and model performance metrics

## Technology Stack

- **Backend**: Python, Pandas, NumPy, Scikit-learn
- **Frontend**: Streamlit, Plotly, Folium
- **Machine Learning**: Random Forest Regression (final model)

## Project Structure

```
Rental-Price-Recommendation-System-in-Madrid-using-Machine-Learning/
│
├── data/                           
│   ├── data_clean.csv               
│   └── madrid-districts.geojson     
│
├── models/                        
│   ├── random_forest_model.pkl      
│   ├── model_features.pkl            
│   ├── model_info.pkl               
│   └── district_mapping.pkl          
│
├── notebooks/                     
│   ├── 01_EDA.ipynb                 
│   ├── 02_Linear_Regression.ipynb    
│   ├── 03_Random_Forest.ipynb       
│   └── 04_XGBoost_LightGBM.ipynb     
│
├── dashboard/                     
│   ├── main.py                       
│   ├── components/               
│   ├── utils/                     
│   └── config/                    
│
├── requirements.txt               
└── README.md                      
```

## Installation

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

## Usage

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

## Model Selection

### Performance Comparison

| Model | RMSE | R² Score | MAE |
|-------|------|----------|-----|
| **Random Forest** | **€85,674** | **0.9251** | **€47,701** |
| Linear Regression | €142,503 | 0.7928 | €94,840 |
| XGBoost | €102,980 | 0.8918 | €62,270 |
| LightGBM | €87,227 | 0.9224 | €51,280 |

### Selection Rationale
- **Highest accuracy**: 92.51% prediction accuracy (R² Score)
- **Lowest error rates**: €85,674 RMSE and €47,701 MAE
- **Robust performance**: Consistent results across property types
- **Feature interpretability**: Clear importance rankings for business insights

## Results

### Model Performance
- **Prediction Accuracy**: 92.51% (R² Score)
- **Root Mean Square Error**: €85,674
- **Mean Absolute Error**: €47,701
- **Feature Count**: 20+ property characteristics
- **Validation Method**: 5-fold cross-validation

### Feature Importance Rankings
1. **Property Area** (34%)
2. **District Location** (28%) 
3. **Number of Rooms** (15%)
4. **Number of Bathrooms** (12%)
5. **Floor Level** (7%)
6. **Amenities** (4%)

### Business Applications
- Accurate price predictions for property valuation
- Real-time estimation for investment decisions
- Market analysis for real estate professionals
- Data-driven pricing strategies for property owners

## License

MIT License - see [LICENSE](LICENSE) file for details.

---




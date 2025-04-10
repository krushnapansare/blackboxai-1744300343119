import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer

def load_and_preprocess_data(filepath):
    """Load and preprocess diet recommendation dataset"""
    # Load data
    data = pd.read_csv(filepath)
    
    # Define preprocessing pipeline
    numeric_features = ['age', 'height', 'weight']
    categorical_features = ['gender', 'activity_level', 'health_conditions', 'dietary_restrictions']
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(), categorical_features)
        ])
    
    # Apply preprocessing
    processed_data = preprocessor.fit_transform(data)
    
    return processed_data, preprocessor

def calculate_bmr(weight, height, age, gender):
    """Calculate Basal Metabolic Rate"""
    # Convert inputs to float
    weight = float(weight)
    height = float(height)
    age = float(age)
    
    if str(gender).lower() == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr

def calculate_tdee(bmr, activity_level):
    """Calculate Total Daily Energy Expenditure"""
    try:
        bmr = float(bmr)
        activity_level = str(activity_level).lower()
        
        activity_multipliers = {
            'sedentary': 1.2,
            'light': 1.375,
            'moderate': 1.55,
            'active': 1.725,
            'very_active': 1.9
        }
        return bmr * activity_multipliers.get(activity_level, 1.2)
    except (ValueError, TypeError):
        return bmr * 1.2  # Default to sedentary if invalid input

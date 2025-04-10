import pandas as pd
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib
import os

# Create models directory if it doesn't exist
os.makedirs('../models', exist_ok=True)

def train_models():
    """Train and save ML models for diet recommendations"""
    # Load sample data
    data = pd.read_csv('/project/sandbox/user-workspace/diet-recommender/data/sample_data.csv')
    
    # Preprocess data
    categorical_features = ['gender', 'activity_level', 'health_conditions', 
                          'dietary_restrictions', 'goal']
    numerical_features = ['age', 'height', 'weight']
    
    # Create preprocessing pipeline
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', 'passthrough', numerical_features),
            ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_features)
        ])
    
    # Train calorie prediction model
    calorie_model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    calorie_model.fit(data[numerical_features + categorical_features], 
                     data['daily_calories'])
    
    # Train meal plan model (classifier)
    meal_model = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', RandomForestClassifier(n_estimators=100, random_state=42))
    ])
    meal_model.fit(data[numerical_features + categorical_features],
                  data['meal_plan'])
    
    # Save models using absolute paths
    models_dir = '/project/sandbox/user-workspace/diet-recommender/models'
    os.makedirs(models_dir, exist_ok=True)
    joblib.dump(calorie_model, f'{models_dir}/calorie_model.joblib')
    joblib.dump(meal_model, f'{models_dir}/meal_model.joblib')
    
    print("Both models trained and saved successfully")

def load_models():
    """Load trained models from disk"""
    try:
        calorie_model = joblib.load('/project/sandbox/user-workspace/diet-recommender/models/calorie_model.joblib')
        meal_model = joblib.load('/project/sandbox/user-workspace/diet-recommender/models/meal_model.joblib')
        return calorie_model, meal_model
    except FileNotFoundError as e:
        print(f"Model loading error: {e}")
        # Train models if they don't exist
        train_models()
        calorie_model = joblib.load('/project/sandbox/user-workspace/diet-recommender/models/calorie_model.joblib')
        meal_model = joblib.load('/project/sandbox/user-workspace/diet-recommender/models/meal_model.joblib')
        return calorie_model, meal_model

if __name__ == '__main__':
    train_models()

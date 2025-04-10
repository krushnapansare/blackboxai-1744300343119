from flask import Flask, request, jsonify
from .data_processing import calculate_bmr, calculate_tdee
from .model_training import load_models
import joblib
import numpy as np
import pandas as pd

app = Flask(__name__, static_folder='../frontend', static_url_path='')

# Load models at startup
calorie_model, meal_model = load_models()

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/predict', methods=['POST'])
def predict():
    """Endpoint for diet recommendations"""
    data = request.json
    
    # Validate required fields
    required_fields = ['age', 'height', 'weight', 'gender', 'activity_level']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Calculate calorie needs
    bmr = calculate_bmr(
        weight=data['weight'],
        height=data['height'],
        age=data['age'],
        gender=data['gender']
    )
    tdee = calculate_tdee(bmr, data['activity_level'])
    
    # Prepare features for models
    # Create DataFrame with same column structure as training data
    # Set default values for optional fields
    health_conditions = data.get('health_conditions', 'none')
    dietary_restrictions = data.get('dietary_restrictions', 'none')
    goal = data.get('goal', 'maintain')

    features = pd.DataFrame({
        'age': [data['age']],
        'height': [data['height']],
        'weight': [data['weight']],
        'gender': [data['gender']],
        'activity_level': [data['activity_level']],
        'health_conditions': [health_conditions],
        'dietary_restrictions': [dietary_restrictions],
        'goal': [goal]
    })
    
    # Get predictions
    calorie_pred = calorie_model.predict(features)[0]
    meal_plan = meal_model.predict(features)[0]
    
    return jsonify({
        'daily_calories': round(tdee),
        'recommended_calories': round(calorie_pred),
        'meal_plan': meal_plan,
        'macronutrients': {
            'protein': round(calorie_pred * 0.3 / 4),  # 30% calories from protein
            'carbs': round(calorie_pred * 0.4 / 4),   # 40% calories from carbs
            'fat': round(calorie_pred * 0.3 / 9)      # 30% calories from fat
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=8000)

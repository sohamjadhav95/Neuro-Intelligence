import pandas as pd
import joblib
import os
from autogluon.tabular import TabularPredictor

def test_heart_disease_prediction():
    """
    A simple debug script to test heart disease prediction directly
    without the complex UI or preprocessing pipeline.
    """
    # Hard-coded values for a known sample
    test_data = {
        'age': 62,
        'sex': 0,
        'cp': 0,
        'trestbps': 138,
        'chol': 294,
        'fbs': 1,
        'restecg': 1,
        'thalach': 106,
        'exang': 0,
        'oldpeak': 1.9,
        'slope': 1,
        'ca': 3,
        'thal': 2
    }
    
    # Create DataFrame
    df = pd.DataFrame([test_data])
    print("\n=== Test Input Data ===")
    print(df)
    
    # Load the model - try different possible target column names
    possible_target_names = ['target', 'target_1', 'label']
    predictor = None
    
    for target_name in possible_target_names:
        model_dir = f"./autogluon_model_{target_name}"
        if os.path.exists(model_dir):
            print(f"Found model with target column: {target_name}")
            predictor = TabularPredictor.load(model_dir)
            break
    
    if predictor is None:
        print("No model found. Please make sure a model has been trained.")
        return
    
    # Get model metadata
    print("\n=== Model Information ===")
    print(f"Problem type: {predictor.problem_type}")
    print(f"Required features: {predictor.feature_metadata.get_features()}")
    
    # Get training data information
    training_info = predictor.info()
    print(f"Model fit time: {training_info.get('fit_time')} seconds")
    print(f"Model accuracy: {training_info.get('val_score')}")
    
    # Check if we need to preprocess the data
    # For simplicity, let's assume the model was trained on the raw data
    # In reality, we should inspect some training samples to check format
    
    # Make direct prediction (bypassing preprocessing)
    raw_prediction = None
    try:
        raw_prediction = predictor.predict(df)
        print("\n=== Direct Model Prediction ===")
        print(f"Raw prediction: {raw_prediction}")
        print(f"Raw prediction type: {type(raw_prediction)}")
        
        # Get the single value
        if isinstance(raw_prediction, pd.Series):
            prediction_value = raw_prediction.iloc[0]
        else:
            prediction_value = raw_prediction[0]
            
        # Handle boolean type conversion
        if isinstance(prediction_value, bool):
            prediction_value = int(prediction_value)
            
        print(f"Final prediction value: {prediction_value}")
        print(f"Prediction value type: {type(prediction_value)}")
    except Exception as e:
        print(f"Error making direct prediction: {e}")
    
    # Try prediction with transform for regression problems
    if predictor.problem_type == 'regression' and raw_prediction is not None:
        try:
            # Check if we have scalers for inverse transform
            scaler_path = "scalers.pkl"
            if os.path.exists(scaler_path):
                scalers = joblib.load(scaler_path)
                print("\n=== Available Scalers ===")
                print(list(scalers.keys()))
                
                # Assuming target name is one of the above tested names
                for target_name in possible_target_names:
                    if target_name in scalers:
                        scaler = scalers[target_name]
                        pred_value = prediction_value
                        transformed_pred = scaler.inverse_transform([[pred_value]])[0][0]
                        print(f"Inverse transformed prediction: {transformed_pred}")
        except Exception as e:
            print(f"Error with inverse transformation: {e}")
    
    return raw_prediction


if __name__ == "__main__":
    print("==== Heart Disease Prediction Debug Tool ====")
    test_heart_disease_prediction()
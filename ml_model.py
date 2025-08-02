import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

def train_and_predict_movement(df):
    """
    Trains a Logistic Regression model to predict next-day price movement.
    
    Args:
        df (pd.DataFrame): DataFrame with stock data and indicators.
        
    Returns:
        float: The model's prediction accuracy.
    """
    df['Target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)
    df = df.dropna()

    features = ['RSI', '20_DMA', '50_DMA', 'Volume']
    X = df[features]
    y = df['Target']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    
    print(f"ML Model Prediction Accuracy: {accuracy:.2f}")
    return accuracy
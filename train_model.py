# backend/train_model.py

import os
import pandas as pd
import numpy as np
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

# ✅ Safely load dataset using relative path
csv_path = os.path.join(os.path.dirname(__file__), '..', 'Data', 'credit_card_synthetic.csv')
df = pd.read_csv(csv_path)

# Drop rows with missing values (if any)
df.dropna(inplace=True)

# Encode categorical features
label_encoders = {}
categorical_cols = ['merchantCategoryCode', 'transactionType', 'geoLocation', 'timeOfDay']

for col in categorical_cols:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col])
    label_encoders[col] = le

# Define features and target
X = df.drop(columns=['isFraud'])
y = df['isFraud']

# Scale numerical features
scaler = StandardScaler()
numeric_cols = ['creditLimit', 'availableCredit', 'amount', 'paymentDueInDays', 'lastPaymentAmount']
X[numeric_cols] = scaler.fit_transform(X[numeric_cols])

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# Train model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print("📊 Classification Report:\n")
print(classification_report(y_test, y_pred))

# Save model and tools to backend/
joblib.dump(model, 'model.pkl')
joblib.dump(scaler, 'scaler.pkl')
joblib.dump(label_encoders, 'label_encoders.pkl')
joblib.dump(X.columns.tolist(), 'feature_order.pkl')  # ✅ Save column order

print("\n✅ Model, scaler, encoders, and feature order saved to ba

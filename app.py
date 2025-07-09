from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import joblib

# --- Initialize Flask App ---
app = Flask(__name__)
CORS(app)

# --- Load trained components ---
model = joblib.load("model.pkl")
scaler = joblib.load("scaler.pkl")
label_encoders = joblib.load("label_encoders.pkl")
feature_order = joblib.load("feature_order.pkl")

# ------------------------------
# 🔮 Predict Endpoint
# ------------------------------
@app.route('/api/predict', methods=['POST'])
def predict():
    try:
        data = request.json

        # Step 1: Process & typecast features in order
        processed_data = {}
        for feat in feature_order:
            val = data.get(feat)

            if feat == 'isCardPresent':
                val = str(val).lower() == 'true'
            elif feat in ['isForeignTransaction', 'isFlaggedFraud']:
                val = int(val)

            processed_data[feat] = val

        # Step 2: Apply label encoders
        for col, le in label_encoders.items():
            if col in processed_data:
                try:
                    processed_data[col] = le.transform([processed_data[col]])[0]
                except ValueError:
                    return jsonify({"error": f"Invalid value '{processed_data[col]}' for '{col}'."}), 400

        # Step 3: Build DataFrame in correct order
        input_df = pd.DataFrame([[processed_data[feat] for feat in feature_order]], columns=feature_order)

        # Step 4: Scale numeric values
        numeric_cols = ['creditLimit', 'availableCredit', 'amount', 'paymentDueInDays', 'lastPaymentAmount']
        input_df[numeric_cols] = scaler.transform(input_df[numeric_cols])

        # Step 5: Predict
        prediction = model.predict(input_df)[0]
        confidence = model.predict_proba(input_df)[0][prediction]

        # Step 6: Explanation
        explanation = "This transaction appears SAFE."
        if prediction == 1:
            explanation = "This transaction was flagged as FRAUD."
            if not processed_data['isCardPresent'] and processed_data['amount'] > 3000:
                explanation += " Large online transaction with card not present."
            if processed_data['isForeignTransaction'] == 1 and processed_data['amount'] > 1000:
                explanation += " Foreign transaction detected."
            if processed_data['isFlaggedFraud'] == 1:
                explanation += " Manually flagged as suspicious."
        else:
            explanation += " No red flags detected."

        return jsonify({
            "prediction": int(prediction),
            "confidence": round(confidence * 100, 2),
            "explanation": explanation
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ------------------------------
# 📊 Dashboard Data Endpoint
# ------------------------------
@app.route('/api/dashboard-data', methods=['GET'])
def dashboard_data():
    try:
        print("✅ /api/dashboard-data called")
        df = pd.read_csv("Data/credit_card_synthetic.csv")

        return jsonify({
            "fraudStats": df['isFraud'].value_counts().to_dict(),
            "transactionType": df['transactionType'].value_counts().to_dict(),
            "merchantCategory": df['merchantCategoryCode'].value_counts().to_dict(),
            "cardPresence": df['isCardPresent'].value_counts().to_dict(),
            "avgAmounts": df.groupby('isFraud')['amount'].mean().to_dict()
        })

    except Exception as e:
        print("❌ Error in dashboard-data:", e)
        return jsonify({"error": str(e)}), 500

# ------------------------------
# 🚀 Run the server
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True)

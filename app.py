import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)

# Load the trained model
loaded_model = pickle.load(open("model.pkl", "rb"))

# Prediction function with explanation
def ValuePredictor(to_predict_list): 
    to_predict = np.array(to_predict_list).reshape(1, -1)  
    result = loaded_model.predict(to_predict)[0]

    # Generate an explanation for fraud detection
    explanation = []

    if to_predict_list[1] > 3000 or to_predict_list[1] < -1.5:
        explanation.append("High or negative transaction amount.")
    if to_predict_list[0] < 0 or to_predict_list[0] > 47:
        explanation.append("Unusual transaction timing detected.")
    if to_predict_list[2] < -1.2 or to_predict_list[2] > 2.2:
        explanation.append("Unusual transaction method used.")
    if to_predict_list[3] < -3.5 or to_predict_list[3] > 3.5:
        explanation.append("Irregular transaction ID pattern.")
    if to_predict_list[4] < -1.3 or to_predict_list[4] > 1.3:
        explanation.append("Suspicious transaction location detected.")
    if to_predict_list[5] < -1.6 or to_predict_list[5] > 1.6:
        explanation.append("Uncommon card type used.")
    if to_predict_list[6] < -1.4 or to_predict_list[6] > 1.4:
        explanation.append("Suspicious banking pattern detected.")

    reason = " | ".join(explanation) if explanation else "No suspicious activity detected."

    return result, reason

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['POST'])
def predict():
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values()) 
        to_predict_list = list(map(float, to_predict_list))  # Convert input to float

        result, reason = ValuePredictor(to_predict_list)

        if result == 1:
            prediction = "🚨 Fraudulent Transaction! " + reason +  """\n🚨 Fraudulent Transaction Detected!
\nRecommended actions:
\n- Contact the customer immediately.
\n- Freeze the transaction if unverified.
\n- Escalate to the fraud team."""
        else:
            prediction = "✅ Transaction is Safe. " + reason

        return render_template("result.html", prediction=prediction)

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__, static_folder='static', static_url_path='/static')

# Load the trained model
model = pickle.load(open('blood_forcast_lr_model.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get form data
        recency = int(request.form['recency'])
        frequency = int(request.form['frequency'])
        monetary = int(request.form['monetary'])
        time = int(request.form['time'])

        # Prepare input for prediction
        input_data = np.array([[recency, frequency, monetary, time]])
        prediction = model.predict(input_data)

        # Interpret prediction
        result = "Yes" if prediction[0] == 1 else "No"
        return render_template('index.html', prediction_text=f"Will Donate in March 2007: {result}")
    except Exception as e:
        return render_template('index.html', prediction_text=f"Error: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True, port=5004)
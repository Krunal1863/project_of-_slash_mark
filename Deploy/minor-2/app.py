# from flask import Flask, request, jsonify, render_template
# import pickle
# import numpy as np

# # Load the model
# model = pickle.load(open('house_xgboost_model.pkl', 'rb'))

# app = Flask(__name__,static_folder = 'static', static_url_path='/static')

# @app.route('/')
# def home():
#     return render_template('index.html')

# @app.route('/predict', methods=['POST'])
# def predict():
#     # Get data from form
#     features = [float(x) for x in request.form.values()]
#     final_features = np.array(features).reshape(1, -1)
    
#     # Make prediction
#     prediction = model.predict(final_features)
    
#     return render_template('index.html', prediction_text=f'Predicted House Price: ₹{prediction[0]:,.2f}')

# if __name__ == "__main__":
#     app.run(debug=True)


# change port number and set 50002 

from flask import Flask, request, jsonify, render_template
import pickle
import numpy as np

# Load the model
model = pickle.load(open('house_xgboost_model.pkl', 'rb'))

app = Flask(__name__, static_folder='static', static_url_path='/static')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get data from form
    features = [float(x) for x in request.form.values()]
    final_features = np.array(features).reshape(1, -1)
    
    # Make prediction
    prediction = model.predict(final_features)
    
    return render_template('index.html', prediction_text=f'Predicted House Price: ₹{prediction[0]:,.2f}')

if __name__ == "__main__":
    app.run(debug=True, port=5002)
import numpy as np
from flask import Flask, request, make_response, render_template, jsonify
import json
import pickle
import logging
from flask_cors import cross_origin

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
model = pickle.load(open('rfc.pkl', 'rb'))

# Configure logging
logging.basicConfig(level=logging.INFO)

# Homepage route
@app.route('/')
def hello():
    return render_template('home.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    # Get JSON data from the request
    json_data = request.json
    
    try:
        # Convert JSON data to a numpy array
        query = np.array(json_data)
        
        # Make prediction using the model
        prediction = model.predict(query)
        
        # Convert prediction to a list and return as JSON response
        return jsonify({'prediction': prediction.tolist()})
    
    except Exception as e:
        # Log the exception and return an error response
        logging.error(str(e))
        return jsonify({'error': 'An error occurred during prediction.'})

# Webhook route for Dialogflow integration
@app.route('/webhook/', methods=['GET', 'POST'])
@cross_origin()
def webhook():
    # Get JSON data from the request
    req = request.get_json(silent=True, force=True)
    
    # Process the request and generate a response
    res = processRequest(req)
    
    # Convert response to JSON and send the response
    res = json.dumps(res, indent=4)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

# Process the request from Dialogflow
def processRequest(req):
    result = req.get("queryResult")
    parameters = result.get("parameters")
    ApplicantIncome = parameters.get("Income")
    CoapplicantIncome = parameters.get("CoapplicantIncome")
    LoanAmount = parameters.get("LoanAmount")
    Credit_History = parameters.get("Credit_History")
    
    try:
        if Credit_History == "Yes":
            Credit_History = 1
        elif Credit_History == "No":
            Credit_History = 0
        # Convert string values to integers
        Credit_History = int(Credit_History)
        
        # Create the feature vector
        int_features = [ApplicantIncome, CoapplicantIncome, LoanAmount, Credit_History]
        final_features = [np.array(int_features)]
        
    except ValueError:
        # Handle incorrect information supplied
        return {"fulfillmentText": "Incorrect information supplied."}
    
    # Get the intent name
    intent = result.get("intent").get('displayName')
    
    if intent == 'Default Welcome Intent - yes':
        try:
            # Make prediction using the model
            prediction = model.predict(final_features)
            
            if prediction == 'Y':
                status = 'Congratulations! You are eligible for a loan. 😀'
            else:
                status = 'We are sorry, you are not eligible for a loan at the moment.'
            
            fulfillmentText = status
            
            return {"fulfillmentText": fulfillmentText}
        
        except Exception as e:
            # Log the exception and return an error response
            logging.error(str(e))
            return {"fulfillmentText": "An error occurred during prediction."}

if __name__ == '__main__':
    app.run(port=5000)

import numpy as np
from flask import Flask, request, make_response,render_template,jsonify
import json
import pickle
from flask_cors import cross_origin

app = Flask(__name__)
model = pickle.load(open('rfc.pkl', 'rb'))

@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/predict', methods=['POST'])
def predict():
     json_ = request.json
     query = (json_)
     prediction = model.predict(query)
     return jsonify({'prediction': list(prediction)})


# geting and sending response to dialogflow
@app.route('/webhook/', methods=['GET','POST'])
@cross_origin()
def webhook():

    req = request.get_json(silent=True, force=True)

    print("req")
    

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    #print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


# processing the request from dialogflow
def processRequest(req):

    #sessionID=req.get('responseId')
    result = req.get("queryResult")
    #print(result)

    parameters = result.get("parameters")
    ApplicantIncome=parameters.get("Income")
    CoapplicantIncome = parameters.get("CoapplicantIncome")
    LoanAmount=parameters.get("LoanAmount")
    Credit_History=parameters.get("Credit_History")
    

    if str.lower(Credit_History) == 'yes':
        Credit_History = int(1)
    elif str.lower(Credit_History) == 'no':
        Credit_History = int(0)
    else:
        return {
            "fulfillmentText": "Error please start again and enter the correct information"
            
        }

    try:
        int_features = [ApplicantIncome, CoapplicantIncome, LoanAmount,Credit_History]
        final_features = [np.array(int_features)]
    
    except ValueError:
        return {
            "fulfillmentText": "Incorrect information supplied"
        }
    

    print(final_features) 

    intent = result.get("intent").get('displayName')
    
    if (intent=='Default Welcome Intent - yes'):
        prediction = model.predict(final_features)
        print(prediction)
    
    	
        if(prediction=='Y'):
            status = 'Congratulations you are eligible for a loan 😀'
        else:
            status = 'We are sorry you are not eligible for a loan at the moment'

       
        fulfillmentText= status
        
        print(fulfillmentText)
        print(prediction)
        return {
            "fulfillmentText": fulfillmentText
        }
    

if __name__ == '__main__':
    app.run()

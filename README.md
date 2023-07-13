# Loan-predictor-chatbot

## This application simplifies the deployment of your machine learning model as a chatbot using DialogFlow and the Flask framework 



## Getting started
​

### Installing dependencies
​
1. Create a python environment using [pythonenv](https://docs.python.org/3/tutorial/venv.html) and activate it.
```bash
python3 -m venv venv
source venv/bin/activate
```
​
2. Install python libraries
```bash
pip install -r requirements.txt
```
​
### Run application
​
```bash
python app.py

```

### Test Application on postman
``` bash
Open Postman and create a new POST request.
Enter the URL of your webhook endpoint (e.g., http://localhost:5000/webhook/).
Set the request body to raw and select JSON (application/json) as the format.
Copy the sample JSON payload below
Click the Send button to send the request.
Check the response received from your Flask app in the Postman response window.
This will simulate a request from Dialogflow to your webhook and allow you to test the functionality of your Flask app.
```

```json
{
  "responseId": "123456",
  "queryResult": {
    "queryText": "Loan eligibility",
    "parameters": {
      "Income": 5000,
      "CoapplicantIncome": 2000,
      "LoanAmount": 100000,
      "Credit_History": "Yes"
    },
    "intent": {
      "displayName": "Default Welcome Intent - yes"
    }
  }
}
```

### Dockerize Application

1. Build the container image 
```bash
docker build -t loan_bot_image .
```

2. Run a container
```
docker run --rm -d -p 5000:5000 --name loan_bot loan_bot_image:latest 
```

3. Check the logs
```bash
docker logs -f stop_loss
```

## Deployment Instructions

Follow the steps in the link below to deploy the app to Heroku

https://devcenter.heroku.com/articles/getting-started-with-python?singlepage=true


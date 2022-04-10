#import flask
from flask import Flask, render_template, request, redirect
from forms import RegistrationFormClass  #forms.py should be at root to identify this
from google.cloud import bigquery
import pandas as pd     #conda install pandas-gbq -c conda-forge
from pandas.io import gbq
import os
from typing import Dict
from google.protobuf import json_format
from google.protobuf.struct_pb2 import Value
from google.cloud import aiplatform
# # If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# # called `app` in `main.py`.
#app = Flask(__name__)
app = Flask(__name__)  # template_folder='htmlfiles' path for templates folder should be above website
app.config['SECRET_KEY']='VenuAneeshDeeptiInnisECE528CLOUDCOMPUTING'   #required for forms

@app.route('/')     #default page or route to different webpages
# display helloworld
def helloworld():
   return 'Credit Approval App'

# def indexpage():
#     return render_template('base.html')

@app.route('/test')
def root(): 
    return render_template('test.html') 

@app.route('/index')
def myindexpage():
    return render_template('index.html')   #file has to be in templates folder

@app.route('/contact')
def mycontactpage():
    return render_template('contact.html')   #file has to be in templates folder

@app.route('/registration', methods=['GET','POST'])  #to get formdata methods
def registration():
    form = RegistrationFormClass()
    if form.is_submitted():
        result = request.form
        query1 = """SELECT  max(ID)+1 as ID FROM `group-project-528.credit_data.LoanData` LIMIT 1"""
        dfread=pd.read_gbq(query1, project_id="group-project-528")
        newid=dfread["ID"]
        print(newid)
        data = {
            'ID': [int(newid)],
            'Profession': [form.profession.data],
            'Married_Single': [form.marriedyn.data],
            'House_Ownership': [form.houseownership.data],
            'Car_Ownership': [bool(form.carownership.data)],
            'CITY': [form.city.data],
            'STATE': [form.state.data],
            'Income': [int(form.income.data)],
            'Age': [int(form.age.data)],
            'Experience': [int(form.experience.data)],
            'CURRENT_JOB_YRS': [int(form.currentjobyrs.data)],
            'CURRENT_HOUSE_YRS': [int(form.currenthouseyrs.data)],
            'risk_flag': '0'
        }

        # #run ml model here if we want
        instance_dict={ "Age": form.age.data, "CURRENT_HOUSE_YRS": form.currenthouseyrs.data, "CURRENT_JOB_YRS": form.currentjobyrs.data,
                "Experience": form.experience.data, "Income": form.income.data, "Car_Ownership": bool(form.carownership.data),
                "House_Ownership": form.houseownership.data, "Married_Single": form.marriedyn.data, "Profession": form.profession.data,
                "STATE": form.state.data}
        
        # # #call ml model using endpoints
        #call ml model using endpoints
        print(instance_dict)
        location= "us-central1"
        api_endpoint="us-central1-aiplatform.googleapis.com"
        project="18179477759"
        endpoint_id="2972490103273816064"
        instance_dict=instance_dict   
        
        # The AI Platform services require regional API endpoints.
        client_options = {"api_endpoint": api_endpoint}
        # Initialize client that will be used to create and send requests.
        # This client only needs to be created once, and can be reused for multiple requests.
        client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
        # for more info on the instance schema, please use get_model_sample.py
        # and look at the yaml found in instance_schema_uri
        instance = json_format.ParseDict(instance_dict, Value())
        instances = [instance]
        parameters_dict = {}
        parameters = json_format.ParseDict(parameters_dict, Value())
        endpoint = client.endpoint_path(
            project=project, location=location, endpoint=endpoint_id
        )
        response = client.predict(
            endpoint=endpoint, instances=instances, parameters=parameters
        )
        print("response")
        print(" deployed_model_id:", response.deployed_model_id)
        # See gs://google-cloud-aiplatform/schema/predict/prediction/tabular_classification_1.0.0.yaml for the format of the predictions.
        predictions = response.predictions
        for prediction in predictions:
            print(" prediction:", dict(prediction))
        # print("prediction result:", prediction[1][0])

        for prediction_ in response.predictions:
            print("Confidence Score:", prediction_["scores"])
            confidence_score = prediction_["scores"]

            # display_names = prediction_["displayNames"]
            # confidence_scores = prediction_["confidences"]
            # for count, id in enumerate(ids):
            #     print(f"Prediction ID: {id}")
            #     print(f"Prediction display name: {display_names[count]}")
            #     print(f"Prediction confidence score: {confidence_scores[count]}")

        # response='struct_value { fields { key: "classes" value { list_value { values { string_value: "1" } values { string_value: "2" } } } } fields { key: "scores" value { list_value { values { number_value: 0.5295441150665283 } values { number_value: 0.4704558551311493 } } } } } '
        # predictions = response
        # s = ""
        # for prediction in predictions:
        #     #s = s & dict(prediction)
        #     print(" prediction:", dict(prediction))
        # #deployed_model_id: "5384501955265560576" model: "projects/831128033926/locations/us-central1/models/2010685709806993408" model_display_name: "untitled_1645380369496_2022220212440""
        instances=""
        #response='response'
        # response='predictedjsonoutput'
        s=confidence_score[0]
        # instance_dict='fullinstance;'
        successmsg = "Bad"
        if s > 0.5:
            successmsg = "Good"
            riskflag="1"
        else:
            successmsg = "Bad"
            riskflag="0"

             
        df = pd.DataFrame(data)
        df['risk_flag']=riskflag 
        print(df)
        print('start')
        print(df.dtypes)
        df.to_gbq(destination_table='credit_data.LoanData', project_id='group-project-528', if_exists='append')
        print('done')

        return render_template('registrationsubmit.html',result=result, response1=response, response2=s, requestsent=instance_dict, response3=successmsg)
    return render_template('registration.html', form=form)


@app.route('/registration/<reg_id>')
def helloworld3(reg_id):
    return 'Credit Approval Registration Form ' + str(reg_id)

# @app.get("/")
# def hello():
#     """Return a friendly HTTP greeting."""
#     return "Hello World!\n"

app.run(port=8080, debug=True)

# if __name__ == "__main__":
#     # Used when running locally only. When deploying to Google App
#     # Engine, a webserver process such as Gunicorn will serve the app. This
#     # can be configured by adding an `entrypoint` to app.yaml.
#     app.run(host="localhost", port=8080, debug=True)



    








# def predict_tabular_classification_sample(
#     #project: str,
#     #endpoint_id: str,
#     #instance_dict: Dict,
#     location: str = "us-central1",
#     api_endpoint: str = "us-central1-aiplatform.googleapis.com",
#     project="831128033926",
#     endpoint_id="5803213575308705792",
#     instance_dict=instance_dict
# ):

    
    # # The AI Platform services require regional API endpoints.
    # client_options = {"api_endpoint": api_endpoint}
    # # Initialize client that will be used to create and send requests.
    # # This client only needs to be created once, and can be reused for multiple requests.
    # client = aiplatform.gapic.PredictionServiceClient(client_options=client_options)
    # # for more info on the instance schema, please use get_model_sample.py
    # # and look at the yaml found in instance_schema_uri
    # instance = json_format.ParseDict(instance_dict, Value())
    # instances = [instance]
    # parameters_dict = {}
    # parameters = json_format.ParseDict(parameters_dict, Value())
    # endpoint = client.endpoint_path(
    #     project=project, location=location, endpoint=endpoint_id
    # )
    # response = client.predict(
    #     endpoint=endpoint, instances=instances, parameters=parameters
    # )
    # print("response")
    # print(" deployed_model_id:", response.deployed_model_id)
    # # See gs://google-cloud-aiplatform/schema/predict/prediction/tabular_classification_1.0.0.yaml for the format of the predictions.
    # predictions = response.predictions
    # for prediction in predictions:
    #     print(" prediction:", dict(prediction))






import os
import pickle
import numpy as np
from typing import List
from sklearn.preprocessing import StandardScaler
from fastapi import Request, FastAPI, Response
from pydantic import BaseModel

# Load the model artifacts and other artifacts.
with open('model/model.pkl', 'rb') as f:
    model = pickle.load(f)
with open('model/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Define the routes
AIP_HEALTH_ROUTE = os.environ.get('AIP_HEALTH_ROUTE', '/health')
AIP_PREDICT_ROUTE = os.environ.get('AIP_PREDICT_ROUTE', '/predict')
# Define input and output data structures

app = FastAPI("Prod ml deployment app.") # Load the model and scaler

class Predictions(BaseModel):
  """Response model for predictions.
  
  This class defines the response model structure for predictions.
  """
  predictions: List[float]  

@app.get(AIP_HEALTH_ROUTE, status_code=200)
async def health():
  """Health check endpoint.
  
  This endpoint returns a health check response
  
  Returns
  -------
  dict : A dictionary containing the health status
  
  """
  return {'health': 'ok'}

@app.post(AIP_PREDICT_ROUTE,  # <-- Route for prediction requests
          response_model=Predictions,  # <-- Define expected response structure
          response_model_exclude_unset=True)  # <-- Exclude unset fields (only fields with assigned values are included in the response.)
async def predict(request: Request):
  """Prediction endpoint.
  
  This endpoint accepts a POST request with JSON data containing 
  instances/data to predict. It appliesthe loaded model and returns the predictions.
  
  Parameters
  ----------
  request : Request
     The incoming request containing the JSON data.
  
  Returns
  -------
  Predictions
     The predicted values, which include labels and their associated probabilities.
  """
   # input json is the Request and will be read into `instances`
  body = await request.json()
  print(body)
  instances = body["instances"]
  
  instances = [instance[0] for instance in instances]
  # Convert the list of instances to a NumPy array
  instances_array = np.array(instances)

  # Scale the features
  instances_scaled = scaler.transform(instances_array)

  # Make predictions
  predictions = list(model.predict(instances_scaled))
  
  return Predictions(predictions=predictions)

if __name__ == "__main__":
    # Start the FastAPI application
    app.run()

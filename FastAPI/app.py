from fastapi import FastAPI,Path,HTTPException, Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated, Literal, Optional
import pickle
import pandas as pd

#importing the model
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

app = FastAPI()


tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

#pydantic model to  validate the input data
class UserInput(BaseModel):
    age: Annotated[int, Field(...,gt=0, lt=120,description="The age of the patient", example=30)]
    weight: Annotated[float, Field(...,gt=0, description="The weight of the patient in kg", example=70.0)]
    height: Annotated[float, Field(...,gt=0, lt=3, description="The height of the patient in cm", example=175.5)]
    income_lpa: Annotated[float, Field(...,gt=0, description="The income of the patient in USD", example=50000.0)]
    smoker: Annotated[bool, Field(..., description="Whether the patient is a smoker", example=False)]
    city: Annotated[str, Field(..., description="The city where the patient resides", example="New York")]
    occupation: Annotated[Literal["retired","freelancer","student","private_job","government_job","unemployed","business_owner"], Field(..., description="The occupation of the patient", example="Software Engineer")]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / (self.height ** 2)

    @computed_field
    @property
    def lifestyle_risk(self) -> str:
        if self.smoker and self.bmi > 30:
            return "high"
        elif self.smoker or self.bmi > 27:
            return "medium"
        else:
            return "low"
        
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 25:
            return "young"
        elif self.age < 45:
            return "adult"
        elif self.age < 60:
            return "middle_aged"
        else:
            return "senior"
        
    @computed_field
    @property   
    def city_tier(self) -> int:
        if self.city in tier_1_cities:
            return 1
        elif self.city in tier_2_cities:
            return 2
        else:
            return 3
        
@app.post("/predict")
def predict_premium(data: UserInput):
    input_data = data.model_dump()
    input_df = pd.DataFrame([input_data])
    predicted_premium = model.predict(input_df)[0]
    return JSONResponse(status_code=200, content={"predicted_premium": predicted_premium})
from fastapi import FastAPI,Path,HTTPException, Query
import json
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated, Literal


class Patient(BaseModel):
    id: Annotated[str, Field(...,description="The unique identifier for the patient", example="P1001")]
    name: Annotated[str, Field(..., description="The name of the patient", example="John Doe")]
    city: Annotated[str, Field(..., description="The city where the patient resides", example="New York")]
    age: Annotated[int, Field(...,gt=0, lt=120, description="The age of the patient", example=30)]
    gender: Annotated[Literal['male','female'],Field(..., description="The gender of the patient", example="male")]
    height: Annotated[float, Field(...,gt=0, description="The height of the patient in cm", example=175.5)]
    weight: Annotated[float, Field(...,gt=0, description="The weight of the patient in kg", example=70.0)]

    @computed_field
    @property
    def bmi(self) -> float:
        return self.weight / ((self.height / 100) ** 2)

    @computed_field
    @property
    def verdict(self) -> str:
        bmi_value = self.bmi
        if bmi_value < 18.5:
            return "Underweight"
        elif 18.5 <= bmi_value < 24.9:
            return "Normal weight"
        elif 25 <= bmi_value < 29.9:
            return "Overweight"
        else:
            return "Obesity"

def load_patients():
    with open("patients.json", "r") as f:
        data=json.load(f)
    return data

def save_patients(data):
    with open("patients.json", "w") as f:
        json.dump(data, f, indent=4)

patients = load_patients()
app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello, World!"}

@app.get("/about")
def about():
    return {"message": "This is a simple FastAPI application."} 

@app.get("/view")
def view_patients():
    data=load_patients()
    return data

@app.get("/view/{patient_id}")
def view_patient(patient_id: str=Path(..., description="The ID of the patient to retrieve",example="P1001")):
    #load all patients
    data=load_patients()
    #find the patient with the given ID
    for patient in data:
        if patient["patientId"]==patient_id:
            return patient
    raise HTTPException(status_code=404, detail="Patient not found")

@app.get("/sort")
def sort_pateints(sort_by: str=Query(..., description="SOrt on the basis of height,weight,bmi"),order: str=Query('asc',description="Order of sorting: asc or desc")):
    valid_fields = ["height", "weight", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f"Invalid sort field from {valid_fields}")
    if order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid order value. Must be 'asc' or 'desc'.")
    
    data = load_patients()
    sort_order = False if order == "asc" else True
    sorted_data = sorted(data, key=lambda x: x[sort_by], reverse=sort_order)
    return sorted_data


@app.post("/create")
def create_patient(patient: Patient):
    data = load_patients()
    # Check if patient with the same ID already exists
    for existing_patient in data:
        if existing_patient["patientId"] == patient.id:
            raise HTTPException(status_code=400, detail="Patient with this ID already exists.")
    
    # Add the new patient to the list
    new_patient = {
        "patientId": patient.id,
        **patient.model_dump(exclude={"id"})
    }

    save_patients(data + [new_patient])
    return JSONResponse(status_code=201, content={"message": "Patient created successfully."})
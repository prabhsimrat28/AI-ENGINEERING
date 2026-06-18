from pydantic import BaseModel,EmailStr,Field,field_validator,model_validator
from typing import List,Dict,Optional

class Patient(BaseModel):
    email: EmailStr
    name: str 
    age: int 
    weight: float 
    married: bool
    allergies: Optional[List[str]] = None
    contact: Dict[str,str]

    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age>60 and 'emergency' not in model.contact:
            raise ValueError("Emergency contact is required for patients over 60 years old.")
        return model
    

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.email)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact)
    print('inserted')


patient_data = {'name': 'John Doe','email': 'john.doe@hdfc.com', 'age': 90,'weight': 70.5, 'married': True, 'contact': {'email': 'john.doe@example.com', 'phone': '123-456-7890'}}
patient1 = Patient(**patient_data)
insert_patient_data(patient1)


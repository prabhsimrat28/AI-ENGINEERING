from pydantic import BaseModel,EmailStr,Field
from typing import List,Dict,Optional,Annotated
class Patient(BaseModel):
    email: EmailStr
    name: str =Field(max_length=50)
    age: int =Field(gt=0, lt=120,strict=True)
    weight: float = Field(gt=0, lt=200)
    married: Annotated[bool, Field(default=None, description="Marital status of the patient")]
    allergies: Optional[List[str]] = None
    contact: Dict[str,str]

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.email)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact)
    print('inserted')

def update_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.email)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact)
    print('updated')

patient_data = {'name': 'John Doe','email': 'john.doe@example.com', 'age': 30,'weight': 70.5, 'married': True, 'contact': {'email': 'john.doe@example.com', 'phone': '123-456-7890'}}
patient1 = Patient(**patient_data)
insert_patient_data(patient1)
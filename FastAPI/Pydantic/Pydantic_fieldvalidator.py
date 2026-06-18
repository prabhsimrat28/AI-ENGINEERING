from pydantic import BaseModel,EmailStr,Field,field_validator
from typing import List,Dict,Optional
class Patient(BaseModel):
    email: EmailStr
    name: str 
    age: int 
    weight: float 
    married: bool
    allergies: Optional[List[str]] = None
    contact: Dict[str,str]

    @field_validator('email')
    @classmethod
    def email_validator(cls, value):
        valid_domains = ['hdfc.com', 'icici.com']
        domain = value.split('@')[-1]
        if domain not in valid_domains:
            raise ValueError(f"Email domain must be one of {valid_domains}")
        return value
    
    @field_validator('name')
    @classmethod
    def name_validator(cls, value):
        return value.upper()

def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.weight)
    print(patient.email)
    print(patient.married)
    print(patient.allergies)
    print(patient.contact)
    print('inserted')



patient_data = {'name': 'John Doe','email': 'john.doe@hdfc.com', 'age': 30,'weight': 70.5, 'married': True, 'contact': {'email': 'john.doe@example.com', 'phone': '123-456-7890'}}
patient1 = Patient(**patient_data)
insert_patient_data(patient1)

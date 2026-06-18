from pydantic import BaseModel,EmailStr,Field,field_validator,model_validator,computed_field
from typing import List,Dict,Optional

class Patient(BaseModel):
    email: EmailStr
    name: str 
    age: int 
    weight: float 
    married: bool
    allergies: Optional[List[str]] = None
    contact: Dict[str,str]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi=self.weight / (self.age ** 2)
        return bmi


def insert_patient_data(patient: Patient):
    print(patient.bmi)
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


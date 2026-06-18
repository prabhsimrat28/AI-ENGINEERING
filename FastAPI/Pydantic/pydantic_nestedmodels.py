from pydantic import BaseModel,EmailStr,Field,field_validator,model_validator,computed_field
from typing import List,Dict,Optional


class Address(BaseModel):
    city: str
    state: str
    pin_code: str

class Patient(BaseModel):
    gender: str
    name: str 
    age: int 
    address: Address

address_data = {'city': 'New York', 'state': 'NY', 'pin_code': '10001'}
address1 = Address(**address_data)
patient_data = {'name': 'John Doe', 'gender':'male', 'age': 30, 'address': address1}
patient1 = Patient(**patient_data)
print(patient1)
print(patient1.address.city)
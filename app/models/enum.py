from enum import Enum 

class UserRole(str,Enum):
    customer="customer"
    admin="admin"
    seller="seller"

class OtpStatus(str,Enum):
    Pending="Pending"
    Verified="Verified"
    Expired="Expired"
    Success="Success"
    Already_Verified="Already_Verified"
    Invalid="Invalid"





from pydantic import BaseModel
from typing import List, Dict

class Product(BaseModel):
    product_name: str
    features: List[Dict[str, str]]
    benefits: str
    use_cases: str

class CompanyData(BaseModel):
    company_name: str
    products: List[Product]

class ProductStore:
    def __init__(self):
        self.company_data = {}

    def add_company_data(self, company_name: str, data: CompanyData):
        self.company_data[company_name] = data

    def get_company_data(self, company_name: str) -> CompanyData:
        return self.company_data.get(company_name, None)
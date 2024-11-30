import json
from typing import Dict, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, ValidationError
from data_extractions import extract_entities_from_document
from data_storage import ProductStore, CompanyData, Product

# Initialize FastAPI app and storage
app = FastAPI()
product_store = ProductStore()

# Pydantic models for API request validation
class FeatureRequest(BaseModel):
    feature_name: str
    feature_description: str

class ProductRequest(BaseModel):
    product_name: str
    features: List[FeatureRequest]
    benefits: str
    use_cases: str


class CompanyRequest(BaseModel):
    company_name: str
    products: List[ProductRequest]


@app.post("/add-company/")
async def add_company_data(company: CompanyRequest):
    """
    Adds company and product information to the storage.
    """
    try:
        # Convert incoming data into the structured format
        company_data = CompanyData(
            company_name=company.company_name,
            products=[
                Product(
                    product_name=product.product_name,
                    features=[{"name": feature.feature_name, "description": feature.feature_description} for feature in product.features],
                    benefits=product.benefits,
                    use_cases=product.use_cases
                )
                for product in company.products
            ]
        )
        product_store.add_company_data(company.company_name, company_data)
        return {"message": "Company data added successfully"}
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/get-company/{company_name}")
async def get_company_data(company_name: str):
    """
    Retrieves company data by company name.
    """
    company_data = product_store.get_company_data(company_name)
    if not company_data:
        raise HTTPException(status_code=404, detail="Company not found")
    return company_data.dict()


@app.post("/extract-and-add-company/")
async def extract_and_add_company_data(text: str):
   """
   Extracts company and product data from an unstructured document and adds it to storage.
   """
   # Extract structured data from the document text using the LLM-based extraction function
   extracted  = extract_entities_from_document(text)
   extracted_data = json.dumps(extracted, indent=4)
  

     # Convert extracted data into the structured format
   company_name = extracted_data["company_name"]
   products = extracted_data["products"]
  
   # Prepare the data as CompanyData and add it to storage
   company_data = CompanyData(company_name=company_name, products=products)
   product_store.add_company_data(company_name, company_data)
  
   return {"message": f"Company data for {company_name} added successfully."}

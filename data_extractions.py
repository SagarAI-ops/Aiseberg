import json
from langchain.llms import OpenAI as LangChainOpenAI
from dotenv import load_dotenv
import os

load_dotenv()  # Loads environment variables from .env file

# Get the OpenAI API key from the environment variable
api_key = "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"
llm = LangChainOpenAI(openai_api_key=api_key, model="gpt-3.5-turbo-instruct", temperature=0.7)

# Detailed prompt template for extracting structured data
prompt_template = """
Extract the following information from the document and structure it in JSON format:

- company_name: The name of the company.
- products: A list of products offered by the company, where each product includes:
  - product_name: The name of the product.
  - features: A list of features of the product, where each feature includes:
    - feature_name: The name of the feature.
    - feature_description: A description of what the feature does.
  - benefits: A list of benefits of using the product.
  - use_cases: A list of common use cases for the product.

Document: {document}

Please output the results in structured JSON format.

Example Output:
{
    "company_name": "TechCorp",
    "products": [
        {
            "product_name": "AI Assistant",
            "features": [
                {
                    "feature_name": "Natural Language Processing",
                    "feature_description": "Handles and understands human language"
                },
                {
                    "feature_name": "Real-Time Data Processing",
                    "feature_description": "Processes data instantly as it arrives"
                }
            ],
            "benefits": [
                "Saves time by automating tasks",
                "Improves decision-making through data insights"
            ],
            "use_cases": [
                "Customer Support",
                "Data Analysis"
            ]
        }
    ]
}
"""

# Create a PromptTemplate using the prompt
from langchain.prompts import PromptTemplate
prompt = PromptTemplate(input_variables=["document"], template=prompt_template)

from langchain.chains import LLMChain
from langchain.output_parsers.json import SimpleJsonOutputParser

# Create an LLMChain with the LangChain LLM
chain = prompt | llm | SimpleJsonOutputParser()

def extract_entities_from_document(document: str) -> dict:
    """
    Extracts company and product information from the document and returns it as a structured dictionary.
    """
    try:
        # Use the `invoke` method with the document parameter
        response = chain.invoke({"document": document})

        # Attempt to parse the response into JSON
        try:
            structured_data = json.loads(response)
            return structured_data
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON: {e}")
            raise ValueError("The response is not valid JSON")

    except Exception as e:
        print(f"An error occurred while extracting entities: {e}")
        raise


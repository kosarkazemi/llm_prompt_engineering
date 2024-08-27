# Product-Extra
Test ML Software Engineer for Akeneo

## Product Extraction API Documentation

Welcome to the Product Extraction API! This API provides a service to extract specified fields from a given list of products using a Language Model. It utilizes Flask, a popular Python web framework, to handle incoming HTTP requests.

### Introduction

This API allows you to extract specific fields from a list of products using a language model. Follow the instructions below to set up the environment using Docker and Poetry.

### Getting Started

#### Installation Instructions

1. **Install Docker:**
   Ensure you have Docker installed on your system. Docker is a containerization platform that simplifies deployment and dependencies.
   - [Docker Installation Guide](https://docs.docker.com/get-docker/)

2. **Clone the Repository:**
   Clone the repository containing the API code to your local machine.
   ```bash
   git clone https://github.com/kosarkazemi/Product-Extra.git
   cd Product-Extra
   ```

3. **Install Poetry:**
   Poetry is a tool for dependency management and packaging in Python. It allows you to manage project dependencies and create a virtual environment.
   - [Poetry Installation Guide](https://python-poetry.org/docs/)

4. **Install Dependencies:**
   Use Poetry to install the project dependencies.
   ```bash
   poetry install
   ```

5. **Build and Run the Docker Image:**
   Build the Docker image from the provided Dockerfile and run the API inside a Docker container.
   ```bash
   docker build -t product_extraction_api .
   docker run -p 5001:5000 product_extraction_api
   ```
   The API will now be running and accessible at `http://0.0.0.0:5001`.

### API Endpoints

1. **`GET /`**

   This endpoint provides a welcome message to users accessing the root URL of the API.
   
   **Request:**
   ```plaintext
   GET /
   ```

   **Response:**
   ```json
   {
     "message": "Welcome to the product extraction API!"
   }
   ```

2. **`POST /extract_fields`**

   This endpoint extracts specified fields from a list of products using a language model.

   **Request:**
   - Method: `POST`
   - Body:
     ```json
     {
       "products": [
         {
           "Titre": "Baignoire d'angle Geberit Bastia: 142x142cm",
           "Description": "BAIG ANGL BASTIA 142X142",
           "LIBL_LIBELLE": "Baignoire d'angle Geberit Bastia avec pieds: 142x142cm",
           "Argumentaire Produit": "Poignes en option",
           "fields_to_extract": ["EF000040"]
         }
       ],
       "model": "LLaMA"
     }
     ```

   **Response:**
   ```json
   [
     {
       "product": 
         {
           "Titre": "Baignoire d'angle Geberit Bastia: 142x142cm",
           "Description": "BAIG ANGL BASTIA 142X142",
           "LIBL_LIBELLE": "Baignoire d'angle Geberit Bastia avec pieds: 142x142cm",
           "Argumentaire Produit": "Poignes en option",
           "fields_to_extract": ["EF000040"]
         },
       "fields": [
         {
           "field_name": "EF000040",
           "field_value": "Answer LLaMA"
         }
       ]
     }
   ]
   ```

### Usage

- **Access the API:**
  Use a tool like Postman or send HTTP requests programmatically to the specified endpoints.

- **Run the client.py Script:**
  Execute the client.py script by running it with Python. This script will send a POST request to the API, extract specified fields from the provided data, and display the response. Use the following command:
  ```bash
  python client.py
  ```
  This script will display the payload being sent, the response status code, and the response JSON, allowing you to verify the interaction with the API and the extracted fields.

## Next Steps

1. **Diverse Examples for Better Understanding:**
   Include a variety of examples from different fields to improve the model's comprehension and extraction accuracy.

2. **Tailored Prompts for Each Product Aspect:**
   Create customized prompts specific to each product's attributes to enhance field extraction precision.

Let's proceed with these steps to enhance the API's performance in extracting fields from product descriptions.
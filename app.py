import logging
from flask import Flask, request, jsonify
from src.LanguageModel import LanguageModel
from src.prompting import make_prompt
from src.utils import parse_llm_output
import json

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def extract_fields(products, model):
    llm_model = LanguageModel.create_instance(model)
    products_extractions = []

    for product in products:
        field_names = product.get("fields_to_extract", [])
        product_fields = []

        for field_name in field_names:
            logger.info(f'Extracting field {field_name} for product: {product.get("Titre")}')

            system_prompt, user_message = make_prompt(product, field_name, model)
            final_prompt = llm_model.format_prompt(system_prompt, user_message)
            model_output = llm_model.call_model(final_prompt)
            field_value = parse_llm_output(model_output)
            product_fields.append({"field_name": field_name, "field_value": field_value})

        products_extractions.append({"product": product, "fields": product_fields})

    return products_extractions

@app.route('/home')
def index():
    logger.info('Received request at index.')
    return 'Welcome to the product extraction API!'

@app.route('/extract_fields', methods=['POST'])
def extract_fields_endpoint():
    payload_str = request.get_json()
    payload = json.loads(payload_str)

    if not payload or not payload.get('model'):
        logger.error('Invalid payload. Model not provided.')
        return jsonify({'error': 'Invalid payload. Model not provided.'}), 400

    products = payload.get('products', [])
    model = payload.get('model')

    logger.info('Received extraction request for model: %s', model)
    products_extractions = extract_fields(products, model)

    return jsonify(products_extractions)


if __name__ == '__main__':
    logger.info('Starting the application.')
    app.run(host='0.0.0.0', port=5000, debug=True)

import json

# Paths to input data files
FIELDS_PATH = "materials/fields.json"
EXAMPLES_PATH = "materials/examples.json"

# System prompt for the user
SYSTEM_PROMPT = "I will provide you with several examples that extract specific attributes from product descriptions. " \
                "Your task is to identify and extract the same attribute for a given product. " \
                "The attributes may relate to the drying type, command options, or other product features. " \
                "Carefully review the provided examples and use the information to identify the relevant attribute for the next product."

# Maximum character limits for different LLM models
MAX_CHARS = {"LLaMA": 4096 - 35 - len(SYSTEM_PROMPT), "CameLLM": 2048 - 40 - len(SYSTEM_PROMPT)}

# Read the fields information from JSON
with open(FIELDS_PATH, 'r') as json_file:
    FIELDS_JSON = json.load(json_file)

# Create a dictionary for fields information
FIELDS_DICT = {item["name"]: item for item in FIELDS_JSON}

# Read the examples from JSON
with open(EXAMPLES_PATH, 'r') as json_file:
    EXAMPLES_DICT = json.load(json_file)


def generate_question(product_info, field_type, field_label, options=None):
    """
    Generate a question based on the product information, field type, and field label.

    Args:
        product_info (dict): Product information dictionary.
        field_type (str): Field type (e.g., 'select', 'boolean', 'number').
        field_label (str): Field label.
        options (list, optional): List of options for 'select' field type.

    Returns:
        str: Generated question string.
    """
    Q_str = f"Given Product Information:\n" \
            f"- Titre: {product_info.get('Titre', '')}\n" \
            f"- Description: {product_info.get('Description', '')}\n" \
            f"- LIBL_LIBELLE: {product_info.get('LIBL_LIBELLE', '')}\n" \
            f"- Argumentaire Produit: {product_info.get('Argumentaire Produit', '')}\n"

    if field_type == "select":
        options_str = ", ".join(options)
        Q_str = f"Q: What is the {field_label} of this product? (options are: {options_str})\n" + Q_str
    elif field_type == "boolean":
        Q_str = f"Q: Is the product {field_label}?\n" + Q_str
    elif field_type == "number":
        Q_str = f"Q: What is the {field_label} of the product?\n" + Q_str

    return Q_str + "\n"


def generate_answer(product_info, field_type, field_label):
    """
    Generate an answer based on the product information, field type, and field label.

    Args:
        product_info (dict): Product information dictionary.
        field_type (str): Field type (e.g., 'select', 'boolean', 'number').
        field_label (str): Field label.

    Returns:
        str: Generated answer string.
    """
    A_str = f"A: Given the title {product_info.get('Titre', '')},\n" \
            f"   the description {product_info.get('Description', '')},\n" \
            f"   the label {product_info.get('LIBL_LIBELLE', '')} \n" \
            f"   and the product argument {product_info.get('Argumentaire Produit', '')}.\n" \
            f"   It's possible to conclude "
    
    if not product_info.get('field_value'):
        # if the field_value is null
        A_str = A_str + f"The {field_label} of the product is unkown.\n"
    else:
        if field_type == "select":
            A_str = A_str + f"The {field_label} of the product is {product_info.get('field_value', '')}.\n"
        elif field_type == "boolean":
            if product_info.get('field_value', 'non').lower() == 'non':
                A_str = A_str + f"No, the product is not {field_label}.\n"
            else:
                A_str = A_str + f"Yes, the product is {field_label}.\n"
        elif field_type == "number":
            A_str = A_str + f"The {field_label} of the product is {product_info.get('field_value', '')}.\n"

    return A_str


def make_prompt(product_input, field_name, llm_model_name):
    """
    Generate a complete prompt with questions and answers based on the product information and field name.

    Args:
        product_input (dict): Product information dictionary.
        field_name (str): Field name to extract.
        llm_model_name (str): LLM model name.

    Returns:
        tuple: System prompt and the complete prompt with questions and answers.
    """
    field_info = FIELDS_DICT.get(field_name)
    field_type = field_info.get("type")
    field_label = field_info.get("label")
    field_options = field_info.get("options", None)

    Q_A_str = generate_question(product_input, field_type, field_label, options=field_options)
    similar_examples = [example for example in EXAMPLES_DICT if example["field_name"] == field_name]

    for new_example in similar_examples:
        new_example_question = generate_question(new_example, field_type, field_label, options=field_options)
        new_example_answer = generate_answer(new_example, field_type, field_label)

        if len(Q_A_str) + len(new_example_question) + len(new_example_answer) < MAX_CHARS.get(llm_model_name):
            Q_A_str = new_example_question + new_example_answer + Q_A_str + "\n\n"
        else:
            break

    return SYSTEM_PROMPT, Q_A_str


if __name__ == '__main__':
    # Example product information, field name, and LLM model name
    product_input_example = {
        "Titre": "Baignoire d'angle Geberit Bastia: 142x142cm",
        "Description": "BAIG ANGL BASTIA 142X142",
        "LIBL_LIBELLE": "Baignoire d'angle Geberit Bastia with feet: 142x142cm",
        "Argumentaire Produit": "Handles as an option",
    }
    field_name_example = "EF000040"  # Example field name
    llm_model_name_example = "LLaMA"  # Example LLM model name

    # Generate the prompt and print it
    prompt_example = make_prompt(product_input_example, field_name_example, llm_model_name_example)
    print(prompt_example)

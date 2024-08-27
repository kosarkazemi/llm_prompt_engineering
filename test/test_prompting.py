import unittest
from src.prompting import generate_question, generate_answer, make_prompt

class TestPrompting(unittest.TestCase):

    def test_generate_question(self):
        """
        Test the generate_question function.
        """
        product_info = {
            "Titre": "Sample Product Title",
            "Description": "This is a description of the sample product.",
            "LIBL_LIBELLE": "Sample product by XYZ Inc.",
            "Argumentaire Produit": "This is an argument for the product.",
        }
        field_type = "select"
        field_label = "Field Label"
        options = ["Option1", "Option2"]

        question = generate_question(product_info, field_type, field_label, options)
        self.assertTrue("What is the Field Label of this product?" in question)
        self.assertTrue("Option1, Option2" in question)

    def test_generate_answer(self):
        """
        Test the generate_answer function.
        """
        product_info = {
            "Titre": "Sample Product Title",
            "Description": "This is a description of the sample product.",
            "LIBL_LIBELLE": "Sample product by XYZ Inc.",
            "Argumentaire Produit": "This is an argument for the product.",
            "field_value": "Option1"
        }
        field_type = "select"
        field_label = "Field Label"

        answer = generate_answer(product_info, field_type, field_label)
        self.assertTrue("The Field Label of the product is Option1." in answer)

    def test_make_prompt(self):
        """
        Test the make_prompt function.
        """
        product_info = {
            "Titre": "Baignoire d'angle Geberit Bastia: 142x142cm",
            "Description": "BAIG ANGL BASTIA 142X142",
            "LIBL_LIBELLE": "Baignoire d'angle Geberit Bastia avec pieds: 142x142cm",
            "Argumentaire Produit": "Poignes en option"
        }
        field_name = "EF000040"
        llm_model_name = "LLaMA"

        prompt = make_prompt(product_info, field_name, llm_model_name)

        self.assertTrue("What is the hauteur (cm) of the product?" in prompt)
        self.assertTrue("Given the title Série 500 ColdSense" in prompt)

if __name__ == '__main__':
    unittest.main()

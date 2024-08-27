import unittest
from app import extract_fields

class TestExtractFields(unittest.TestCase):
    def setUp(self):
        # Mock input payload and expected output
        self.payload = {
            'products': [ 
                {
                    "Titre": "Baignoire d'angle Geberit Bastia: 142x142cm",
                    "Description": "BAIG ANGL BASTIA 142X142",
                    "LIBL_LIBELLE": "Baignoire d'angle Geberit Bastia avec pieds: 142x142cm",
                    "Argumentaire Produit": "Poignes en option",
                    "fields_to_extract": ["EF000040"]
                },
            ],
            'model': 'LLaMA'
        }

        self.expected_output = [
            {
                'product': self.payload['products'][0],
                'fields': [
                    {
                        'field_name': 'EF000040',
                        'field_value': ' Answer LLaMA'
                    }
                ]
            }
        ]

    def test_extract_fields(self):
        # Call the function and compare the output
        output = extract_fields(self.payload['products'], self.payload['model'])
        self.assertEqual(output, self.expected_output)

if __name__ == '__main__':
    unittest.main()

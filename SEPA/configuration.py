import os
import json

# Represents the secrets.json
class Configuration:

    quarter = None
    input_filename = None
    output_names_file = None

    path_to_input_folder = None
    path_to_output_folder = None
    sheet_name = None

    iban = None
    bic = None
    iban_name = None
    iban_message = None

    def __init__(self, quarter, filename):
        self.quarter = quarter
        self.input_filename = filename

        secrets_dict = self.load_secrets_json()
        self.sheet_name = secrets_dict.get("SHEET_NAME")
        self.output_names_file = secrets_dict.get("OUTPUT_NAMES_FILE")
        self.path_to_input_folder = secrets_dict.get("PATH_TO_INPUT_FOLDER")
        self.path_to_output_folder = secrets_dict.get("PATH_TO_OUTPUT_FOLDER")
        self.iban = secrets_dict.get("IBAN")
        self.bic = secrets_dict.get("BIC")
        self.iban_name = secrets_dict.get("IBAN_NAME")
        self.iban_message = secrets_dict.get("IBAN_MESSAGE")


    def load_secrets_json(self) -> dict:
        secrets_file = os.path.join('secrets.json').encode("utf-8")
        try:
            with open(secrets_file, mode='r', encoding='utf-8') as f:
                return json.loads(f.read())
        except FileNotFoundError:
            return {}


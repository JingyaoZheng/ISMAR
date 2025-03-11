import pandas as pd
import random
import os
from dotenv import load_dotenv
from tqdm import tqdm

def extract_lines(source_file: str, target_file: str, num_lines=151):
    """
    Extracts a specific number of lines from a text file and saves them to another text file.
    
    Args:
        source_file (str): Path to the source text file from which lines are to be extracted.
        target_file (str): Path to the target text file where the extracted lines will be saved.
        num_lines (int): Number of lines to extract. Default is 151.
    """
    
    try:
        with open(source_file, 'r') as file:
            lines = file.readlines()

        #Data Cleaning 
        if any('<s>' in line or '</s>' in line for line in lines):
            lines = [line.replace('<s>', '').replace('</s>', '').strip() for line in lines]
        else:
            lines = [line.strip() for line in lines]


        if len(lines) < num_lines:
            raise ValueError("The source file does not contain enough lines.")

        random_lines = random.sample(lines, num_lines)

        new_data = pd.DataFrame(random_lines, columns=['Content'])

        if os.path.exists(target_file):
            existing_data = pd.read_excel(target_file)
            updated_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            updated_data = new_data

        updated_data.to_excel(target_file, index=False)

        print(f"Successfully extracted {num_lines} lines from '{source_file}' to '{target_file}'.")

    except FileNotFoundError:
        print(f"Error: The file '{source_file}' does not exist.")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

def translate_column(input_file, column_name='Content', target_language='ZH'):
    
    load_dotenv()
    DL_api_key = os.getenv('DEEPL_API_KEY')
    if not DL_api_key:
        raise ValueError("Please set your DeepL API key in the .env file.")
    data = pd.read_excel(input_file)

    if column_name not in data.columns:
        raise ValueError(f"Column '{column_name}' does not exist in the input file.")
    
    def translate_text(text, target_language):
        import requests
        url = "https://api-free.deepl.com/v2/translate"
        params = {
            'auth_key': DL_api_key,
            'text': text,
            'target_lang': target_language
        }
        response = requests.post(url, data=params)
        if response.status_code == 200:
            translated_text = response.json()['translations'][0]['text']
            return translated_text
        else:
            print(f"Failed to translate text. Status Code: {response.status_code}, Response: {response.text}")
            return text
    
    new_column = "Translated Content"
    tqdm.pandas(desc="Translating text...")
    data[new_column] = data[column_name].progress_apply(lambda text: translate_text(text, target_language))
    data.to_excel(input_file, index=False)



if __name__ == "__main__":
    extract_lines('Data/mobile_train.txt', 'data.xlsx', 200)
    # extract_lines('email_dev.txt', 'data.xlsx', 23)
    # translate_column('data.xlsx', 'Content', 'ZH')
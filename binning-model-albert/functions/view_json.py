import json


def load_and_check_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            # Check the content of the JSON file
            # You can add your own logic here
            if data:
                total = len(data)
                number_of_null_values_for_category_code = 0
                number_of_null_values_for_text = 0
                both = 0
                for i in range(len(data)):
                    print(json.dumps(data[i]['CategoryV7'], indent=4))
                    if (data[i]['CategoryV7'] == 'null' or data[i]['CategoryV7'] == None):
                        number_of_null_values_for_category_code += 1
                        if (data[i]['subject_content_text'] == "null" or data[i]['subject_content_text'] == None):
                            both += 1
                    if (data[i]['subject_content_text'] == "null" or data[i]['subject_content_text'] == None):
                        number_of_null_values_for_text += 1
                print("Total: ", total)
                print("Null Catrgory Code: ",
                      number_of_null_values_for_category_code)
                print("Null Text: ", number_of_null_values_for_text)
                print("Both Text: ", both)
            else:
                print("JSON file is empty.")
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Invalid JSON format.")


# Example usage
load_and_check_json(
    'data/no_pii_grievance_v2/no_pii_grievance_v2.json')

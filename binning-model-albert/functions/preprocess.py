import json
import csv
import os
import csv
import pandas
import pandas as pd
import re


def load_json(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
            if data:
                return data
            else:
                print("JSON file is empty.")
    except FileNotFoundError:
        print("File not found.")
    except json.JSONDecodeError:
        print("Invalid JSON format.")


def clean_and_extract_json(data):
    data_array = []
    for i in range(len(data)):
        if (data[i]['CategoryV7'] == 'null' or data[i]['CategoryV7'] == None):
            continue
        if (data[i]['subject_content_text'] == "null" or data[i]['subject_content_text'] == None):
            continue
        required_data = {
            "subject_content_text": data[i]['subject_content_text'],
            "category_code": data[i]['CategoryV7']['$numberLong']
        }
        data_array.append(required_data)

    return data_array, len(data_array)


def save_data_to_json(data, file_path):
    try:
        with open(file_path, "w") as json_file:
            json.dump(data, json_file)
        print(f"Data Cleaned and saved to {file_path}")
    except FileNotFoundError:
        print(f"No Such Directory Exists: {file_path}")


def read_csv_file(file_path):
    try:
        dataframe = pd.read_csv(file_path, encoding="utf-8")
        return dataframe
    except FileNotFoundError:
        print("File not found.")


def create_json_from_df(df):
    # required_data = df.loc[:, ["Code", "Description"]]
    required_data = df
    # Code	Description	OrgCode	Parent	Stage	MonitoringCode

    i = 0
    required_json = {}
    final_json = []
    for index, row in required_data.iterrows():
        row = list(row)
        if row[1] == "#":
            continue

        required_json[f"{row[0]}"] = {
            "code": row[0],
            "category_name": row[1],
            "label": make_label_from_category_names(row[1]),
            "parent_code": row[3]
        }
    return required_json


def make_label_from_category_names(string):
    converted_string = string.lower()

    replaced_string = re.sub(r'/', ' ', converted_string)
    replaced_string = re.sub(r'\s+', '-', replaced_string)
    replaced_string = replaced_string.replace(",", '-')
    replaced_string = replaced_string.replace("(", '-')
    replaced_string = replaced_string.replace(")", '')
    replaced_string = replaced_string.replace("--", '-')
    replaced_string = replaced_string.replace("&", 'and')
    replaced_string = re.sub(r'-$', '', replaced_string)

    return replaced_string


def join_data(grevience_data, category_code_data):
    result_data = []
    result_labels = []
    for item in grevience_data:
        category_code_item = category_code_data[item["category_code"]]
        # If the category has a parent assign that code
        if "parent_code" in category_code_item and category_code_item['parent_code'] in category_code_data and category_code_item['parent_code'] != "null" and category_code_item['parent_code'] != "":
            category_code_item = category_code_data[category_code_item['parent_code']]

        combined_data = {
            "subject_content_text": remove_newlines(item['subject_content_text']),
            "code": category_code_item["code"],
            "category_name": category_code_item['category_name'],
            "label": category_code_item['label']
        }
        result_labels.append(category_code_item['label'])
        result_data.append(combined_data)
    return result_data, list(set(result_labels))


def save_data_to_csv(data, file_path):
    try:
        # columns = ['subject_content_text', "code", "category_name", "label"]
        # with open(file_path, "w", encoding="utf-8") as f:
        #     f.write(f"subject_content_text,code,category_name, label\n")

        #     for item in data:
        #         f.write(
        #             f"{item['subject_content_text']},{item['code']},{item['category_name']}, {item['label']}\n")
        # print(f"Data Cleaned and saved to {file_path}")
        df = pd.DataFrame(data)
        df.to_csv(file_path, encoding="utf-8")
        print(f"Data Cleaned and saved to {file_path}")

    except FileNotFoundError:
        print(f"No Such Directory Exists: {file_path}")


def remove_newlines(text):
    text = text.replace("\n", ' ')
    return text.replace("\r", ' ')


def save_labels(labels, file_path):
    with open(file_path, "w") as f:
        for label in labels:
            f.write(f"{label}\n")


# Process JSON Dump
data_path_json = 'data/no_pii_grievance_v2/no_pii_grievance_v2.json'
json_file_name = data_path_json.split("/")[-1][:-5]
print(f"Processing File: {json_file_name}")
data = load_json(data_path_json)
data, number_of_usable_data = clean_and_extract_json(data)

print("Number of data points: ", number_of_usable_data)
# save_data_to_json(data, f'data/cleaned/{json_file_name}_cleaned.json')


# Process CSV Dump
data_path_csv = 'data\CategoryCode_Mapping_v2_utf8.csv'
csv_file_name = data_path_csv.split("/")[-1][:-4]
df = read_csv_file(data_path_csv)
json_data = create_json_from_df(df)
final_data, final_labels = join_data(data, json_data)
save_data_to_json(final_data, f"data/cleaned/cleaned_and_preprocessed.json")
save_labels(final_labels, "data/cleaned/labels.txt")
print(len(final_labels))
save_data_to_csv(final_data, f"data/cleaned/cleaned_and_preprocessed.csv")

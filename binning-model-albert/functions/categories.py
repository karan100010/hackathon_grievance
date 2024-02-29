import pandas as pd
import json


def read_csv_file(file_path):
    try:
        dataframe = pd.read_csv(file_path, encoding="utf-8")
        return dataframe
    except FileNotFoundError:
        print("File not found.")


def create_json_from_df(df):
    # required_data = df.loc[:, ["Code", "Description", "OrgCode","Parent","Stage", "MonitoringCode"]]
    required_data = df
    i = 0
    required_json = {}
    final_json = []
    for index, row in required_data.iterrows():
        row = list(row)
        # Code	Description	OrgCode	Parent	Stage	MonitoringCode

        required_json[f"{row[0]}"] = {
            "code": row[0],
            "category_name": row[1],
            "description": row[2],
            "parent_code": row[3],
            "stage": row[4],
            "monitering_code": row[5]
        }
    return required_json


def save_data_to_json(data, file_path):
    try:
        with open(file_path, "w") as json_file:
            json.dump(data, json_file)
        print(f"Data Cleaned and saved to {file_path}")
    except FileNotFoundError:
        print(f"No Such Directory Exists: {file_path}")


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


df = read_csv_file("data\CategoryCode_Mapping_v2_utf8.csv")
json_from_csv = load_json("data\CategoryCode_Mapping_v2_utf8.json")


def create_category_parent_mapping(data):
    catrgory_parent_mapping = {}
    i = 0
    for key, value in data.items():
        cat = value
        if i % 5000 == 0:
            save_data_to_json(catrgory_parent_mapping,
                              "E:\hackathon\data\cleaned\parent_category_mapping.json")

        if cat["parent_code"] != 'nan' and cat["parent_code"] != "" and cat["parent_code"] != None and cat["parent_code"] != "null":
            parent_code = str(int(cat["parent_code"]))
            if parent_code in catrgory_parent_mapping:

                new_child = {
                    "name": cat["category_name"],
                    "code": str(cat["code"])
                }

                catrgory_parent_mapping[parent_code]["children"].append(
                    new_child)
            else:

                catrgory_parent_mapping[parent_code] = {}
                catrgory_parent_mapping[parent_code]["children"] = []
                catrgory_parent_mapping[parent_code]["children"].append({
                    "name": cat["description"],
                    "code": str(cat["code"])
                })

        else:

            if cat['code'] not in catrgory_parent_mapping:
                # orphan category not in the parents

                catrgory_parent_mapping[f"{cat['code']}"] = {
                    "children": []
                }
        i += 1
    return catrgory_parent_mapping


def replce_parent_codes_with_category_names(category_parent_mapping, category_data):
    final_data = {}
    for parent_category_code, value in category_parent_mapping.items():
        if parent_category_code in category_data:
            cat = category_data[parent_category_code]
            final_data[cat["category_name"]] = value
            final_data[cat["category_name"]]["code"] = parent_category_code
        else:
            final_data["others"] = value
            final_data["others"]["code"] = parent_category_code
    return final_data


catrgory_parent_mapping = create_category_parent_mapping(json_from_csv)
catrgory_parent_mapping = replce_parent_codes_with_category_names(
    catrgory_parent_mapping, json_from_csv)

save_data_to_json(catrgory_parent_mapping,
                  "E:\hackathon\data\cleaned\parent_category_mapping.json")

import pandas as pd

# Load and clean data
data = pd.read_csv('smartphones.csv')
data = data.drop_duplicates()

# Standardize brand names to lowercase
data['brand_name'] = data['brand_name'].str.lower()

# Get unique brand names
brand_names = data['brand_name'].drop_duplicates().reset_index(drop=True)
print("Available brands:\n")
for brand in brand_names:
    print("-", brand)

# Function to get a valid brand name from user
def get_valid_brand(prompt):
    while True:
        brand = input(prompt).lower()
        if brand in brand_names.values:
            return brand
        print("Brand not found. Please check your input.")

# Function to get a valid model index from user
def get_model_index(models, prompt):
    while True:
        try:
            index = int(input(prompt))
            if 0 <= index < len(models):
                return index
            else:
                print("Invalid index. Please select from the available models.")
        except ValueError:
            print("Please enter a valid number.")

# Function to show available models for a brand
def display_models(model_data):
    print("Available models:")
    for i, model in enumerate(model_data['model']):
        print(f"{i}: {model}")

# Get first brand and model
first_phone_name = get_valid_brand("Enter the first company name: ")
phone1_model_data = data[data['brand_name'] == first_phone_name].reset_index(drop=True)
display_models(phone1_model_data)
index_of_model1 = get_model_index(phone1_model_data['model'], "Enter the index of the model 1: ")
phone_specs1 = phone1_model_data.iloc[[index_of_model1]]

# Get second brand and model
sec_phone_name = get_valid_brand("Enter the second company name: ")
phone2_model_data = data[data['brand_name'] == sec_phone_name].reset_index(drop=True)
display_models(phone2_model_data)
index_of_model2 = get_model_index(phone2_model_data['model'], "Enter the index of the model 2: ")
phone_specs2 = phone2_model_data.iloc[[index_of_model2]]

# Display specs
print("\nSpecifications for Model 1:")
for col in phone_specs1.columns:
    print(f"{col} : {phone_specs1.iloc[0][col]}")

print("\nSpecifications for Model 2:")
for col in phone_specs2.columns:
    print(f"{col} : {phone_specs2.iloc[0][col]}")

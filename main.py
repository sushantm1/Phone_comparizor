import pandas as pd
import numpy as np

# Load and clean data
data = pd.read_csv('smartphones.csv')
data = data.drop_duplicates()

# Standardize brand names to lowercase
data['brand_name'] = data['brand_name'].str.lower()

# Get unique brand names
brand_names = data['brand_name'].drop_duplicates().reset_index(drop=True)
print("Available brands:\n", brand_names)

# Input first brand from user
first_phone_name = input("Enter the first company name: ").lower()

# Filter models by brand
if first_phone_name in brand_names.values:
    # print(data)
    phone1_model_data = data[data['brand_name'] == first_phone_name].reset_index(drop=True)
    print("Available models from", first_phone_name, ":\n", phone1_model_data['model'])
else:
    print("Brand not found. Please check your input.")

index_of_model1 = int(input("Enter the index of the model 1 : "))

sec_phone_name = input("Enter the second company name: ").lower()

if sec_phone_name in brand_names.values:
    # print(data)
    phone2_model_data = data[data['brand_name'] == sec_phone_name].reset_index(drop=True)
    print("Available models from", sec_phone_name, ":\n", phone2_model_data['model'])
else:
    print("Brand not found. Please check your input.")


index_of_model2 = int(input("Enter the index of the model 2 : "))

phone_sepcs1=data.loc[(data['brand_name']==first_phone_name) & (data['model'] == phone1_model_data['model'][index_of_model1])].reset_index(drop=True)
phone_sepcs2=data.loc[(data['brand_name']==sec_phone_name) & (data['model'] == phone2_model_data['model'][index_of_model2])].reset_index(drop=True)

# print(phone_sepcs1['model'].to_string(index=False, header=False))
# print(phone_sepcs2['model'].to_string(index=False, header=False))

for i in phone_sepcs1:
    print(i, " : ", phone_sepcs1[i][0])

print("\n\n")
for i in phone_sepcs2:
    print(i, " : ", phone_sepcs2[i][0])

# def to():
#     return phone1_model_data, phone2_model_data




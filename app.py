import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import math

from google import genai
client = genai.Client(api_key="")
from main import phone_sepcs1, phone_sepcs2

phone1=phone_sepcs1['model'].to_string(index=False,header=False)
phone2=phone_sepcs2['model'].to_string(index=False,header=False)

# Input text to generate a review
# input_text = (f"iphone 16 vs samsung s23, which is best.\n")
input_text = (
    f"Write a detailed comparison between the {phone1} and {phone2} behave as like i made this AI comparision model and make it concise and short and remove the conversation line, just give me the comparison.\n"
)
print('\n')
# Generate text
print("Generated Review:")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=input_text,
)
print(response.text)



column1 = phone_sepcs1['model'].to_string(index=False, header=False)
column2 = phone_sepcs2['model'].to_string(index=False, header=False)

category = ['Model 1', 'Model 2']

# Convert extracted values to numeric types and replace NaN with 0
price1 = int(float(pd.to_numeric(phone_sepcs1['price'].to_string(index=False, header=False).strip(), errors='coerce') or 0))
price2 = int(float(pd.to_numeric(phone_sepcs2['price'].to_string(index=False, header=False).strip(), errors='coerce') or 0))

num_cores1 = int(float(pd.to_numeric(phone_sepcs1['num_cores'].to_string(index=False, header=False).strip(), errors='coerce') or 0))
num_cores2 = int(float(pd.to_numeric(phone_sepcs2['num_cores'].to_string(index=False, header=False).strip(), errors='coerce') or 0))

battery1 = int(pd.to_numeric(phone_sepcs1['battery_capacity'].to_string(index=False, header=False).strip(), errors='coerce') or 0)
battery2 = int(pd.to_numeric(phone_sepcs2['battery_capacity'].to_string(index=False, header=False).strip(), errors='coerce') or 0)

ram1 = int(pd.to_numeric(phone_sepcs1['ram_capacity'].to_string(index=False, header=False).strip(), errors='coerce') or 0)
ram2 = int(pd.to_numeric(phone_sepcs2['ram_capacity'].to_string(index=False, header=False).strip(), errors='coerce') or 0)

internal_memory1 = int(pd.to_numeric(phone_sepcs1['internal_memory'].to_string(index=False, header=False).strip(), errors='coerce') or 0)
internal_memory2 = int(pd.to_numeric(phone_sepcs2['internal_memory'].to_string(index=False, header=False).strip(), errors='coerce') or 0)

screen_size1 = int(float(pd.to_numeric(phone_sepcs1['screen_size'].to_string(index=False, header=False).strip(), errors='coerce') or 0))
screen_size2 = int(float(pd.to_numeric(phone_sepcs2['screen_size'].to_string(index=False, header=False).strip(), errors='coerce') or 0))

primary_camera1 = int(pd.to_numeric(phone_sepcs1['primary_camera_rear'].to_string(index=False, header=False).strip(), errors='coerce') or 0)
primary_camera2 = int(pd.to_numeric(phone_sepcs2['primary_camera_rear'].to_string(index=False, header=False).strip(), errors='coerce') or 0)

# Sample data
data = {
    'Category': ['price', 'cores', 'battery', 'ram', 'internal_memory', 'screenSize', 'primary_camera'],
    column1: [price1, num_cores1, battery1, ram1, internal_memory1, screen_size1, primary_camera1],
    column2: [price2, num_cores2, battery2, ram2, internal_memory2, screen_size2, primary_camera2],
}

# Create DataFrame
df = pd.DataFrame(data)

# Melt the DataFrame to long-form for seaborn
df_melted = df.melt(id_vars='Category', var_name='Columns', value_name='Values')

# Create subplots
categories = df['Category']

# Calculate the number of rows and columns for a square grid
num_categories = len(categories)
grid_size = math.ceil(math.sqrt(num_categories))  # Square grid dimensions

# Create subplots
fig, axes = plt.subplots(nrows=grid_size, ncols=grid_size, figsize=(15, 15), constrained_layout=True)

# Flatten the axes array for easier indexing
axes = axes.flatten()

# Plot each category in its respective subplot
for i, category in enumerate(categories):
    ax = axes[i]
    barplot = sns.barplot(
        x='Columns',
        y='Values',
        data=df_melted[df_melted['Category'] == category],
        ax=ax
    )
    ax.set_title(f'Comparison for {category}')
    ax.set_xlabel('Models')
    ax.set_ylabel('Values')

    # Add value labels to the bars
    for bar in barplot.patches:
        bar_height = bar.get_height()
        if not pd.isna(bar_height):  # Ensure the value is not NaN
            ax.text(
                bar.get_x() + bar.get_width() / 2,  # X-coordinate (center of the bar)
                bar_height,  # Y-coordinate (height of the bar)
                f'{int(bar_height)}',  # Label text
                ha='center',  # Horizontal alignment
                va='bottom',  # Vertical alignment
                fontsize=10,  # Font size
                color='black'  # Label color
            )

# Hide any unused subplots
for j in range(i + 1, len(axes)):
    axes[j].axis('off')

# Show plot
plt.show()

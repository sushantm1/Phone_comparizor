import os
import math
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from google import genai

# Setup
genai_api_key = os.getenv("GENAI_API_KEY") or "your_fallback_key_here"
client = genai.Client(api_key="")

# Loading and Prepare Data
data = pd.read_csv('smartphones.csv').drop_duplicates()
data['brand_name'] = data['brand_name'].str.lower()
brand_names = data['brand_name'].drop_duplicates().reset_index(drop=True)

# helper functions
def get_valid_brand(prompt):
    while True:
        brand = input(prompt).lower()
        if brand in brand_names.values:
            return brand
        print(" Brand not found. Try again.")

def get_model_index(models, prompt):
    while True:
        try:
            index = int(input(prompt))
            if 0 <= index < len(models):
                return index
            else:
                print("Invalid index. Try again.")
        except ValueError:
            print("Enter a valid number.")

def display_models(df):
    for i, model in enumerate(df['model']):
        print(f"{i}: {model}")

def extract_specs(df):
    def safe_get(column): return int(float(pd.to_numeric(df[column].iloc[0], errors='coerce') or 0))
    return {
        'price': safe_get('price'),
        'cores': safe_get('num_cores'),
        'battery': safe_get('battery_capacity'),
        'ram': safe_get('ram_capacity'),
        'internal_memory': safe_get('internal_memory'),
        'screen_size': safe_get('screen_size'),
        'primary_camera': safe_get('primary_camera_rear')
    }

def generate_ai_comparison(model1, model2):
    input_text = (
        f"Write a detailed comparison between the {model1} and {model2}. "
        f"Behave like I built this AI-based comparison model. Make it concise, direct, and avoid conversational lines."
    )
    print("\n AI Comparison:\n")
    response = client.models.generate_content(model="gemini-2.0-flash", contents=input_text)
    print(response.text)

def plot_bar_charts(specs1, specs2, label1, label2):
    data = {
        'Category': list(specs1.keys()),
        label1: list(specs1.values()),
        label2: list(specs2.values())
    }
    df = pd.DataFrame(data)
    df_melted = df.melt(id_vars='Category', var_name='Phone', value_name='Value')

    num_categories = len(df['Category'])
    grid_size = math.ceil(math.sqrt(num_categories))
    fig, axes = plt.subplots(nrows=grid_size, ncols=grid_size, figsize=(15, 15), constrained_layout=True)
    axes = axes.flatten()

    for i, category in enumerate(df['Category']):
        ax = axes[i]
        plot = sns.barplot(x='Phone', y='Value', data=df_melted[df_melted['Category'] == category], ax=ax)
        ax.set_title(category.capitalize())
        for bar in plot.patches:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, height, f'{int(height)}', ha='center', va='bottom')
    for j in range(i + 1, len(axes)):
        axes[j].axis('off')
    plt.show()

def plot_radar_chart(specs1, specs2, label1, label2):
    import numpy as np

    categories = list(specs1.keys())
    values1 = np.array(list(specs1.values()), dtype=float)
    values2 = np.array(list(specs2.values()), dtype=float)

    values1_norm = values1 / values1.max()
    values2_norm = values2 / values2.max()

    values1 = list(values1_norm) + [values1_norm[0]]
    values2 = list(values2_norm) + [values2_norm[0]]
    categories += [categories[0]]
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    ax.plot(angles, values1, label=label1, linewidth=2)
    ax.fill(angles, values1, alpha=0.25)
    ax.plot(angles, values2, label=label2, linewidth=2)
    ax.fill(angles, values2, alpha=0.25)

    ax.set_thetagrids(np.degrees(angles[:-1]), categories)
    ax.set_title(" Radar Comparison")
    ax.legend()
    plt.show()

# Main Flow
print("Available brands:")
for brand in brand_names:
    print("-", brand)

# Select phone 1
brand1 = get_valid_brand("Enter first brand: ")
models1 = data[data['brand_name'] == brand1].reset_index(drop=True)
display_models(models1)
idx1 = get_model_index(models1['model'], "Enter index for model 1: ")
phone1 = models1.iloc[[idx1]]
label1 = phone1['model'].iloc[0]

# Select phone 2
brand2 = get_valid_brand("Enter second brand: ")
models2 = data[data['brand_name'] == brand2].reset_index(drop=True)
display_models(models2)
idx2 = get_model_index(models2['model'], "Enter index for model 2: ")
phone2 = models2.iloc[[idx2]]
label2 = phone2['model'].iloc[0]

# Compare specs
specs1 = extract_specs(phone1)
specs2 = extract_specs(phone2)

# Show AI Review
generate_ai_comparison(label1, label2)

# Plot graphs
plot_bar_charts(specs1, specs2, label1, label2)
plot_radar_chart(specs1, specs2, label1, label2)

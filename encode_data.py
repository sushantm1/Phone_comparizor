# import google
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
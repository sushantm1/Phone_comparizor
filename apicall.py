# import google
from google import genai

client = genai.Client(api_key="AIzaSyDDBoJswO854qU88dSbdd0zpfi_Z1K0pLk")

response = client.models.generate_content(
    model="gemini-2.0-flash",
    # contents="Write a detailed comparison between the iPhone 16 and Samsung S23 behave as like i " \
    # "made this AI comarision and make it concise and short",
    contents="i want to make a ai model which will compare two phones on the basis of there specification and give me the best one.\n",
)

print(response.text)


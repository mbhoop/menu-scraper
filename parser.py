from dotenv import load_dotenv
import anthropic
import base64
import sys
import json
import os

# read .env and load api key
load_dotenv()

# set up anthropic client
client = anthropic.Anthropic()

allergens = input("Any food allergies? (If none, enter 'no') ").lower()
diets = input("Any dietary restrictions? (If none, enter 'no') ").lower()

# read menu pdf and encode it to base64 bytes
# since you can't send raw binary over a text-based API call
with open(sys.argv[1], "rb") as menu:
    ext = os.path.splitext(sys.argv[1])[1].strip(".")
    base64_bytes = base64.b64encode(menu.read())
    base64_string = base64_bytes.decode('utf-8')

# logic for accepting multiple file types
if ext == 'pdf':
    content_block = {
        "type": "document",
        "source": {"type": "base64", "media_type": "application/pdf", "data": base64_string}
    }
elif ext in ["jpg", "jpeg", "png", "webp"]:
    media_type = f"image/{'jpeg' if ext in ['jpg', 'jpeg'] else ext}"
    content_block = {
        "type": "image",
        "source": {"type": "base64", "media_type": media_type, "data": base64_string}
    }

# send API request to create this message
message = client.messages.create(
    model="claude-sonnet-4-6",
    # max length of response allowed
    max_tokens=5000,
    messages=[
        {
            "role": "user",
            "content": [ 
                content_block,
                {
                    # prompt
                    "type": "text",
                    "text": f"""You are showing which options are safe at this restaurant for a user
                            with certain dietary restrictions.
                            The user has the following allergies: {allergens}.
                            The user follows these diets: {diets}.
                            Parse the provided menu for dishes that are both safe for their diet 
                            and do not contain any of their allergens.
                            List menu items that for sure contain the allergen in the allergen_summary,
                            and list items that follow the diet and are allergen free in diet_summary.
                            Return only the JSON object, no other text.
                            Output response in the following JSON format:
                            {{
                                "summary": "This restaurant poses a high risk for quinoa-allergic diners as quinoa appears in multiple dishes. Cross-contamination is possible. Vegan options are available but limited.",

                                "dishes": [
                                    {{
                                    "name": "Harvest Bowl",
                                    "ingredients": ["quinoa", "roasted vegetables", "tahini", "lemon"],
                                    "allergens_present": ["quinoa"],
                                    "diet_safe": ["vegan", "vegetarian"],
                                    "uncertain_ingredients": []
                                    }}
                                ],
                                "allergen_summary": {{
                                    "quinoa": ["Harvest Bowl"]
                                }},
                                "diet_summary": {{
                                    "vegan": ["Hummus Bowl", "Garden Salad"]
                                }},
                                "uncertain_dishes": {{
                                    "peanuts": ["Chef's Chicken"]
                                }}
                            }}
                            """
                },
            ],
        }
    ],
)

# store API response
response = message.content[0].text

# find where JSON actually starts
start = response.find("{")
end = response.rfind("}") + 1
response = response[start:end]

# converts JSON string into Python object
parsed_menu = json.loads(response)


def contains_allergen(parsed_menu):
    if parsed_menu["allergen_summary"]:
        return True
    return False


def print_results(parsed_menu):
    print(f"\n{parsed_menu["summary"]}")
    if contains_allergen(parsed_menu):
        print(f"\nThis restaurant contains {allergens}!")
        for allergen, dishes in parsed_menu["allergen_summary"].items():
            for dish in dishes:
                print(dish)

    if parsed_menu["diet_summary"]:
        print(f"\nThe following dishes are {diets} and {allergens} free: ")
        for diet, dishes in parsed_menu["diet_summary"].items():
            for dish in dishes:
                print(dish)
        print("\n")
    else:
        print("No items match your diet preferences.")
    
    if parsed_menu["uncertain_dishes"]:
        print(f"The following dishes may possibly contain {allergen}: ")
        for uncertain_dish, dishes in parsed_menu["uncertain_dishes"].items():
            for dish in dishes:
                print(dish)


print_results(parsed_menu)

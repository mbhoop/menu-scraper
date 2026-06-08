from dotenv import load_dotenv
import anthropic
import base64
import sys
import json

# read .env and load api key
load_dotenv()

# set up anthropic client
client = anthropic.Anthropic()

allergens = ["quinoa"]
diets = ["vegan"]

# read menu pdf and encode it to base64 bytes
# since you can't send raw binary over a text-based API call
with open(sys.argv[1], "rb") as menu:
    base64_bytes = base64.b64encode(menu.read())
    base64_string = base64_bytes.decode('utf-8')


# send API request to create this message
message = client.messages.create(
    model="claude-sonnet-4-6",
    # max length of response allowed
    max_tokens=5000,
    messages=[
        {
            # who the message is coming from
            "role": "user",
            # content of the message
            "content": [
            {
                # menu document
                "type": "document",
                "source": {
                    # kind of data in document
                    "type": "base64",
                    # what kind of file
                    "media_type": "application/pdf",
                    # menu as a base64 encoded string
                    "data": base64_string
                }
            },
            {
                # prompt
                "type": "text",
                "text": """You are showing which options are safe for a user
                        who wants to eat at this restaurant but has dietary restrictions. 
                        The user is vegan and allergic to quinoa.
                        Parse the provided menu for dishes that contain quinoa and dishes that are vegan.
                        If you are unsure whether an ingredient contains an allergen or violates a diet, list it in uncertain_ingredients rather than guessing.
                        Return only the JSON object, no other text.
                        Output response in the following JSON format:

                        {
                            "dishes": [
                                {
                                "name": "Harvest Bowl",
                                "ingredients": ["quinoa", "roasted vegetables", "tahini", "lemon"],
                                "allergens_present": ["quinoa"],
                                "diet_safe": ["vegan", "vegetarian"],
                                "uncertain_ingredients": []
                                },
                                {
                                "name": "Chef's Chicken",
                                "ingredients": ["chicken", "satay sauce", "rice"],
                                "allergens_present": [],
                                "diet_safe": [],
                                "uncertain_ingredients": ["satay sauce"]
                                }
                            ],
                            "allergen_summary": {
                                "quinoa": ["Harvest Bowl"]
                            },
                            "diet_summary": {
                                "vegan": ["Harvest Bowl", "Garden Salad"]
                            },
                            "uncertain_dishes": {
                                "peanuts": ["Chef's Chicken"]
                            }
                            }
                        """
                },
            ],
        }
    ],
)
# print API response
print(message.content)

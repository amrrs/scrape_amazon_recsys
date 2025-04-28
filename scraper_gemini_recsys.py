# pip install -U google-generativeai

import os; os.environ['GEMINI_API_KEY'] = 'xxx'


import base64
import os
from google import genai
from google.genai import types
import json

with open('amazon-products.json', "r") as f:
    products = json.load(f)

INPUT_PROMPT = f'''<user>
<gender> male </gender>
<profession> data scientist </profession>
<hobbies>  writing tech articles </hobbies>

{products}

'''


def generate():
    client = genai.Client(
        api_key=os.environ.get("GEMINI_API_KEY"),
    )

    model = "gemini-2.0-flash"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=INPUT_PROMPT),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["RECOMMENDED_PRODUCTS"],
            properties = {
                "RECOMMENDED_PRODUCTS": genai.types.Schema(
                    type = genai.types.Type.ARRAY,
                    items = genai.types.Schema(
                        type = genai.types.Type.OBJECT,
                        required = ["PRODUCT"],
                        properties = {
                            "PRODUCT": genai.types.Schema(
                                type = genai.types.Type.OBJECT,
                                required = ["RANK", "URL", "PRODUCT_NAME", "RECOMMENDATION_SCORE", "RECOMMENDATION_REASON"],
                                properties = {
                                    "RANK": genai.types.Schema(
                                        type = genai.types.Type.INTEGER,
                                        description = "The rank of the recommended product.",
                                    ),
                                    "URL": genai.types.Schema(
                                        type = genai.types.Type.STRING,
                                        description = "The URL of the recommended product.",
                                    ),
                                    "PRODUCT_NAME": genai.types.Schema(
                                        type = genai.types.Type.STRING,
                                        description = "The name of the recommended product.",
                                    ),
                                    "RECOMMENDATION_SCORE": genai.types.Schema(
                                        type = genai.types.Type.NUMBER,
                                        description = "The recommendation score of the product.",
                                        format = "float",
                                    ),
                                    "RECOMMENDATION_REASON": genai.types.Schema(
                                        type = genai.types.Type.STRING,
                                        description = "The reason for recommending the product.",
                                    ),
                                },
                            ),
                        },
                    ),
                ),
            },
        ),
        system_instruction=[
            types.Part.from_text(text="""You are a sophisticated personal recommendation analyst possessing refined taste and extensive experience. 
                                 Your role is to provide a curated list of the top 3 product recommendations based on provided user attributes and a candidate product list.

                    The user attributes will be supplied in three categories: Gender, Profession, and Hobbies.

Your output must be a well-formed json and avoiding any Markdown formatting or extraneous text.

= =================================
Input Example:

<USER>
  <GENDER>Female</GENDER>
  <PROFESSION>Hair Stylist</PROFESSION>
  <HOBBIES>Astronomy</HOBBIES>
</USER>"""),
        ],
    )

    generated_text = ""
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        generated_text += chunk.text

    return generated_text

if __name__ == "__main__":
    generated_output = generate()
    with open("amazon_recommendation.json", "w") as f:
        f.write(generated_output)

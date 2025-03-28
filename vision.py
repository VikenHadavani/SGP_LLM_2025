from flask import Flask, render_template, request
from dotenv import load_dotenv
import os
import google.generativeai as genai
from PIL import Image
import io

app = Flask(__name__, static_folder='static', template_folder='templates')

load_dotenv()  # take environment variables from .env.

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


def get_gemini_response(input_text, image_data):
    """
    Generates a response from the Gemini model based on the input text and image data.

    Args:
        input_text: The text prompt.
        image_data: The image data (bytes).  Can be None.

    Returns:
        The response text from the Gemini model.
    """

    model = genai.GenerativeModel('gemini-2.0-flash')  # Use gemini-2.0-flash for images!
    if image_data:
        try:
            image = Image.open(io.BytesIO(image_data))  # Open image from bytes
        except Exception as e:
            print(f"Error opening image: {e}")
            return "Error processing the image."


        if input_text:
            response = model.generate_content([input_text, image])
        else:
            response = model.generate_content(image)  # Only the image
    else:
        # Handle the case where no image is provided. If you want the non-vision model, then this is the place
        # Otherwise, return an error
        return "Please upload an image."


    return response.text



@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = ""
    uploaded_image_url = None  # For displaying the uploaded image

    if request.method == 'POST':
        input_text = request.form['input_text']
        image_file = request.files['image']

        if image_file:
            image_data = image_file.read()  # Read image as bytes
            response_text = get_gemini_response(input_text, image_data)
            uploaded_image_url = "data:image/jpeg;base64," + str(base64.b64encode(image_data).decode())  # Create base64 URL for display
        else:
            response_text = "Please upload an image."  # Or handle the case differently

    return render_template('index.html', response=response_text, image_url=uploaded_image_url)


import base64  # Import for base64 encoding

if __name__ == '__main__':
    app.run(debug=True)
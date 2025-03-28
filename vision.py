from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
import google.generativeai as genai
from PIL import Image
import io
import base64

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Initialize Flask app
app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.getenv('SECRET_KEY')  # Replace with a secure key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Initialize database and bcrypt
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# User model for database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False) # Add account creation timestamp

# Create the database
with app.app_context():
    db.create_all()

# Function to get Gemini response
def get_gemini_response(input_text, image_data):
    """
    Generates a response from the Gemini model based on the input text and image data.

    Args:
        input_text: The text prompt.
        image_data: The image data (bytes). Can be None.

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
        return "Please upload an image."

    return response.text

# Route: Home (Image Analysis)
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
            response_text = "Please upload an image."

    return render_template('index.html', response=response_text, image_url=uploaded_image_url, session=session)

# Route: Signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'success': False, 'message': 'User already exists'}), 400

        # Hash the password and save the user
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'success': True, 'message': 'Signup successful'})

    return render_template('signup.html')

# Route: Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        print(f"Attempting login for email: {email}")

        # Check if the user exists
        user = User.query.filter_by(email=email).first()
        if not user:
            print("User not found")
            return render_template('login.html', error="Invalid email or password")

        if not bcrypt.check_password_hash(user.password, password):
            print("Incorrect password")
            return render_template('login.html', error="Invalid email or password")

        # Log the user in (store in session)
        session['user_id'] = user.id
        session['email'] = user.email
        print(f"User {email} logged in successfully")

        # Redirect to the main page
        return redirect(url_for('index'))

    return render_template('login.html')

# Route: Profile
@app.route('/profile', methods=['GET'])
def profile():
    if 'user_id' not in session:
        # Redirect to login if the user is not logged in
        return redirect(url_for('login'))

    # Fetch user details from the database
    user = User.query.filter_by(id=session['user_id']).first()
    if not user:
        return redirect(url_for('logout'))  # Log out if the user is not found

    return render_template('profile.html', user=user)

# Route: Logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will recreate the database
    app.run(debug=True)
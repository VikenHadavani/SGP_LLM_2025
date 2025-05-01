from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask import Response
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
app.secret_key = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database and bcrypt
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# User model for database
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

class History(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    input_text = db.Column(db.String(255), nullable=True)
    image_url = db.Column(db.String(255), nullable=True)
    response = db.Column(db.Text, nullable=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

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
            image = Image.open(io.BytesIO(image_data)) 
        except Exception as e:
            print(f"Error opening image: {e}")
            return "Error processing the image."

        if input_text:
            response = model.generate_content([input_text, image])
        else:
            response = model.generate_content(image) 
    else:
        return "Please upload an image."

    return response.text

# Route: Home (Image Analysis)
@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = ""
    uploaded_image_url = None

    if request.method == 'POST':
        input_text = request.form['input_text']
        image_file = request.files['image']

        if image_file:
            image_data = image_file.read()
            response_text = get_gemini_response(input_text, image_data)
            uploaded_image_url = "data:image/jpeg;base64," + str(base64.b64encode(image_data).decode())  # Create base64 URL for display
            # Save the interaction to the History table
            if 'user_id' in session:
                history_entry = History(
                    user_id=session['user_id'],
                    input_text=input_text,
                    image_url=uploaded_image_url,
                    response=response_text
                )
                db.session.add(history_entry)
                db.session.commit()
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
        return redirect(url_for('logout'))

    return render_template('profile.html', user=user)

# Route: history
@app.route('/history', methods=['GET'])
def history():
    if 'user_id' not in session:
        # Redirect to login if the user is not logged in
        return redirect(url_for('login'))

    query = History.query.filter_by(user_id=session['user_id'])

    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    keyword = request.args.get('keyword')

    if start_date:
        query = query.filter(History.timestamp >= start_date)
    if end_date:
        query = query.filter(History.timestamp <= end_date)
    if keyword:
        query = query.filter(History.input_text.contains(keyword) | History.response.contains(keyword))
        
    # Fetch the user's history from the database
    page = request.args.get('page', 1, type=int)
    per_page = 5  
    user_history = History.query.filter_by(user_id=session['user_id']).order_by(History.timestamp.desc()).all()

    return render_template('history.html', history=user_history)

# Route: history/download
@app.route('/history/download', methods=['GET'])
def download_history():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_history = History.query.filter_by(user_id=session['user_id']).order_by(History.timestamp.desc()).all()

    # Generate CSV content
    def generate():
        data = [['Timestamp', 'Input Text', 'Image URL', 'Response']]
        for entry in user_history:
            data.append([
                entry.timestamp.strftime('%Y-%m-%d %H:%M:%S') if entry.timestamp else "N/A",
                entry.input_text or "N/A",
                entry.image_url or "N/A",
                entry.response or "N/A"
            ])
        for row in data:
            yield ','.join(f'"{item}"' for item in row) + '\n'

    return Response(generate(), mimetype='text/csv', headers={"Content-Disposition": "attachment;filename=history.csv"})

#Route: Settings
@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user = User.query.filter_by(id=session['user_id']).first()

    if request.method == 'POST':
        # Update user settings
        new_email = request.form.get('email')
        new_password = request.form.get('password')

        if new_email:
            user.email = new_email
        if new_password:
            hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
            user.password = hashed_password

        db.session.commit()
        return render_template('settings.html', user=user, success="Settings updated successfully!")

    return render_template('settings.html', user=user)

#Route: Help & Support
@app.route('/help', methods=['GET', 'POST'])
def help():
    if request.method == 'POST':
        # Handle support ticket submission
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # For now, just print the message (you can integrate email or database storage)
        print(f"Support Ticket from {name} ({email}): {message}")
        return render_template('help.html', success="Your message has been sent successfully!")

    return render_template('help.html')

# Route: Logout
@app.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('index'))

# Run the app
if __name__ == '__main__':
    app.run(ssl_context=('server.cert', 'server.key'), debug=True)
    
    
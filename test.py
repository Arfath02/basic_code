from flask import Flask, render_template, request, redirect, url_for
import os
from flask_mail import Mail, Message

app = Flask(__name__)

# In a real-world scenario, you would use a database to store reviews.
reviews = []

# Ensure the 'static/photos' directory exists
os.makedirs("static/photos", exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reviews', methods=['GET'])
def view_reviews():
    return render_template('reviews.html', reviews=reviews)

@app.route('/contact')
def contact():
    return render_template('contact.html')


@app.route('/submit_review', methods=['POST'])
def submit_review():
    if request.method == 'POST':
        user_name = request.form.get('userName')
        user_review = request.form.get('userReview')
        
        # Handle file upload
        user_photo = request.files.get('userPhoto')
        
        if user_photo and user_name and user_review:
            # Save the photo in the 'static/photos' folder
            photo_filename = os.path.join("static/photos", f"{user_name}_photo.jpg")
            user_photo.save(photo_filename)

            new_review = {
                'user_name': user_name,
                'user_review': user_review,
                'user_photo': photo_filename,
            }

            reviews.append(new_review)

            # Redirect to the reviews page after submitting a review.
            return render_template('reviews.html', reviews=reviews)

    return "Error submitting review"

# Configure Flask-Mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = 'scarpofficial2526@gmail.com'
app.config['MAIL_PASSWORD'] = 'anoe vxqn ttul uuwz'
app.config['MAIL_DEFAULT_SENDER'] = 'scarpofficial2526@gmail.com'

mail = Mail(app)

@app.route('/submit_form', methods=['GET', 'POST'])
def submit_form():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        message=request.form['message']
        phone=request.form['phone']
        
        # Send email
        msg = Message('Form Submission',
                      recipients=['scarpofficial2526@gmai.com'])
        msg.body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
        mail.send(msg)

        # Redirect to thank-you page
        return redirect(url_for('thank_you'))

    return render_template('main.html')

@app.route('/thank-you')
def thank_you():
    return 'Thank you for submitting the form!'

@app.route('/whatsapp')
def redirect_to_whatsapp():
    phone_number = '+919025792281'
    
    # Construct the WhatsApp URL
    whatsapp_url = f'https://wa.me/{phone_number}'

    # Redirect to WhatsApp
    return redirect(whatsapp_url)
   
if __name__ == '__main__':
    app.run(debug=True)

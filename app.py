from flask import Flask, render_template, request, redirect,flash,url_for,session
from flask_sqlalchemy import SQLAlchemy
from models import db, Review
app= Flask(__name__)

app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()
    
@app.route('/',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email=request.form['email'];
        session['email'] = email
        if(email == 'admin@gmail.com'):
            return redirect('/dashboard')
        else:
            return redirect(url_for('review'))
    return render_template('login.html')

@app.route('/review', methods=['GET', 'POST'])
def review():
    email = session.get('email')
    if request.method == 'POST':
        username = request.form.get('username')
        review_text = request.form.get('review_text')

        if username and review_text:
            new_review = Review(email=email,user=username, review_text=review_text)
            db.session.add(new_review)
            db.session.commit()
    reviews = Review.query.filter_by(email=email).all()
    if  reviews:
         return render_template('index.html', reviews=reviews)

    return render_template('index.html')


@app.route('/dashboard',methods=['GET','POST'])
def dashboard():
   
    return render_template('dashboard.html',reviews=Review.query.all())

@app.route('/delete/<int:sno>',methods=['GET','POST'])
def delete(sno):
    review=Review.query.filter_by(sno=sno).first();
    db.session.delete(review)
    db.session.commit() 
    return redirect('/dashboard')

@app.route('/history',methods=['GET','POST'])
def history():
    if request.method == 'POST':
        username = request.form.get('username')
        reviews = Review.query.filter_by(user=username).all()
        if not reviews:
            flash('No reviews found for this user.')
            return redirect('/review')
        return render_template('index.html',reviews=reviews)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
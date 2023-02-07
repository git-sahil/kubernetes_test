import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from waitress import serve

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI') #f'postgresql://{os.environ.get["POSTGRES_USER"]}:{os.environ.get["POSTGRES_PASSWORD"]}@postgres:5432/dbname'
app.config['SSL_CERT'] = os.environ.get('SSL_CERT') #'/run/secrets/cert'
app.config['SSL_KEY'] = os.environ.get('SSL_KEY') #'/run/secrets/key'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/users')
def get_users():
    users = User.query.all()
    return jsonify([{'username': user.username, 'email': user.email} for user in users])

@app.route('/ready')
def readiness_check():
    return 'OK', 200

if __name__ == '__main__':
    context = (app.config['SSL_CERT'], app.config['SSL_KEY'])
    db.create_all()
    if not User.query.filter_by(username='john').first():
        user = User(username='john', email='john@example.com')
        db.session.add(user)
        db.session.commit()
    serve(app, host='0.0.0.0', port=5000, ssl_context=context)

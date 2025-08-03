from flask import Flask
from routes.users import users_bp  # Import the Blueprint for user routes

app = Flask(__name__)

# Register user routes
app.register_blueprint(users_bp)

@app.route('/')
def home():
    return {"message": "User Management System API is running"}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)

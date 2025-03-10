from app import create_app

# Create Flask app
app = create_app()

# Run only once to create the database
"""from app import create_app, db
app = create_app()
with app.app_context():
    db.create_all()"""

if __name__ == '__main__':
    app.run(debug=True)
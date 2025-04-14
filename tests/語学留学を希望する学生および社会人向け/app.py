from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///stepup.db"
db = SQLAlchemy(app)

@app.route("/api/language_schools", methods=["GET"])
def get_language_schools():
    language_schools = LanguageSchool.query.all()
    return jsonify([school.to_dict() for school in language_schools])

if __name__ == "__main__":
    app.run(debug=True)
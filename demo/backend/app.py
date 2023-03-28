import json
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# tutorial: https://adamraudonis.medium.com/how-to-deploy-a-website-on-aws-with-docker-flask-react-from-scratch-d0845ebd9da4
@app.route('/')  
def home():
    return "ok"

@app.route('/api/get_questions')
def get_questions():
    return {"questions": ["question1", "other stuff", "next question"]}


@app.route('/api/submit_question', methods=["POST"])
def submit_question():
    question = json.loads(request.data)["question"]
    return {"answer": f"Your question was {len(question)} chars long"}

# TODO: turn off debug mode for deployment
if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')

import json
from flask import Flask, request
from flask_cors import CORS
from prompt_gpt import AskGPT
from retrieve_data import QAGPT_DataLoader

app = Flask(__name__)
CORS(app)

aiTA = AskGPT()
QAGPT_Data = QAGPT_DataLoader()

# tutorial: https://adamraudonis.medium.com/how-to-deploy-a-website-on-aws-with-docker-flask-react-from-scratch-d0845ebd9da4
@app.route('/')  
def home():
    return "ok"

@app.route('/api/get_random_qa')
def get_random_qa():
    # return {"questions": ["question1", "other stuff", "next question"]}
    return QAGPT_Data.get_random_qa_trio()

@app.route('/api/submit_question', methods=["POST"])
def submit_question():
    question = json.loads(request.data)["question"]
    gpt_answer = aiTA.ask_gpt(question)
    return {"answer": gpt_answer}

# TODO: turn off debug mode for production
if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')

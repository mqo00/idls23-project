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
    k, d = QAGPT_Data.get_random_qa_trio()
    # print("get random qa keys:", k == d["hash"], type(d["hash"]))
    return d

@app.route('/api/submit_question', methods=["POST"])
def submit_question():
    question = json.loads(request.data)["question"]
    gpt_answer = aiTA.ask_gpt(question)
    # store an entry in the database, hash the question and answer
    k = QAGPT_Data.add_to_db(question, gpt_answer)
    return {"answer": gpt_answer, "hash": k}

@app.route('/api/submit_feedback', methods=["POST"])
def submit_feedback():
    data = json.loads(request.data)
    k = data["key"]
    update_dict = data["update_dict"]
    d = QAGPT_Data.update_db(k, update_dict)
    # print(d)
    return {"status": "ok"}

# TODO: turn off debug mode for production
if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')

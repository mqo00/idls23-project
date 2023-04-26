import os
import json
import time
import openai
from tqdm import tqdm
from dotenv import load_dotenv
from retrieve_data import LabeledQA_DataLoader, write_to_json

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY") # GPT4 & 3.5
openai.organization = os.getenv("OPENAI_ORG_ID") # Organization: cmuwine

def get_token_length(messages):
    token_length = 0
    for message in messages:
        token_length += len(message["content"].split())
    return token_length

def load_json_dict(file='gpt_eval.json'):
    json_d = dict()
    with open(file) as f:
        json_list = json.load(f)
        for d in json_list:
            label, num_examples = d["label"], d["num_examples"]
            question, ta_answer, gpt_answer = d["question"], d["ta_answer"], d["gpt_answer"]
            key = (label, num_examples, question)
            json_d[key] = (ta_answer, gpt_answer)
    return json_d

class AskGPT():
    def __init__(self, gpt="gpt-3.5-turbo", temperature=0.2):
        self.gpt = gpt
        self.temperature = temperature
        self.examples = []
        self.fix_prompt = []

    def format_qa(self, q, a):
        user = {"role": "user", "content": f"Question: {q}."}
        assistant = {"role": "assistant", "content": f"Answer: {a}."}
        return [user, assistant]
    
    # n = 0: zero-shot learning
    def get_qa_examples(self, q, n, label=None):
        return []

    def format_gpt_prompt(self, q, n, label=None):
        system = {"role": "system", "content": "You are a helpful and experienced teaching assistant of a deep learning course."}
        # self.examples = self.get_qa_examples(q, n, label)
        user = {"role": "user", "content": f"Question: {q}."}
        return [system] + self.examples + self.fix_prompt + [user]

    def ask_gpt(self, q, n=0, label=None):
        messages = self.format_gpt_prompt(q, n, label)
        try:
            response = openai.ChatCompletion.create(
                model=self.gpt,
                temperature=self.temperature,
                messages=messages
            )
            error = False
            gpt_answer = response['choices'][0]['message']['content']
        except Exception as e:
            print("Error:", e)
            # print("Message token count", get_token_length(messages))
            response = {}
            error = True
            gpt_answer = "[OPENAI_ERROR] " + str(e)
        
        response["error"] = error
        response["num_examples"] = n
        response["label"] = label
        response["prompt"] = messages
        write_to_json(response, file='gpt_response.json')
        return gpt_answer, messages


class EvalGPT(AskGPT):
    def __init__(self, gpt="gpt-3.5-turbo", temperature=0.2):
        super().__init__(gpt, temperature)
        self.QA_data = LabeledQA_DataLoader()
        self.qa_pairs = self.QA_data.get_qa_pairs()
        self.PrevQA = load_json_dict()
        print("#labels:", len(self.QA_data), "#prev_qa:", len(self.PrevQA))

    def get_qa_examples(self, q, n, label):
        qas = []
        for _ in range(n):
            q, a = self.QA_data.get_random_qa_pair(label)
            qa = self.format_qa(q, a)
            qas += qa
        return qas

    def evaluate_qas(self, start=0, end=2, num_examples=3):
        assert end > start and end <= len(self.qa_pairs)
        for i in tqdm(range(start, end)):
            (label, qa_list) = list(self.qa_pairs.items())[i]
            if (label, num_examples, qa_list[-1][0]) in self.PrevQA:
                print("Already evaluated:", label, num_examples)
                continue
            if len(qa_list) <= 2: continue
            for (q, a) in qa_list:
                if (label, num_examples, q) in self.PrevQA: continue
                assert len(qa_list) > 2
                self.examples = self.get_qa_examples(q, n, label)
                gpt_answer = self.ask_gpt(q, num_examples, label)[0]
                data = {
                    "label": label,
                    "num_examples": num_examples,
                    "question": q,
                    "ta_answer": a,
                    "gpt_answer": gpt_answer
                }
                write_to_json(data, file='gpt_eval.json')
                time.sleep(2) # avoid rate limit
        print("All questions are evaluated!")


GPT = EvalGPT()
length = len(GPT.qa_pairs)
for n in [0, 1, 3, 5, 10, 15, 20]:
    GPT.evaluate_qas(start=0, end=length, num_examples=n)
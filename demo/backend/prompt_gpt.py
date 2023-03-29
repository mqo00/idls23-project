import os
import json
import random
import openai
from tqdm import tqdm
# from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY") # GPT4 & 3.5
openai.organization = os.getenv("OPENAI_ORG_ID") # Organization: cmuwine

# A naive dataloader class to read all test questions & answers & store in dictionary
# class methods to randomly draw one q-a pair or yield all q-a pairs
class QADataLoader():
    def __init__(self, q_file='test-q.txt', a_file='test-a.txt'):
        self.q_file = q_file
        self.a_file = a_file
        self.qa_pairs = dict()

    def __len__(self):
        if len(self.qa_pairs) == 0:
            self.get_qa_pairs()
        return len(self.qa_pairs)

    def __repr__(self):
        if len(self.qa_pairs) == 0:
            self.get_qa_pairs()
        pairs = 3
        length = f"Total {len(self.qa_pairs)} q-a pairs.\n"
        message = f"Printing first {pairs} q-a pairs:\n"
        for i, (q, a) in enumerate(self.qa_pairs.items()):
            if i >= pairs: break
            message += f"{i}-th Question: {q}\nAnswer: {a}\n\n"
        return length + message

    def read_file(self, file):
        with open(file, "r") as f:
            data = f.read()
        return data

    def get_qa_pairs(self):
        q_data = self.read_file(self.q_file)
        a_data = self.read_file(self.a_file)
        # remove the strings with length <=1
        q_list = [q for q in q_data.split("\n") if len(q) > 1]
        a_list = [a for a in a_data.split("\n") if len(a) > 1]
        for q, a in zip(q_list, a_list):
            q = q.replace(u'\xa0', u' ')
            a = a.replace(u'\xa0', u' ')
            self.qa_pairs[q] = a
        return self.qa_pairs
    
    def get_random_qa_pair(self):
        if len(self.qa_pairs) == 0:
            self.get_qa_pairs()
        q = random.choice(list(self.qa_pairs.keys()))
        a = self.qa_pairs[q]
        print("Question:", q)
        print("Answer:", a)
        return q, a
    
class AskGPT():
    def __init__(self, gpt="gpt-3.5-turbo", temperature=0.2):
        self.gpt = gpt
        self.temperature = temperature
        self.QA_data = QADataLoader()
        self.qa_pairs = self.QA_data.get_qa_pairs()
        # QA_data.get_random_qa_pair()

    def format_qa(q, a):
        user = {"role": "user", "content": f"Question: {q}."}
        assistant = {"role": "assistant", "content": f"Answer: {a}."}
        return [user, assistant]
    
    # generate n examples for in-context learning
    def get_qa_examples(self, q, n):
        qas = []
        # TODO: use input q as a key to retrieve the example qa pairs
        for _ in range(n):
            assert n > 0
            q, a = self.QA_data.get_random_qa_pair()
            qa = self.format_qa(q, a)
            qas += qa
        return qas

    # n = 0: zero-shot learning
    def format_gpt_prompt(self, q, n=0):
        system = {"role": "system", "content": "You are a helpful and experienced teaching assistant of a deep learning course."}
        examples = self.get_qa_examples(q, n)
        user = {"role": "user", "content": f"Question: {q}."}
        return [system] + examples + [user]

    def submit_gpt(self, q):
        messages = self.format_gpt_prompt(q)
        # print(messages)
        response = openai.ChatCompletion.create(
            model=self.gpt,
            temperature=self.temperature,
            messages=messages
        )
        gpt_answer = response['choices'][0]['message']['content']
        # print(gpt_answer)
        response["prompt"] = messages
        self.write_to_json(response)
        return gpt_answer

    def write_to_json(self, json_obj, file='gpt_responses.json'):
        # p = Path(directory)
        # p.mkdir(parents=True, exist_ok=True)
        if not os.path.exists(file): # create file not exist and write empty list
            with open(file , 'w+') as f:
                json.dump([], f)
        with open(file) as f:
            json_list = json.load(f)
            json_list.append(json_obj) # need to be not a dict
        with open(file, 'w') as f:
            json.dump(json_list, f, separators=(',', ': '), indent=4)
        # print(f"Write to {file} successfully!")

    def evaluate_qas(self, start=0, end=3):
        assert end > start and end <= len(self.qa_pairs)
        with open('test-gpt.txt', 'a') as f:
            for i in tqdm(range(start, end)):
                (q, a) = list(self.qa_pairs.items())[i]
                # print(f"{i}-th question:")
                gpt_answer = self.submit_gpt(q)
                data = {
                    "question": q,
                    "ta-answer": a,
                    "gpt-answer": gpt_answer
                }
                f.write(f"{i}-th GPT Answer:\n{gpt_answer}\n")
                self.write_to_json(data, file='gpt_eval.json')
            print("All questions are evaluated!")

aiTA = AskGPT() # gpt = "gpt-4")
aiTA.evaluate_qas(start=105, end=len(aiTA.QA_data))


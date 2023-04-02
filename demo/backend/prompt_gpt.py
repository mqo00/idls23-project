import os
import openai
from tqdm import tqdm
from dotenv import load_dotenv
from utils import write_to_json
from retrieve_data import QADataLoader

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY") # GPT4 & 3.5
openai.organization = os.getenv("OPENAI_ORG_ID") # Organization: cmuwine

class AskGPT():
    def __init__(self, gpt="gpt-3.5-turbo", temperature=0.2):
        self.gpt = gpt
        self.temperature = temperature
        self.fix_prompt = []

    def format_qa(self, q, a):
        user = {"role": "user", "content": f"Question: {q}."}
        assistant = {"role": "assistant", "content": f"Answer: {a}."}
        return [user, assistant]
    
    # n = 0: zero-shot learning
    def get_qa_examples(self, q, n):
        return []

    def format_gpt_prompt(self, q, n):
        system = {"role": "system", "content": "You are a helpful and experienced teaching assistant of a deep learning course."}
        examples = self.get_qa_examples(q, n)
        user = {"role": "user", "content": f"Question: {q}."}
        return [system] + examples + self.fix_prompt + [user]

    def ask_gpt(self, q, n=0):
        messages = self.format_gpt_prompt(q, n)
        response = openai.ChatCompletion.create(
            model=self.gpt,
            temperature=self.temperature,
            messages=messages
        )
        gpt_answer = response['choices'][0]['message']['content']
        response["prompt"] = messages
        write_to_json(response, file='gpt_response.json')
        return gpt_answer, messages


class EvalGPT(AskGPT):
    def __init__(self, gpt="gpt-3.5-turbo", temperature=0.2):
        super().__init__(gpt, temperature)
        self.QA_data = QADataLoader()
        self.qa_pairs = self.QA_data.get_qa_pairs()

    def evaluate_qas(self, start=0, end=3):
        assert end > start and end <= len(self.qa_pairs)
        with open('test-gpt.txt', 'a') as f:
            for i in tqdm(range(start, end)):
                (q, a) = list(self.qa_pairs.items())[i]
                # print(f"{i}-th question:")
                gpt_answer = self.ask_gpt(q)[0]
                data = {
                    "question": q,
                    "ta_answer": a,
                    "gpt_answer": gpt_answer
                }
                f.write(f"{i}-th GPT Answer:\n{gpt_answer}\n")
                write_to_json(data, file='gpt_eval.json')
            print("All questions are evaluated!")

class TestGPT(AskGPT):
    def __init__(self, QA_data, gpt="gpt-3.5-turbo", temperature=0.2):
        super().__init__(gpt, temperature)
        self.QA_data = QA_data # QAGPT_DataLoader
        self.fix_prompt = []

    # generate n examples for in-context learning
    def get_qa_examples(self, q, n):
        qas = []
        # TODO: use input q as a key to retrieve the example qa pairs
        for _ in range(n):
            assert n > 0
            _, d = self.QA_data.get_random_qa_trio()
            q, a = d["question"], d["ta_answer"]
            qa = self.format_qa(q, a)
            qas += qa
        return qas
    
    def set_fix_promt(self, qa_pairs):
        for q, a in qa_pairs:
            qa = self.format_qa(q, a)
            self.fix_prompt += qa
        return self.fix_prompt
    
    def set_template_qa(self, q, a):
        qa = self.format_qa(q, a)
        self.fix_prompt += qa
        return self.fix_prompt


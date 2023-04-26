import os
import json
import random
from hashlib import sha256

def write_to_json(json_obj, file='gpt_response.json'):
    if not os.path.exists(file): # create file not exist and write empty list
        with open(file , 'w+') as f:
            json.dump([], f)
    with open(file) as f:
        json_list = json.load(f)
        json_list.append(json_obj) # need to be not a dict
    with open(file, 'w') as f:
        json.dump(json_list, f, separators=(',', ': '), indent=4)


# A naive dataloader class to read all test questions & answers & store in dictionary
# class methods to randomly draw one q-a pair or yield all q-a pairs
class LabeledQA_DataLoader():
    def __init__(self, qa_file='20s_test.json'):
        self.qa_file = qa_file
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

    def get_qa_pairs(self):
        with open(self.qa_file) as f:
            json_list = json.load(f)
            for d in json_list:
                q, a = d["question"], d["answer"]
                label = d["label"]
                qa = self.qa_pairs.get(label, [])
                self.qa_pairs[label] = qa + [(q, a)]
                # a = a.replace(u'\xa0', u' ')
        for label in self.qa_pairs:
            print(label, len(self.qa_pairs[label]))
        return self.qa_pairs
    
    def get_random_qa_pair(self, label):
        if len(self.qa_pairs) == 0:
            self.get_qa_pairs()
        q, a = random.choice(self.qa_pairs[label])
        # print("Label:", label)
        # print("Question:", q)
        # print("Answer:", a)
        return q, a

# read question, ta-ansewer, gpt-answer from json file gpt_eval.json
# store in a dictionary, support random draw or yield all
class QAGPT_DataLoader():
    def __init__(self, file='gpt_eval.json'):
        self.file = file
        self.qa_trios = dict()
    
    def __len__(self):
        if len(self.qa_trios) == 0:
            self.get_qa_trios()
        return len(self.qa_trios)
    
    def __repr__(self):
        return f"Total {len(self)} qa-trios."

    def get_random_qa_trio(self):
        if len(self.qa_trios) == 0:
            self.get_qa_trios()
        k = random.choice(list(self.qa_trios.keys()))
        d = self.qa_trios[k]
        return k, d
    
    def hash_trio(self, q, gpt, ta=""):
        return sha256(q.encode()+ta.encode()+gpt.encode()).hexdigest()
    
    def get_qa_trios(self):
        with open(self.file, "r") as f:
            data = json.load(f)
            for i, d in enumerate(data):
                q = d["question"]
                ta = d["ta_answer"]
                gpt = d["gpt_answer"]
                k = self.hash_trio(q, gpt, ta)
                d["hash"] = k
                d["order"] = i
                self.qa_trios[k] = d
        return self.qa_trios

    def add_to_db(self, q, gpt_answer):
        k = self.hash_trio(q, gpt_answer)
        d = {"question": q, "gpt_answer": gpt_answer, "hash": k}
        self.qa_trios[k] = d
        write_to_json(d, 'gpt_newq.json')
        return k

    # incorrect/unhelpful/great: -1/0/1?
    def update_db(self, k, update_dict):
        d = self.qa_trios[k]
        # update_dict = {"label": "unhelpful", "edit": "new answer"}
        d.update(update_dict)
        self.qa_trios[k] = d
        write_to_json(d, 'label_qa.json')
        return d
    
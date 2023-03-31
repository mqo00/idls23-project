# IDLS23 Project

**An LLM-based Piazza TA Assistant for IDL**

Team Members: 
* Qianou (Christina) Ma (qianoum)
* Yunxin (Silvia) Gu (yunxing)
* Ruixuan (Ray) Tang (ruixuant)
* Saloni Parekh (salonipa)

TA Mentor:
* Vish (vishhvas)
* Harshith Kumar (harunkum)

## Directory
```
Make a GitHub folder structure like:
├── README.md
├── data
│   └── naive_dataset (do not commit)
├── demo
│   ├── backend
│   └── frontend
├── eval
└── model
    ├── baseline_gpt
    ├── finetune_lm
    └── retriever_roberta
```

## Documents 
- Demo app: http://ai-ta.qianouma.com/
- Overleaf Project Writeup (read-only link): https://www.overleaf.com/read/nxjzhtkrbtmb
- Lit Review Google Slides: https://docs.google.com/presentation/d/1eaLwSjnPJyAChPPDPhVofv60f4IpCc6Fg6Hnc-Hce3E/edit?usp=sharing
- Paperpile: https://paperpile.com/shared/J4seto
- Presentation Google Slides: 

## TODOs
* Ray: naive QA pairs (ignoring follow-up) dataset - text form (train, val, test), future step considering follow-up
* Saloni: evaluation (metric other than human eval), future step considering QA API for TAs?
* Silvia: fine-tune RoBERTa downstream task

Christina
* [DONE] BASELINE MODEL: zero-shot Prompt Engineering exploration for GPT3.5 & GPT4
* [DONE] built a simple react & flask webpage for human feedback/labeling and demo
* [TODO] a RoBERTa-based retriever finetuned on piazza data, for building in-context examples for GPT


# Experiment

## Data
* In this study, we plan to use the previous 6 semesters' piazza data from the course of CMU LTI 11785 Intro to Deep Learning (from 2020 Spring to 2022 Fall).
* First, we clean the raw data and create a "naive" dataset, including students' questions and instructors' answers. The size of "naive" QA pairs is 9900,
    * We split the "naive dataset" into train:val:test=64%:16%:20%(6336:1980:1584).
* Todo



## Evaluation
Todo @ Saloni
* Natural Language Inference [(NLI)](https://towardsdatascience.com/natural-language-inference-an-overview-57c0eecf6517), we could evaluate 2 things: 
  * whether the model's responses and the TA's responses are aligned or contradict each other and 
  * whether the model's responses and the external knowledge source (piazza post about assignments) align with each other or not
* ROUGE, BLEU, BERTScore, and BARTScore


## Model 

### GPT3.5 & GPT4
```
Baseline: gpt-3.5-turbo
Temperature = 0.2
Prompt (zeroshot): 
[
  {"role": "system", "content": "You are a helpful and experienced teaching assistant of a deep learning course."},
  {"role": "user", "content": f"Question: {q}."}
]
```
### Finetune Retriever

### Finetune LM
Todo @ Silvia

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
- Overleaf Project Proposal (read-only link): https://www.overleaf.com/read/nxjzhtkrbtmb
- Lit Review Google Slides: https://docs.google.com/presentation/d/1eaLwSjnPJyAChPPDPhVofv60f4IpCc6Fg6Hnc-Hce3E/edit?usp=sharing
- Paperpile: https://paperpile.com/shared/J4seto
- Presentation Google Slides: 

## TODOs
* Ray: naive QA pairs (ignoring follow-up) dataset - text form (train, val, test), future step considering follow-up
* Saloni: evaluation (metric other than human eval), future step considering QA API for TAs?
* Christina: baseline, future step RoBERTa retriever, also build a simple react or flask webpage for playing around with the model
* Silvia: fine-tune RoBERTa downstream task

# Experiment

## Data
Todo @ Ray


## Evaluation
Todo @ Saloni
* Natural Language Inference [(NLI)](https://towardsdatascience.com/natural-language-inference-an-overview-57c0eecf6517), we could evaluate 2 things: 
  * whether the model's responses and the TA's responses are aligned or contradict each other and 
  * whether the model's responses and the external knowledge source (piazza post about assignments) align with each other or not
* ROUGE, BLEU, BERTScore, and BARTScore


## Model 

### GPT3.5 & GPT4
Todo @ Christina
* BASELINE MODEL: zero-shot Prompt Engineering exploration

### Finetune LM
Todo @ Silvia
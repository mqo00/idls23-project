# Model Demo

## Frontend
* Input (Q): 
  * auto generate example of a question
  * a text box for copy/paste new question
* Model:
  * submit request to gpt3.5 & gpt4 for answer given prompt
  * **TODO:** switch different models: with/out retriever, finetunelm, etc.
  * **TODO:** demo the retrieved examples
* Output (A):
  * **TODO:** display nli & machine eval scores, store data
* Human-Eval:
  * **TODO:** feedback for retriever produced examples: thumb up & down
  * additional feedback for model answer: edits & thumb up & down

## Backend
* data processing: just for loop parse all 200 test Q&A pairs & generate responses

## Run servers locally
* `cd backend` (with .venv)
  * `python app.py` (port 8080)
  * `pip freeze -> requirements.txt`
* `cd frontend`
  * use `.env`: `REACT_APP_API_URL=http://localhost:8080/api`
    * `npm start` (port 3000)
    
## Deployment on pythonanywhere for backend:
* `git clone https://github.com/mqo00/idls23-project.git`
* `python3 -m venv .venv` initialize virtual environment and install python packages
  * `source .venv/bin/activate`
  * `pip install -r requirements.txt`
  
## Deployment on Netlify for frontend:
  * `export REACT_APP_API_URL=https://qianoum.pythonanywhere.com/api`
    * `echo "$REACT_APP_API_URL"`
    * `npm run build`

* Here we go! Checkout the web app at http://ai-ta.qianouma.com/

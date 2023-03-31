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

## Deployment on AWS EC2 (t2.micro for backend):
* Connect to your instance using its Public DNS: `ec2-3-22-176-0.us-east-2.compute.amazonaws.com`
* Elastic IP address: `3.22.176.0`

### Setup steps
* `ssh -i "11785_aws.pem" ubuntu@ec2-3-22-176-0.us-east-2.compute.amazonaws.com`
* `git clone https://github.com/mqo00/idls23-project.git`
  * do the same `.venv` setup locally
  * `pip freeze -> requirements.txt`
* `cd idls23-project/demo` setup python
  * `sudo apt-get update`
  * `sudo apt install python3-pip python3-venv`
* `python3 -m venv .venv` initialize virtual environment and install python packages
  * `source .venv/bin/activate`
  * `pip install -r requirements.txt`

### Run servers (with .venv)
* `cd backend`
  * `python app.py` (port 8080)
  * if default port 80, need to run with sudo like this: `sudo /home/ubuntu/idls23-project/demo/.venv/bin/python app.py`

* `cd frontend`
  * `export REACT_APP_API_URL=http://3.22.176.0:8080/api`
  * `echo "$REACT_APP_API_URL"`
  * or use a `.env` file, which contain the above if on EC2, and the follows if locally: `REACT_APP_API_URL=http://localhost:8080/api`
  * `npm start` (port 3000)
  * `npm run build` for Netlify

* Here we go! Checkout the web app at http://ai-ta.qianouma.com/

### tmux
```
tmux
Ctrl+B % split panes
Ctrl+B <- ->
Ctrl+B d detach
tmux ls 
tmux attach -t 0
```

### EBS & Elastic IP
* https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/elastic-ip-addresses-eip.html
* https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ebs-using-volumes.html
* `sudo mkfs -t xfs /dev/xvdf` to install a file system on a new EBS volume
  * `sudo mkdir $YOUR_DIR_NAME`
  * `sudo mount /dev/xvdf $YOUR_DIR_NAME`
* ```sudo chown `whoami` $YOUR_DIR_NAME```


### Download & Upload files
* Upload: `scp -i "~/.ssh/11785_aws.pem" .env ubuntu@ec2-3-22-176-0.us-east-2.compute.amazonaws.com:/file/idls23-project/demo/backend/.env`
* Download `scp -i "~/.ssh/11785_aws.pem" ubuntu@ec2-3-22-176-0.us-east-2.compute.amazonaws.com:/idls23-project/FILE .`

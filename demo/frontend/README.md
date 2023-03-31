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
* **TODO:** Serving
  * actually... I'm too dumb to realize that I can just serve the frontend at [Netlify](https://www.netlify.com/pricing/) or whatever and link it to backend and then I can just use t2.micro ```_(:з」∠)_```
  * tutorials: [1](https://medium.com/@shefaliaj7/hosting-react-flask-mongodb-web-application-on-aws-part-4-hosting-web-application-b8e205c19e4), [2](https://dev.to/asim_ansari7/deploy-a-react-node-app-to-production-on-aws-2gdf), [3](https://adhasmana.medium.com/how-to-deploy-react-and-node-app-on-aws-a-better-approach-5b22e2ed2da2), [4](https://blog.miguelgrinberg.com/post/how-to-deploy-a-react--flask-project)

## Backend
* data processing: just for loop parse all 200 test Q&A pairs & generate responses

## Deployment on AWS EC2:
* Connect to your instance using its Public DNS: `ec2-3-22-176-0.us-east-2.compute.amazonaws.com`
* Elastic IP address: `3.22.176.0`

### Setup steps
* `ssh -i "11785_aws.pem" ubuntu@ec2-3-22-176-0.us-east-2.compute.amazonaws.com`
* `git clone https://github.com/mqo00/idls23-project.git`
  * do the same `.venv` setup locally
  * `pip freeze -> requirements.txt`
* `cd idls23-project/demo` setup python & npm
  * `sudo apt-get update`
  * `sudo apt install python3-pip python3-venv npm`
* `python3 -m venv .venv` initialize virtual environment and install python packages
  * `source .venv/bin/activate`
  * `pip install -r requirements.txt`
* `cd frontend` install node_modules
  * `npm install`

### Run servers (with .venv)
* `cd backend`
  * `python app.py` (port 8080)
  * if default port 80, need to run with sudo like this: `sudo /home/ubuntu/idls23-project/demo/.venv/bin/python app.py`

* `cd frontend`
  * `export REACT_APP_API_URL=http://3.22.176.0:8080/api`
  * `echo "$REACT_APP_API_URL"`
  * or use a `.env` file, which contain the above if on EC2, and the follows if locally: `REACT_APP_API_URL=http://localhost:8080/api`
  * `npm start` (port 3000)

* Here we go! Checkout the web app at [shorturl.at/ntJ26](http://3.22.176.0:3000/)

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

### Check RAM
* `node`
  * `v8.getHeapStatistics()`
  * `export NODE_OPTIONS="--max-old-space-size=15000"`
  * `echo "$NODE_OPTIONS"`


### Download & Upload files
* Upload: `scp -i "~/.ssh/11785_aws.pem" .env ubuntu@ec2-3-22-176-0.us-east-2.compute.amazonaws.com:/file/idls23-project/demo/backend/.env`
* Download `scp -i "~/.ssh/11785_aws.pem" ubuntu@ec2-3-22-176-0.us-east-2.compute.amazonaws.com:/idls23-project/FILE .`

### Build for production
`npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!

See the section about [deployment](https://facebook.github.io/create-react-app/docs/deployment) for more information.

### Other deployment options that I have no time to explore
* [PythonAnywhere](https://www.pythonanywhere.com/pricing/)
* [Heroku](https://www.heroku.com/pricing)
* [Firebase](https://firebase.google.com/pricing)
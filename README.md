# Explainable AI for Meaningful Human Control
## Installation
- Install the Docker version for your OS: https://docs.docker.com/engine/install/
- Start the Docker service: 
``` bash
sudo service docker start
```
- Install the Docker image:
``` bash
sudo docker build -t xai4mhc .
```
- Run the Docker image:
``` bash
sudo docker run -v $(pwd)/experiment_logs:/usr/src/app/experiment_logs \ # store experiment logs locally
                -v $(pwd)/data:/usr/src/app/data \ # store data locally
                -p 3000:3000 \ # map port 3000 of the container to port 3000 on the host
                -p 3001:3001 \ # map port 3000 of the container to port 3000 on the host
                -e PARTICIPANT_ID = "1" \ # replace with the participant ID of your choice
                -e ENVIRONMENT_TYPE = "trial" \ # replace with your environment of choice: trial or experiment
                -e CONDITION = "shap" \ # replace with your explanation condition of choice: baseline, shap, or util
                -e COUNTERBALANCE_CONDITION = "1" \ # replace with your counterbalance condition of choice: 1, 2, 3, 4, 5, 6, 7, or 8
                -e IS_DOCKER = "true" \ # keep this environment variable as it is used to distinguish between running the repository locally or using Docker
                --rm \ # automatically remove the container when it exits
                xai4mhc # specify the Docker image to use
```
- Visit the web GUI at: localhost:3000. In the dropdown menu to choose an agent to view, select brutus or titus (depending on your counterbalance condition):

![localhost-startpage](images/localhost_startpage.png "Localhost Startpage") 

- Install the required dependencies through 'pip install -r requirements.txt'. 
- Launch the human-agent teamwork task by running main.py.
- You will be asked to enter which environment to run. 'Tutorial' will launch a step by step tutorial of the task in a simplified and smaller world, aimed at getting you familiar with the environment, controls, and messaging system. 'Experiment' will launch the complete task, but first you will be asked to enter one of the explainability conditions 'baseline', 'trust', 'workload', or 'performance'. In the 'trust', 'workload', and 'performance' conditions, the agent teammate will model your trust in the agent, workload during the task, or task performance, and adapt its provided explanations accordingly. In the 'baseline' condition, the agent has no user model and will randomly adapt its provided explanations. 
- Go to http://localhost:3000 and clear your old cache of the page by pressing 'ctrl' + 'F5'.
- Open the 'God' and 'human' view. Start the task in the 'God' view with the play icon in the top right of the toolbar. 
- Go to the 'human' view to start the task. Open the messaging interface by pressing the chat box icon in the top right of the toolbar. 

## Task
The objective of the task is to find target victims in the different areas and carry them to the drop zone. Rescuing mildly injured victims (yellow color) add three points to the total score, rescuing critically injured victims (red color) adds six points to the total score. Critically injured victims can only be carried by both human and agent together. Areas can be blocked by three different obstacle types. One of these can only be removed together, one only by the agent, and one both alone and together (but together is much faster). The world terminates after successfully rescuing all target victims, or after 8 minutes. Save the output logs by pressing the stop icon in the 'God' view, which can then be found in the 'experiment_logs' folder. The image below shows the 'God' view and the messaging interface. 

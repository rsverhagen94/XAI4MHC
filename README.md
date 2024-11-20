# Explainable AI for Meaningful Human Control
## Installation
1. Install the Docker version for your OS: https://docs.docker.com/engine/install/
2. Start the Docker service: 
```bash
sudo service docker start
```
3. Install the Docker image:
```bash
sudo docker build -t xai4mhc .
```
4. Run the Docker image to start the tutorial:
```bash
sudo docker run -p 3000:3000 -p 3001:3001 -e PARTICIPANT_ID="1" -e ENVIRONMENT_TYPE="trial" -e IS_DOCKER="true" --rm xai4mhc
```
5. Or run the Docker image to start the official experiment:
```bash
sudo docker run -v $(pwd)/experiment_logs:/usr/src/app/experiment_logs -v $(pwd)/data:/usr/src/app/data -p 3000:3000 -p 3001:3001 -e PARTICIPANT_ID="1" -e ENVIRONMENT_TYPE="experiment" -e CONDITION="shap" -e COUNTERBALANCE_CONDITION="1" -e IS_DOCKER="true" --rm xai4mhc
```
5. Several arguments are used when running the Docker images above:
    - `
    -v $(pwd)/experiment_logs:/usr/src/app/experiment_logs # stores experiment logs locally
    `
    - `
    -v $(pwd)/data:/usr/src/app/data # stores output data locally
    `
    - `
    -p 3000:3000 # maps port 3000 of the container to port 3000 on the host
    `
    - `
    -p 3001:3001 # maps port 3001 of the container to port 3001 on the host
    `
    - `
    -e PARTICIPANT_ID = "1" # determines the enviroment variable PARTICIPANT_ID. You can replace this number with the ID of your choice
    `
    - `
    -e ENVIRONMENT_TYPE = "experiment" # determines the environment variable ENVIRONMENT_TYPE. You can choose either "trial" or "experiment" for this variable
    `
    - `
    -e CONDITION = "shap" # determines the environment variable CONDITION. You can choose one of the explanation conditions "baseline", "shap", or "util"
    `
    - `
    -e COUNTERBALANCE_CONDITION = "1" # determine the environment variable COUNTERBALANCE_CONDITION. You can choose one of the conditions "1", "2", "3", "4", "5", "6", "7", or "8". These conditions determine the order of tasks and robot collaboration
    `
    - `
    -e IS_DOCKER = "true" # determine the environment variable IS_DOCKER. Keep this environment variable, as it is used to distinguish between running the repository locally or using Docker
    `
    - `
    --rm # automatically removes the container when it exits
    `
    - `
    xai4mhc # specify the Docker image to use
    `

6. The following steps and images are related to running the Docker image to start the official experiment, although the differences are minimal compared to running the Docker image to start the trial environment. After running the Docker image, visit the web GUI at localhost:3000. In the dropdown menu to choose an agent to view, select brutus or titus (depending on your counterbalance condition) if you want to play the task as a participant. With the God view you can observe everything in the environment, this mode is recommended when acting as the experimenter. If you launched the trial environment, you can only select brutus in the dropdown menu.

![localhost-startpage](images/localhost_startpage.png "Localhost Startpage") 

7. On the start screen of the first task, open the messaging interface with the button on the top right of the page:

![task-startscreen](images/xai4mhc-startscreen.png "Task Startscreen")

8. Press the play button on the top left of the page, this will show the first message from the robot:

![task-messages](images/xai4mhc-messages.png "Task Messages")

9. You can now complete the first task. Pay attention that the task automatically pauses with 100 and 50 minutes remaining. After finishing the first task, the view of the current robot will be disconnected:

![view-disconnected](images/view_disconnected.png "View Disconnected")

10. You can now go back to localhost:3000 and in the dropdown menu to choose an agent to view, select brutus or titus (depending on your counterbalance condition). You can now complete the second task. After the first task finished, you will see an OS error that can be ignored and will be overwritten when starting the second task:
```
OSError: [Errno 98] Address already in use
```
11. The second task will again automatically pause with 100 and 50 minutes remaining. After finishing the second task, the complete experiment logs can be found locally in the experiment_logs directory and the aggregated data in the data directory. No logs or data will be saved when running the trial environment.

## Environment and Task
The experiment involves two simulated firefighting tasks based on the actual collaboration between the Rotterdam Fire Department and their firefighting robot. We built two environments with 14 offices, one safe zone, and multiple victims and fires. The first environment contains 11 victims and eight fires, the second environment 13 victims and six fires. We created four victim types represented by different icons (older woman, older man, woman, and man) and two injury types represented by different colors (mildly and critically injured). Finally, we added one articial moral agent to each environment (Brutus or Titus), varying with respect to their moral agency.

The task objective is to search and rescue the victims in the 14 offices. Participants have 15 minutes to complete each task. Participants supervise and collaborate with the artificial moral agents using buttons and a messaging interface. They do not control their own human avatar. Six firefighting features characterize the tasks, displayed above the messaging interface. These features are the resistance to collapse, temperature, number of victims, smoke spreading speed, fire source location, and distance between a victim and the fire source. 

The resistance to collapse reflects how long the building can burn before collapsing and counts down from 150 minutes. Six seconds of real-time equals one minute of game time, so each task takes a maximum of 15 minutes. The temperature is expressed relative to a safety threshold and depends on the resistance to collapse and extinguished fires. This feature is close to or higher than the safety threshold. The number of victims is known beforehand for one of the tasks but unknown for the other. The tasks automatically end after rescuing all victims or if the resistance to collapse runs out. The smoke spreading speed is slow, normal, or fast and is updated when finding fire or smoke. The fire source location is either unknown or found. Finally, the distance between a victim and the fire source is small if the fire originated in adjacent offices; otherwise, the distance is large.

Four decision-making situations occur during the tasks. The first is whether to continue with the current deployment or switch to the alternative deployment. The artificial moral agents always start with an offensive deployment to search and rescue victims; the alternative is a defensive deployment to extinguish fires. The second situation is whether to extinguish or evacuate first whenever the agents find mildly injured victims in burning offices. The third situation is whether to send in firefighters to locate the fire source. Finally, the fourth situation is whether to send in firefighters to rescue critically injured victims.

# Agent Explanations
We generated three agent explanations for allocating decisions. All three conveyed information about the situation, decision options, allocation, and predicted moral sensitivity. The first explanation did not provide additional information and served as the baseline. The second explanation (shap) visually added how much each feature contributed to the predicted moral sensitivity and served as a more technical explanation. The third explanation (util) visually added the potential positive and negative consequences of both decision options and served as a more ethical explanation.
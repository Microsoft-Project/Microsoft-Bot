# Genre-recognition

## How to create Docker container to run the application:

```bash
# Create a docker Image
docker build -t djangoapp .
```

```bash
# Start Web app from a docker container
docker run -p 8000:8000 -i -t djangoapp
```

```bash
# Go to following link in the browser
http://localhost:8000
```
## Individual Contribution in Team Work
#### Week 1
| Individual Name  | Description of contribution           | Signature |
|------------------|---------------------------------------|-----------|
| All team members | Create a communication channel        |     *     |
| All team members | Setup the development environment     |     *     |
| All team members | Create a Trello board                 |     *     |
| All team members | Came up with the three ideas to pitch |     *     |
#### Week 2
| Individual Name  | Description of contribution                    | Signature |
|------------------|------------------------------------------------|-----------|
| All team members | Pitch of three ideas and picked the final idea |     *     |
| All team members | Data Collection                                |     *     |
| Shab Pompeiano   | Feature Extraction                             |           |
| All team members | Assignment 1                                   |     *     |
| Haider Ali       | Setup Docker Image                             |           |
| Haider Ali       | Docker readme                                  |           |
#### Week 3
| Individual Name  | Description of contribution        | Signature |
|------------------|------------------------------------|-----------|
| Shab Pompeiano   | Setup Django Project               |           |
| Gagandeep Singh  | Toy Prediction Model               |           |
#### Week 4
| Individual Name  | Description of contribution        | Signature |
|------------------|------------------------------------|-----------|
| Gagandeep Singh  | Website home UI                    |           |
| Shab Pompeiano   | K-Means Clustering                 |           |
| Haider Ali       | Docker Image Squeezing (research)  |           |
#### Week 5
| Individual Name              | Description of contribution                  | Signature |
|------------------------------|----------------------------------------------|-----------|
| Shab Pompeiano               | Different ML models                          |           |
| Haider Ali                   | Docker image squeezing (Implementation)      |           |
| Gagandeep Singh, Haider Ali  | Website admin home UI                        |     *     |
| Shab Pompeiano               | Implement toy model to website (ML Pipeline) |           |
#### Week 6
| Individual Name              | Description of contribution                       | Signature |
|------------------------------|---------------------------------------------------|-----------|
| Shab Pompeiano               | Create final model training script                |           |
| Haider Ali                   | GKE  and Gitlab Kubernetes Integration (Research) |           |
| Gagandeep Singh, Haider Ali  | Add activate model feature                        |     *     |
| Shab Pompeiano               | Data validation                                   |           |
| Shab Pompeiano               | Admin retrain model feature (website)             |           |

#### Week 7
| Individual Name             | Description of contribution                       | Signature |
|-----------------------------|---------------------------------------------------|-----------|
| Haider Ali                  | Cloud Deployment with Kubernetes (Implementation) |           |
| Haider Ali, Gagandeep Singh | Setup CI/CD environment in GitLab                 |     *     |
| Shab Pompeiano              | Unit testing                                      |           |
| Haider Ali, Gagandeep Singh | Website Prediction UI                             |     *     |
#### Week 8 - (Post Fair)
| Individual Name             | Description of contribution                   | Signature |
|-----------------------------|-----------------------------------------------|-----------|
| Haider Ali                  | Integration of Secondary model with User data |           |
| Haider Ali                  | Automatic retraining for Secondary Model      |           |
| Haider Ali, Gagandeep Singh | Repository Code Reformat                      |     *     |
| Haider Ali, Gagandeep Singh | Update ReadMe.md                              |     *     |

## Libraries used
* numpy
* Django v3.1.3
* joblib
* matplotlib
* pandas
* sqlite3
* scikit-learn
* scipy
* sqlparse
* gunicorn
* librosa
* keras v2.4.3
* tensorflow v2.3.0

## Thanks to
* Tailwind CSS
* Alpine.js
* Chart.js
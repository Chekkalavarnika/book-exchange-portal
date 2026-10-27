# BookLoop — Book Exchange Portal (DevOps Case Study)

## 1. Application overview
BookLoop is a small Flask web application for a community book exchange. Visitors can view listed books and add a book with its title, author, and owner. It includes `/health` for Kubernetes health checks.

**Technology:** Python, Flask, Git, Docker, Kubernetes, Jenkins.

> Demo note: the sample book list is held in memory, so newly added books reset when the app/container restarts. This is acceptable for this DevOps demonstration, not a production storage design.

## 2. Project files and what they do
- `app.py` — Flask web application and `/health` endpoint.
- `requirements.txt` — Python dependency list.
- `Dockerfile` — instructions to package the app into a Docker image.
- `.dockerignore` — files excluded from the Docker build context.
- `.gitignore` — files Git should ignore.
- `Jenkinsfile` — CI/CD pipeline: checkout, build image, apply Kubernetes YAML, wait for rollout.
- `k8s/deployment.yaml` — creates two application replicas and health probes.
- `k8s/service.yaml` — exposes the application through NodePort `30080`.

## 3. Prerequisites
Install and verify:
- Git
- Python 3.10+ (for running without Docker)
- Docker Desktop, running with Linux containers
- `kubectl`
- A local Kubernetes cluster such as Minikube, with `minikube` installed
- Jenkins with Pipeline, Git, and Docker/Kubernetes command-line tools available to its agent

The Jenkinsfile is a demonstration pipeline. Jenkins must run on an agent that can use Docker and has a valid Kubernetes context configured. A default Jenkins container usually does **not** have these tools or cluster access automatically.

## 4. Run the application directly (optional first check)
Open a terminal in this project folder:
```bash
python -m venv .venv
```
Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```
Open `http://localhost:5000`. Add a book to test the form. Health endpoint: `http://localhost:5000/health`.

## 5. Git repository
Create an empty repository on GitHub, then run these commands in the project folder (replace the URL with your own repository URL):
```bash
git init
git add .
git commit -m "Initial BookLoop application and DevOps files"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/book-exchange-portal.git
git push -u origin main
```
Do not type the example URL literally; replace `YOUR-USERNAME` with your GitHub username. If Git says the remote already exists, use `git remote set-url origin YOUR-REPOSITORY-URL`.

## 6. Build and test the Docker image
Start Docker Desktop and wait until it says Docker is running. From the project folder:
```bash
docker build -t book-exchange-portal:latest .
docker run --rm -p 5000:5000 book-exchange-portal:latest
```
Open `http://localhost:5000`. Stop the container with `Ctrl+C`. To check the image:
```bash
docker images
```

## 7. Start local Kubernetes
For a simple local demo, start Minikube:
```bash
minikube start
kubectl config current-context
```
**Important:** Minikube must be able to access the image. The easiest local-demo method is:
```bash
minikube image build -t book-exchange-portal:latest .
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
kubectl get deployments
kubectl get pods
kubectl get services
kubectl rollout status deployment/book-exchange
```
Open the application using:
```bash
minikube service book-exchange-service
```
This command normally opens a browser or prints the service URL. You can also try `minikube service book-exchange-service --url`.

If you need to redeploy after changing code, rebuild the image in Minikube and run:
```bash
kubectl rollout restart deployment/book-exchange
kubectl rollout status deployment/book-exchange
```

## 8. Jenkins CI/CD setup
1. Open Jenkins in your browser and sign in.
2. Ensure the Jenkins agent that runs the job has Git, Docker CLI/daemon access, `kubectl`, and access to the same Kubernetes cluster.
3. In Jenkins, choose **New Item** → give it a name such as `BookLoop-CI-CD` → choose **Pipeline**.
4. Under Pipeline, choose **Pipeline script from SCM**, SCM **Git**, and paste your GitHub repository URL. Select branch `*/main` and script path `Jenkinsfile`.
5. Save and click **Build Now**. Open **Console Output** to see each stage.
6. To trigger builds automatically on pushes, configure a GitHub webhook to the Jenkins webhook endpoint or enable a suitable SCM polling trigger. A webhook requires your Jenkins instance to be reachable by GitHub.

**Environment-specific note:** The included Jenkinsfile uses `sh`, which is intended for a Linux-based Jenkins agent. It assumes `docker` and `kubectl` are configured and that the local cluster image is available to Kubernetes. If your Jenkins is running on Windows or on a remote agent/cluster, the commands and image delivery need to match that setup. For a shared/remote cluster, push the image to a registry and update the deployment image to that registry image.

## 9. Quick troubleshooting
- `docker` not recognized: start Docker Desktop or install/configure Docker CLI, then reopen terminal.
- `kubectl` cannot connect: run `minikube start` and check `kubectl config current-context`.
- `ImagePullBackOff`: make sure the image exists inside Minikube with `minikube image ls`, and the deployment image name matches.
- Jenkins `docker: not found` or `kubectl: not found`: install tools on the Jenkins agent; they are not supplied by the Jenkinsfile.
- Jenkins cannot reach cluster: configure Kubernetes context/credentials for the Jenkins agent. Do not put passwords or tokens in Git.
- Port 5000 already in use: stop the other service or use `docker run --rm -p 5001:5000 book-exchange-portal:latest` and open `http://localhost:5001`.

## 10. One-minute video plan
Record your screen and speak clearly. Show each item briefly; don't spend too long on one file.

**Suggested script (about 1 minute):**
“Hello ma’am. My case study application is BookLoop, a Book Exchange Portal built using Python Flask. The `app.py` file displays the available books and lets a user add a book. `requirements.txt` lists Flask as a dependency. The Dockerfile packages the application into a Docker image. The project is stored in Git, and the Jenkinsfile defines the CI/CD stages to check out the code, build the image, and deploy the application. The Kubernetes deployment YAML runs two replicas and checks application health, while the service YAML exposes the app. Here is the running BookLoop application in the browser. I can add a book, and the application is deployed through Kubernetes. This demonstrates the DevOps workflow from source code to deployment. Thank you.”

**Suggested screen order:**
1. Browser: BookLoop running and add-book form.
2. Project folder / GitHub repository: show `app.py`, `requirements.txt`, `Dockerfile`, `Jenkinsfile`, and `k8s` folder.
3. Docker Desktop or terminal: show `docker images` and/or the running container.
4. Jenkins: show pipeline stages and successful Console Output.
5. Terminal: `kubectl get pods` and `kubectl get services`.
6. Return to browser and show the exposed app.

Only claim a stage succeeded after you have actually run and verified it. If time is short, prepare the app and pipeline before recording; use one continuous screen recording with your voice.

## 11. Submission checklist
- [ ] App opens and can add a book
- [ ] Docker image builds and runs
- [ ] Git repository contains the project files
- [ ] Kubernetes pods are Running and service is created
- [ ] Jenkins pipeline runs successfully (if required by your lab environment)
- [ ] One-minute screen recording includes your explanation and the required tools/files

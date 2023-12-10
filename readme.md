<h1>ML Model Deployment Pipeline</h1>

  <h3>Project Overview</h3>

  <p>The project is divided into backend and frontend components.</p>

  <h3>Backend</h3>

  <ul>
    <li>
      <h5>Tech Stack Used:</h5>
      <ul>
        <li>FastAPI</li>
        <li>Transformers</li>
        <li>Pytorch</li>
        <li>Uvicorn</li>
        <li>SqlAlchemy</li>
        <li>Pydantic</li>
      </ul>
    </li>
    <li>
      <h5>Project Details:</h5>
      <ul>
        <li>Utilizes the Transformers library for sentiment analysis.</li>
        <li>Exposes sentiment analysis through a <code>/predict</code> API endpoint (requires user authentication).</li>
        <li>Logs prediction results in a MySQL database, associating results with user IDs.</li>
        <li>Authentication handled by <code>auth.py</code> using JWT tokens and password hashing.</li>
        <li>Database connection managed by <code>database.py</code>.</li>
        <li>Model definitions and API endpoints in <code>models.py</code>.</li>
      </ul>
    </li>
    <li>
      <h5>Containerization:</h5>
      <ul>
        <li>Docker image: <a href="https://hub.docker.com/r/pranaypandeyofficial5/sentiment">pranaypandeyofficial5/sentiment</a>.
        </li>
        <li>Dockerfile sets up the environment and runs the Uvicorn server.</li>
      </ul>
    </li>
    <li>
      <h5>Kubernetes Deployment:</h5>
      <ul>
        <li>Kubernetes configuration in <code>pods.yaml</code>.</li>
        <li>Deployment with three replicas using Kubernetes Deployment.</li>
        <li>Exposes the service through a LoadBalancer.</li>
      </ul>
    </li>
  </ul>

  <h4>pods.yaml Explanation</h4>
  <ul>
    <li><code>apiVersion: apps/v1</code>: Specifies the Kubernetes API version for the Deployment.</li>
    <li><code>kind: Deployment</code>: Indicates that this YAML defines a Deployment.</li>
    <li><code>metadata</code>: Contains metadata for the Deployment, including the name (<code>sentiment-deployment</code>).
    </li>
    <li><code>spec</code>: Specifies the desired state for the Deployment.
      <ul>
        <li><code>replicas: 3</code>: Configures three replicas of the sentiment container. Adjust as needed.</li>
        <li><code>selector</code>: Defines a label selector to match pods with the label <code>app: sentiment</code>.
        </li>
        <li><code>template</code>: Specifies the pod template.
          <ul>
            <li><code>metadata</code>: Labels the pod with <code>app: sentiment</code>.</li>
            <li><code>spec</code>: Defines the pod's specification.
              <ul>
                <li><code>containers</code>: Specifies the containers within the pod.
                  <ul>
                    <li><code>name: sentiment-container</code>: Names the container.</li>
                    <li><code>image: pranaypandeyofficial5/sentiment:1.0</code>: Specifies the Docker image to run in
                      the container.</li>
                    <li><code>ports</code>: Maps the container port 80 to the pod.</li>
                  </ul>
                </li>
              </ul>
            </li>
          </ul>
        </li>
      </ul>
    </li>
  </ul>

  <h4>Service Configuration:</h4>
  <ul>
    <li><code>apiVersion: v1</code>: Specifies the Kubernetes API version for the Service.</li>
    <li><code>kind: Service</code>: Indicates that this YAML defines a Service.</li>
    <li><code>metadata</code>: Contains metadata for the Service, including the name (<code>sentiment-service</code>).
    </li>
    <li><code>spec</code>: Specifies the desired state for the Service.
      <ul>
        <li><code>selector</code>: Defines a label selector to match pods with the label <code>app: sentiment</code>.
        </li>
        <li><code>ports</code>: Configures the ports for the Service.
          <ul>
            <li><code>protocol: TCP</code>: Specifies the protocol.</li>
            <li><code>port: 80</code>: Exposes port 80 on the service.</li>
            <li><code>targetPort: 80</code>: Directs traffic to port 80 on the pods.</li>
          </ul>
        </li>
        <li><code>type: LoadBalancer</code>: Exposes the service through a LoadBalancer.</li>
      </ul>
    </li>
  </ul>

  <h3>API Endpoints</h3>

  <ul>
    <li>
      <h4>Authentication Required:</h4>
      <ul>
        <li><code>POST /auth/</code>: Create a new user (username and password required).</li>
        <li><code>POST /auth/token</code>: Obtain a JWT token from user credentials (username and password).</li>
      </ul>
    </li>
    <li>
      <h4>Authenticated Endpoints:</h4>
      <ul>
        <li><code>GET /</code>: Get the current user.</li>
        <li><code>POST /predict</code>: Log and return sentiment classification and score for the provided prompt.</li>
        <li><code>GET /data</code>: Get results/logs for prompts entered by the current user.</li>
      </ul>
    </li>
  </ul>

  <h3>Steps to Replicate the Backend Locally</h3>

  <ol>
    <li>Create a Python virtual environment:
      <ul>
        <li><code>virtualenv .venv</code> (for Windows)</li>
        <li><code>source .venv/bin/activate</code> (for Linux)</li>
      </ul>
    </li>
    <li>Clone the repository: <code>git clone https://github.com/Pranay-Pandey/ml-assignment-backend</code></li>
    <li>Install dependencies: <code>pip install -r requirements.txt</code></li>
    <li>Run the Uvicorn server (may use <code>--reload</code> to update it on making changes): <code>uvicorn app.main:app</code>
    </li>
    <b>NOTE: You will have to specify DATABASE_URL, SECRET_KEY and ALGORITHM as environment variable before you run this backend</b>
  </ol>

  <p>This will expose the API endpoints. The docs may be checked out from <a href="http://localhost:8000/docs">localhost:8000/docs</a>.
  </p>

  <h3>Running the Docker Container</h3>

  <ul>
    <li>Pull the official Docker container: <code>docker pull pranaypandeyofficial5/sentiment</code></li>
    <li>Build the Docker image locally: <code>docker build -t [name-of-your-docker-image]:tag .</code></li>
    <li>Run the Docker container: <code>docker run --rm -it -p 8080:80 [name-of-your-docker-image]:tag</code></li>
  </ul>

  <p>This will expose your API to <a href="http://localhost:8080/">localhost:8080/</a>.</p>

  <h3>Kubernetes Deployment</h3>

  <ul>
    <li>Deploy Kubernetes using <code>pods.yaml</code>: <code>kubectl create -f pods.yaml</code></li>
    <li>Or deploy pods using terminal commands:
      <ul>
        <li><code>kubectl run [name-your-pod] --image=pranaypandeyofficial5/sentiment:tag --port=80</code></li>
        <li><code>kubectl expose pod [name-of-your-pod] --name=[name-your-service] --port=80</code></li>
        <li><code>kubectl port-forward service/[name-of-your-service] 8080:80</code></li>
      </ul>
    </li>
  </ul>

  <p>Now your API is exposed through the port 8080.</p>

  ![image](https://github.com/Pranay-Pandey/ml-assignment-backend/assets/79053599/731a4d72-e97c-4939-a7a2-6dbcd5758e0f)



  <h2> FrontEnd </h2>

  
  <h3>Project Overview</h3>

  <p>The frontend is built using React and styled with Tailwind CSS. It consists of three main pages: Register, Login, and the main page ("/").</p>

  <h4>Frontend Tech Stack Used:</h4>
  <ul>
    <li>React</li>
    <li>Tailwind CSS</li>
  </ul>

  <h4>Pages and Components:</h4>
  <ul>
    <li><strong>Register Page:</strong> Allows users to create a new account through the API endpoint <code>/auth/</code>.</li>
    <li><strong>Login Page:</strong> Users can log in using the <code>/auth/token/</code> endpoint, which returns a JWT token. This token must be stored for subsequent API requests.</li>
    <li><strong>Main Page ("/"):</strong> Contains two components: Analyse and Results.</li>
    <ul>
      <li><strong>Analyse Component:</strong> Uses the <code>/predict</code> endpoint to submit prompts. The JWT token should be included as a header for authentication. Results are logged in the database for the current user.</li>
      <li><strong>Results Component:</strong> Displays the prediction logs for the current user.</li>
    </ul>
  </ul>

  <h3>Steps to Reproduce the Frontend</h3>

  <ol>
    <li>Clone the repository:
      <code>git clone https://github.com/Pranay-Pandey/ml-assignment-frontend</code>
    </li>
    <li>Build the project:
      <code>npm install .</code>
    </li>
    <li>Create a <code>.env</code> file and set the variable:
      <code>REACT_APP_YOUR_BACKEND_URL</code> as the hosted backend URL.
    </li>
    <li>Start the development server:
      <code>npm run start</code>
    </li>
  </ol>

  <p>This will start the development server hosting the frontend. Make sure the backend is running and accessible at the specified URL in the <code>.env</code> file.</p>

  ![image](https://github.com/Pranay-Pandey/ml-assignment-backend/assets/79053599/53305db6-3ea7-46bb-9625-75ac5339b7c6)
  ![image](https://github.com/Pranay-Pandey/ml-assignment-backend/assets/79053599/46bb36c5-d762-44ec-aacd-3e1bdc553cca)
  ![image](https://github.com/Pranay-Pandey/ml-assignment-backend/assets/79053599/1c6af65b-2a77-473c-93e2-d10d752d45c0)
  ![image](https://github.com/Pranay-Pandey/ml-assignment-backend/assets/79053599/17663a8d-4499-445e-9a77-2558ca003e48)
  ![image](https://github.com/Pranay-Pandey/ml-assignment-backend/assets/79053599/32b63692-b32f-4e4a-a3e3-5566fe030311)

  


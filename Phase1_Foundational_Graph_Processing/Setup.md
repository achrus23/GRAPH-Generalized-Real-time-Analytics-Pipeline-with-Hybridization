# Phase 1: Setup Guide  

**This guide walks through the process of setting up Phase 1 using Docker**.  
Since the **Dockerfile automates everything**, you only need to update a few details and run some commands.

---

## **Step 1: Update the Dockerfile to Use Local Files**  
Since the repository is already cloned, update the **Dockerfile** to **use local files** instead of cloning from GitHub.

### **Changes to Make in the Dockerfile**
**Remove or comment out the GitHub repository cloning section**  
Find this section in the `Dockerfile`:
```dockerfile
# Clone the GitHub repository dynamically
RUN echo "Cloning the repository from GitHub..." && \
    if [ -n "$GITHUB_TOKEN" ] && [ -n "$GITHUB_REPO" ]; then \
        counter=0; \
        until git clone https://${GITHUB_TOKEN}:x-oauth-basic@github.com/${GITHUB_REPO}.git /workspace || [ $counter -gt 5 ]; do \
            echo "Retrying GitHub clone..."; \
            sleep 5; \
            counter=$((counter+1)); \
        done; \
    else \
        echo "Error: Missing GitHub token or repository!"; \
        exit 1; \
    fi

Modify the Dockerfile to Copy Files from Your Local Directory
Add the following line to copy files from your local cloned repository into the container:
# Copy local project files into the Docker container
COPY . /workspace

Modify Python Script Paths (If Needed)
In the Dockerfile, make sure that the Neo4j data loading script points to the correct directory.
Find this line:
python3 /workspace/data_loader.py
```
## **Step 2: Build the Docker Image**
Now, build the Docker image using the updated Dockerfile:
```
docker build -t graph-phase1 .
```
## **Step 3: Run the Docker Container**
Now, start the container to launch the Neo4j database:
```
docker run -d -p 7474:7474 -p 7687:7687 --name graph-container graph-phase1
```
## **Step 4: Access Neo4j Database**
Once the container is running, access Neo4j in a browser at:
```
http://localhost:7474/
```
Login Credentials:
Username: neo4j
Password: project1phase1

Run the following Cypher query to verify that the dataset has been loaded correctly:
```
MATCH (p:Location)-[t:TRIP]->(d:Location) RETURN p, t, d LIMIT 10;
```
## **Step 5: Running Graph Algorithms**
Once Neo4j is set up and running, execute the PageRank and BFS algorithms.

Run Tester
To compute PageRank and BFS scores for locations based on trip connectivity:
```
docker exec -it graph-container bash -c "python3 /workspace/tester.py"
```
## **Step 6: Verify the Graph Data in Neo4j**
To check the created nodes and relationships, run the following query inside the Neo4j Browser:
```
MATCH (n) RETURN n LIMIT 20;
```
To count the total number of trips stored:
```
MATCH ()-[r:TRIP]->() RETURN COUNT(r);
```

# Phase 2: Setup Guide  

## **Step 1: Setup the Orchestrator & Kafka**  
In this step, we will **set up Minikube as the orchestrator** and **Kafka for data ingestion**.

### **1️ Install & Start Minikube**  
If Minikube is not installed, install it from [Minikube Official Site](https://minikube.sigs.k8s.io/docs/start/).

Start Minikube with sufficient resources:  
```sh
minikube start --memory=8192 --cpus=4 --disk-size=30g
```
### **2 Deploy Zookeeper (Kafka Dependency)**
Kafka requires Zookeeper for cluster coordination. Deploy Zookeeper using:
```
kubectl apply -f zookeeper-setup.yaml
```
Verify Zookeeper is running:
```
kubectl get pods -l app=zookeeper
```
### **3 Deploy Kafka**
Kafka is used for streaming data between components.
Deploy Kafka with:
```
kubectl apply -f kafka-setup.yaml
```
Ensure the following environment variables are set in kafka-setup.yaml:
```
env:
  - name: KAFKA_BROKER_ID
    value: "1"
  - name: KAFKA_ZOOKEEPER_CONNECT
    value: "zookeeper-service:2181"
  - name: KAFKA_LISTENER_SECURITY_PROTOCOL_MAP
    value: "PLAINTEXT:PLAINTEXT, PLAINTEXT_INTERNAL:PLAINTEXT"
  - name: KAFKA_ADVERTISED_LISTENERS
    value: "PLAINTEXT://localhost:9092,PLAINTEXT_INTERNAL://kafka-service:29092"
  - name: KAFKA_OFFSETS_TOPIC_REPLICATION_FACTOR
    value: "1"
  - name: KAFKA_AUTO_CREATE_TOPICS_ENABLE
    value: "true"
```
Verify Kafka is running:
```
kubectl get pods -l app=kafka
```

## **Step 2: Deploy Neo4j in Kubernetes
Now, deploy Neo4j for real-time graph data processing.

### **1Deploy Neo4j with Helm**
Neo4j will be deployed in standalone mode.
```
kubectl apply -f neo4j-values.yaml
```

Ensure your neo4j-values.yaml contains:
```
neo4j:
  acceptLicenseAgreement: "yes"
  password: "project1phase2"
  plugins:
    - "graph-data-science"
persistence:
  enabled: true
  size: 10Gi
```

Verify Neo4j deployment:
```
kubectl get pods -l app=neo4j
```

## **Step 3: Connect Kafka to Neo4j**

This step sets up real-time data ingestion from Kafka into Neo4j.

Apply the Kafka → Neo4j Connector:
```
kubectl apply -f kafka-neo4j-connector.yaml
```

Ensure the following configurations in kafka-neo4j-connector.yaml:
```
yaml
config:
  connector.class: "org.apache.kafka.connect.neo4j.Neo4jSinkConnector"
  topics: "trip_data"
  neo4j.server.uri: "bolt://neo4j-service:7687"
  neo4j.authentication.basic.username: "neo4j"
  neo4j.authentication.basic.password: "project1phase2"
```
Verify the connector:
```
kubectl get pods -l app=kafka-neo4j-connector
```

## **Step 4: Start the Data Pipeline**
Once Kafka is running, execute the data producer script to start streaming:
```
python interface.py
```

## **Step 5: Access Neo4j Database**
Once the cluster is running, access Neo4j in a browser:
```
http://localhost:7474/
```

Login Credentials

Username: neo4j
Password: project1phase2

To verify the data is being ingested correctly, run:
```
MATCH (p:Location)-[t:TRIP]->(d:Location) RETURN p, t, d LIMIT 10;
```

## **Step 6: Run Graph Algorithms**

Once Neo4j and Kafka are running, execute PageRank and BFS.

Run Tester:
```
docker exec -it graph-container bash -c "python3 /workspace/tester.py"
```

## **Step 7: Verify the Graph Data in Neo4j**
To check the created nodes and relationships, run:
```
MATCH (n) RETURN n LIMIT 20;
```
To count the total number of trips stored:
```
MATCH ()-[r:TRIP]->() RETURN COUNT(r);
```

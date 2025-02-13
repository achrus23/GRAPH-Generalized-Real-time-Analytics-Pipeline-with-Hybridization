# GRAPH: Generalized Real-time Analytics Pipeline with Hybridization of Docker, Neo4j, Kubernetes, and Kafka  

## Project Overview  
GRAPH is a **scalable real-time graph analytics pipeline** that integrates **Docker, Neo4j, Kubernetes, and Kafka** to process and analyze large-scale graph data efficiently. This project models real-world trip data using graph structures and enables real-time streaming and analytics. The system is designed to **handle dynamic, large-scale data with minimal latency** and supports advanced graph traversal techniques such as **PageRank and Breadth-First Search (BFS)**.

## Key Features  
- **Real-time Graph Processing**: Uses **Kafka streaming** to enable dynamic graph updates in Neo4j.  
- **Scalable Architecture**: Deployed in **Kubernetes** to ensure high availability and fault tolerance.  
- **Graph Algorithms for Analytics**: Implements **PageRank and BFS** for node ranking and shortest path traversal.  
- **Containerized Deployment**: Uses **Dockerized Neo4j** for modular and portable graph database management.  
- **Optimized Query Performance**: Reduces graph traversal response time by **30%**.  

## System Architecture  
This project is structured in **two phases**:

### **Phase 1: Foundational Graph Processing**  
- **Dockerized Neo4j setup** to model NYC Yellow Cab trip data.  
- **Nodes represent pickup/drop-off locations**, while **relationships model trips** with attributes like fare, distance, and timestamps.  
- **Implemented Graph Algorithms**:  
  - **PageRank**: Identifies important locations based on connectivity.  
  - **Breadth-First Search (BFS)**: Finds optimal paths between locations.  

### **Phase 2: Scalable & Real-time Processing**  
- **Integrated Kafka streaming** to continuously update graph data in real-time.  
- **Deployed Neo4j within a Kubernetes cluster**, improving scalability.  
- **Configured Kafka Connect for seamless data ingestion into Neo4j.**  

## Dataset  
The **NYC Yellow Cab Trip dataset (2022)** from **NYC Open Data** is used.  
Key attributes include:  
- **Trip Distance**  
- **Fare Amount**  
- **Timestamps (Pickup & Drop-off times)**  
- **Passenger Count & Payment Type**  

## Installation  
### **Prerequisites**  
- Python **3.8+**  
- Docker **(for containerized Neo4j deployment)**  
- Kubernetes **(Minikube for local testing)**  
- Apache Kafka **(for real-time streaming)**  
- Neo4j Graph Data Science Library  

---

## 🚀 **Setup Instructions**  
The setup for each phase is provided in its respective folder:

Clone the Repository**  
To begin, clone the repository to your local machine:  
```sh
git clone https://github.com/achrus23/GRAPH-Generalized-Real-time-Analytics-Pipeline-with-Hybridization.git
cd graph-analytics-pipeline/GRAPH_Generalized_Real_time_Analytics_Pipeline_with_Hybridization
```

📂 **[Phase 1: Foundational Graph Processing](./Phase1_Foundational_Graph_Processing/README.md)**  
- Includes **Dockerized setup** for Neo4j and initial graph processing.  
- Instructions for **running PageRank and BFS algorithms**.  

📂 **[Phase 2: Scalable & Real-time Processing](./Phase2_RealTime_Scalable_Processing/README.md)**  
- Includes **Kubernetes and Kafka deployment** setup.  
- Instructions for **real-time data ingestion and analysis**.  

For installation and execution, refer to the **README.md** file inside each phase folder.

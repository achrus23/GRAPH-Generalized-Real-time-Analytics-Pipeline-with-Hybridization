# Phase 2: Setup Guide  

🚀 **This guide walks through setting up Phase 2 using Kubernetes and Kafka** to enable real-time graph processing.  
Since the **configuration files automate everything**, you only need to update a few details and run some commands.

---

## 📂 **Project Structure**  
📂 Phase2_RealTime_Scalable_Processing
│-- 📜 README.md # Overview of Phase 2
│-- 📜 setup.md # Detailed setup instructions
│-- 📜 zookeeper-setup.yaml # Zookeeper configuration
│-- 📜 kafka-setup.yaml # Kafka broker setup
│-- 📜 neo4j-values.yaml # Neo4j Helm chart values
│-- 📜 kafka-neo4j-connector.yaml # Kafka → Neo4j streaming config
│-- 📜 interface.py # Interacts with the data pipeline

## 🛠 **Setup Instructions**  
For detailed setup steps, **please refer to** [setup.md](./setup.md).

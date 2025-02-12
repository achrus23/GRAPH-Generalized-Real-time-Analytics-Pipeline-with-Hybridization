# Base image: Ubuntu 22.04
FROM ubuntu:22.04

# Arguments for platform and noninteractive mode for apt
ARG TARGETPLATFORM=linux/amd64,linux/arm64
ARG DEBIAN_FRONTEND=noninteractive

# Arguments for GitHub Token and Repository (set during build)
ARG GITHUB_TOKEN
ARG GITHUB_REPO

# Install necessary packages, Neo4j, Python3, pip, and Java 17 for Neo4j compatibility
RUN apt-get update && \
    apt-get install -y wget gnupg software-properties-common openjdk-17-jdk git && \
    wget -O - https://debian.neo4j.com/neotechnology.gpg.key | apt-key add - && \
    echo 'deb https://debian.neo4j.com stable latest' > /etc/apt/sources.list.d/neo4j.list && \
    add-apt-repository universe && \
    apt-get update && \
    apt-get install -y nano unzip neo4j=1:5.5.0 python3 python3-pip && \
    apt-get autoremove -y && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Set Neo4j authentication (username: neo4j, password: project1phase1)
ENV NEO4J_AUTH=neo4j/project1phase1

# Configure Neo4j settings for external access
RUN sed -i 's/#server.default_listen_address=0.0.0.0/server.default_listen_address=0.0.0.0/' /etc/neo4j/neo4j.conf && \
    sed -i 's|#server.directories.import=/var/lib/neo4j/import|server.directories.import=/var/lib/neo4j/import|' /etc/neo4j/neo4j.conf && \
    sed -i 's/#server.bolt.listen_address=:7687/server.bolt.listen_address=0.0.0.0:7687/' /etc/neo4j/neo4j.conf && \
    sed -i 's/#server.http.listen_address=:7474/server.http.listen_address=0.0.0.0:7474/' /etc/neo4j/neo4j.conf

# Download the GDS plugin for Neo4j
RUN wget -O /var/lib/neo4j/plugins/neo4j-graph-data-science-2.3.1.jar \
    https://graphdatascience.ninja/neo4j-graph-data-science-2.3.1.jar

# Ensure necessary security settings for GDS procedures in neo4j.conf
RUN echo "dbms.security.procedures.unrestricted=gds.*" >> /etc/neo4j/neo4j.conf
RUN echo "dbms.security.procedures.allowlist=gds.*" >> /etc/neo4j/neo4j.conf

# Download the dataset directly to the Neo4j import directory
RUN wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2022-03.parquet -O yellow_tripdata_2022-03.parquet

# Upgrade pip and install required Python libraries
RUN pip3 install --upgrade pip && \
    pip3 install neo4j pandas pyarrow

# Clone the GitHub repository dynamically
RUN echo "Cloning the repository from GitHub..." && \
    if [ -n "$GITHUB_TOKEN" ] && [ -n "$GITHUB_REPO" ]; then \
        counter=0; \
        until git clone https://${GITHUB_TOKEN}:x-oauth-basic@github.com/${GITHUB_REPO}.git /app || [ $counter -gt 5 ]; do \
            echo "Retrying GitHub clone..."; \
            sleep 5; \
            counter=$((counter+1)); \
        done; \
    else \
        echo "Error: Missing GitHub token or repository!"; \
        exit 1; \
    fi && \
    chmod +x /app/*.py

# Start Neo4j, set password using cypher-shell, and stop Neo4j
RUN neo4j start && \
    sleep 20 && \
    echo "ALTER CURRENT USER SET PASSWORD FROM 'neo4j' TO 'project1phase1';" | cypher-shell -u neo4j -p neo4j --database=system && \
    neo4j stop

# Load data into Neo4j using the provided script
RUN neo4j start && \
    sleep 20 && \
    python3 /app/data_loader.py && \
    neo4j stop

# Expose Neo4j ports for HTTP and Bolt
EXPOSE 7474 7687

# Start Neo4j service and keep the container running
CMD ["/bin/bash", "-c", "neo4j start && tail -f /dev/null"]

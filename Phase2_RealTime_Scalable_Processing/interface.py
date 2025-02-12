from neo4j import GraphDatabase

class Interface:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)
        self._driver.verify_connectivity()

    def close(self):
        self._driver.close()

    def ensure_graph_exists(self, session):
        """
        Ensures the in-memory graph 'project1phase2graph' exists; if it does, replaces it.
        """
        graph_name = 'project1phase2graph'

        # Check if the graph already exists
        result = session.run("CALL gds.graph.exists($graph_name) YIELD exists", parameters={"graph_name": graph_name})
        graph_exists = result.single()["exists"]
        
        if graph_exists:
            # Drop the existing in-memory graph
            session.run("CALL gds.graph.drop($graph_name)", parameters={"graph_name": graph_name})
            print(f"Existing graph '{graph_name}' dropped.")

        # Create the in-memory graph with multiple relationship properties
        session.run("""
            CALL gds.graph.project(
                $graph_name,
                'Location',
                {
                    TRIP: {
                        orientation: 'UNDIRECTED',
                        properties: {
                            distance: {
                                property: 'distance'
                            },
                            fare: {
                                property: 'fare'
                            }
                        }
                    }
                }
            )
        """, parameters={"graph_name": graph_name})
        print(f"Graph '{graph_name}' created with properties distance and fare.")

    def bfs(self, start_node, target_nodes):
        """
        Finds the shortest path from start_node to each node in target_nodes using the GDS BFS algorithm.
        Accepts target_nodes as either a single integer or a list of integers.
        Returns a list of paths for each target node, or an empty path if unreachable.
        """
        with self._driver.session() as session:
            # Define the BFS-specific graph name
            bfs_graph_name = 'bfsGraph'
            
            # Check if the BFS graph already exists and drop it if so
            result = session.run("CALL gds.graph.exists($graph_name) YIELD exists", parameters={"graph_name": bfs_graph_name})
            if result.single()["exists"]:
                session.run("CALL gds.graph.drop($graph_name)", parameters={"graph_name": bfs_graph_name})
                # print(f"Existing BFS graph '{bfs_graph_name}' dropped.")
            
            # Create the BFS-specific graph with only necessary properties
            session.run("""
                CALL gds.graph.project(
                    $graph_name,
                    'Location',
                    {
                        TRIP: {
                            orientation: 'UNDIRECTED'
                        }
                    }
                )
            """, parameters={"graph_name": bfs_graph_name})
            # print(f"BFS graph '{bfs_graph_name}' created.")

            # Convert target_nodes to a list if it's a single integer
            if isinstance(target_nodes, int):
                target_nodes = [target_nodes]
            
            paths = []

            # Run BFS for each target node individually
            for target_node in target_nodes:
                result = session.run("""
                    MATCH (source:Location {name: $start_node_name}), (target:Location {name: $target_node_name})
                    CALL gds.bfs.stream($graph_name, {
                        sourceNode: id(source),
                        targetNodes: [id(target)]
                    })
                    YIELD nodeIds
                    RETURN [nodeId IN nodeIds | gds.util.asNode(nodeId).name] AS path
                """, parameters={
                    "graph_name": bfs_graph_name,
                    "start_node_name": start_node,
                    "target_node_name": target_node
                })
                
                # Extract path from result, or add an empty path if not found
                path = [{"name": node_name} for record in result for node_name in record["path"]]
                if path:
                    paths.append({"path": path})
                else:
                    paths.append({"path": []})  # Add an empty path if no result is found
            
            return paths if paths else [{"path": []}]

    def pagerank(self, max_iterations, weight_property):
        """
        Runs PageRank on the graph using the specified weight_property.
        Returns a list with the nodes having the maximum and minimum PageRank scores.
        """
        damping_factor = 0.85
        orientation = 'NATURAL'  # Set orientation variable within the method
        
        with self._driver.session() as session:
            # Define the PageRank-specific graph name
            pagerank_graph_name = 'pagerankGraph'
            
            # Check if the PageRank graph already exists and drop it if so
            result = session.run("CALL gds.graph.exists($graph_name) YIELD exists", parameters={"graph_name": pagerank_graph_name})
            if result.single()["exists"]:
                session.run("CALL gds.graph.drop($graph_name)", parameters={"graph_name": pagerank_graph_name})
                # print(f"Existing PageRank graph '{pagerank_graph_name}' dropped.")
            
            # Create the PageRank-specific graph with weighted properties and specified orientation
            session.run(f"""
                CALL gds.graph.project(
                    $graph_name,
                    'Location',
                    {{
                        TRIP: {{
                            orientation: '{orientation}',
                            properties: {{
                                distance: {{
                                    property: 'distance'
                                }},
                                fare: {{
                                    property: 'fare'
                                }}
                            }}
                        }}
                    }}
                )
            """, parameters={
                "graph_name": pagerank_graph_name,
            })
            # print(f"PageRank graph '{pagerank_graph_name}' created with orientation '{orientation}' and properties distance and fare.")

            # Run the PageRank algorithm
            result = session.run("""
                CALL gds.pageRank.stream($graph_name, {
                    maxIterations: $max_iterations,
                    dampingFactor: $damping_factor,
                    relationshipWeightProperty: $weight_property
                })
                YIELD nodeId, score
                RETURN gds.util.asNode(nodeId).name AS name, score
                ORDER BY score DESC, name ASC
            """, parameters={
                "graph_name": pagerank_graph_name,
                "max_iterations": max_iterations,
                "damping_factor": damping_factor,
                "weight_property": weight_property
            })
            
            # Collect all PageRank scores in a list ordered by descending score
            records = [{"name": record["name"], "score": record["score"]} for record in result]
            
            # If records exist, extract max and min PageRank scores
            if records:
                max_score = records[0]  # First entry is max because it's ordered DESC
                min_score = records[-1]  # Last entry is min
                # print("PageRank Results - Max and Min:", [max_score, min_score])
                return [max_score, min_score]  # Return as a list with max and min
            else:
                # print("No PageRank results found.")
                return []
            
    
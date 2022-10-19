from neo4j import GraphDatabase


def find_nodes(tx):
    query = "MATCH (n:AuthorNode)-[r:WROTE]->(b:BookNode) RETURN b, n, r"
    return [result for result in tx.run(query)]

def find_nodes2(tx):
    query = "MATCH (n:AuthorNode)-[r:WROTE_TEST]->(b:BookNode) RETURN b, n, r"
    return [result for result in tx.run(query)]

user = "neo4j"
pwd = "IIo5sYSiuV3v5JCH-JlchPAzD_ynZlSVT3N5bC-Nzk8"
uri = "neo4j+s://3ff681bc.databases.neo4j.io"

driver = GraphDatabase.driver(uri, auth=(user, pwd))

with driver.session(database="neo4j") as session:
    res = session.execute_read(find_nodes2)

# Node object
book = dict(res[0][0].items())
author = dict(res[0][1].items())

# Relationship object
wrote = dict(res[0][2].items())

driver.close()

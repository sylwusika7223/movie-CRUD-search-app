from neo4j import GraphDatabase

def get_neo4j_session():
    uri = "bolt://localhost:7687"  # Zmienna z URL Neo4j
    username = "neo4j"
    password = "password"  # Zmień na odpowiednie hasło
    driver = GraphDatabase.driver(uri, auth=(username, password))
    return driver.session()

def close_neo4j_session(session):
    session.close()


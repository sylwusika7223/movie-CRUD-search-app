from neo4j import GraphDatabase

def get_neo4j_session():
    uri = "bolt://localhost:7687"  
    #uri = "bolt://neo4j:7687" 
    username = "neo4j"
    password = "password"  
    driver = GraphDatabase.driver(uri, auth=(username, password))
    return driver.session()

def close_neo4j_session(session):
    session.close()
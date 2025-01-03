// Tworzymy węzły dla Filmów, Aktorów i Reżyserów
CREATE (f1:Film {title: 'Inception', genre: 'Sci-Fi', year: 2010})
CREATE (f2:Film {title: 'The Dark Knight', genre: 'Action', year: 2008})
CREATE (a1:Aktor {name: 'Leonardo DiCaprio'})
CREATE (a2:Aktor {name: 'Christian Bale'})
CREATE (r1:Rezyser {name: 'Christopher Nolan'})

// Tworzymy relacje między węzłami
MERGE (a1)-[:GRA_W]->(f1)
MERGE (a2)-[:GRA_W]->(f2)
MERGE (r1)-[:REZYSEUJE]->(f1)
MERGE (r1)-[:REZYSEUJE]->(f2)

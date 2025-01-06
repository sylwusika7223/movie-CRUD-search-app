// Tworzenie indeksów, które zapewnią unikalność
CREATE CONSTRAINT FOR (a:Actor) REQUIRE a.name IS UNIQUE;
CREATE CONSTRAINT FOR (d:Director) REQUIRE d.name IS UNIQUE;
CREATE CONSTRAINT FOR (m:Movie) REQUIRE m.title IS UNIQUE;
CREATE CONSTRAINT FOR (g:Genre) REQUIRE g.name IS UNIQUE;


// Home Alone
MERGE (m:Movie {title: "Home Alone", year: "1990"})
ON CREATE SET m.genre = "Comedy"
MERGE (d:Director {name: "Chris Columbus"})
MERGE (g:Genre {name: "Comedy"})
MERGE (a:Actor {name: "Macaulay Culkin"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a)-[:ACTED_IN]->(m);

// The Matrix
MERGE (m:Movie {title: "The Matrix", year: "1999"})
ON CREATE SET m.genre = "Sci-Fi"
MERGE (d:Director {name: "Lana Wachowski"})
MERGE (g:Genre {name: "Sci-Fi"})
MERGE (a1:Actor {name: "Keanu Reeves"})
MERGE (a2:Actor {name: "Carrie-Anne Moss"})
MERGE (a3:Actor {name: "Laurence Fishburne"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

// The Godfather
MERGE (m:Movie {title: "The Godfather", year: "1972"})
ON CREATE SET m.genre = "Crime"
MERGE (d:Director {name: "Francis Ford Coppola"})
MERGE (g:Genre {name: "Crime"})
MERGE (a1:Actor {name: "Marlon Brando"})
MERGE (a2:Actor {name: "Al Pacino"})
MERGE (a3:Actor {name: "James Caan"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

// Titanic
MERGE (m:Movie {title: "Titanic", year: "1997"})
ON CREATE SET m.genre = "Romance"
MERGE (d:Director {name: "James Cameron"})
MERGE (g:Genre {name: "Romance"})
MERGE (a1:Actor {name: "Leonardo DiCaprio"})
MERGE (a2:Actor {name: "Kate Winslet"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m);

// The Avengers
MERGE (m:Movie {title: "The Avengers", year: "2012"})
ON CREATE SET m.genre = "Action"
MERGE (d:Director {name: "Joss Whedon"})
MERGE (g:Genre {name: "Action"})
MERGE (a1:Actor {name: "Robert Downey Jr."})
MERGE (a2:Actor {name: "Scarlett Johansson"})
MERGE (a3:Actor {name: "Chris Hemsworth"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

// Avatar
MERGE (m:Movie {title: "Avatar", year: "2009"})
ON CREATE SET m.genre = "Sci-Fi"
MERGE (d:Director {name: "James Cameron"})
MERGE (g:Genre {name: "Sci-Fi"})
MERGE (a1:Actor {name: "Sam Worthington"})
MERGE (a2:Actor {name: "Zoe Saldana"})
MERGE (a3:Actor {name: "Sigourney Weaver"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

// The Dark Knight
MERGE (m:Movie {title: "The Dark Knight", year: "2008"})
ON CREATE SET m.genre = "Action"
MERGE (d:Director {name: "Christopher Nolan"})
MERGE (g:Genre {name: "Action"})
MERGE (a1:Actor {name: "Christian Bale"})
MERGE (a2:Actor {name: "Heath Ledger"})
MERGE (a3:Actor {name: "Aaron Eckhart"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

// Pulp Fiction
MERGE (m:Movie {title: "Pulp Fiction", year: "1994"})
ON CREATE SET m.genre = "Crime"
MERGE (d:Director {name: "Quentin Tarantino"})
MERGE (g:Genre {name: "Crime"})
MERGE (a1:Actor {name: "John Travolta"})
MERGE (a2:Actor {name: "Uma Thurman"})
MERGE (a3:Actor {name: "Samuel L. Jackson"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

// Gladiator
MERGE (m:Movie {title: "Gladiator", year: "2000"})
ON CREATE SET m.genre = "Historical Drama"
MERGE (d:Director {name: "Ridley Scott"})
MERGE (g:Genre {name: "Historical Drama"})
MERGE (a1:Actor {name: "Russell Crowe"})
MERGE (a2:Actor {name: "Joaquin Phoenix"})
MERGE (a3:Actor {name: "Connie Nielsen"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

// Interstellar
MERGE (m:Movie {title: "Interstellar", year: "2014"})
ON CREATE SET m.genre = "Sci-Fi"
MERGE (d:Director {name: "Christopher Nolan"})
MERGE (g:Genre {name: "Sci-Fi"})
MERGE (a1:Actor {name: "Matthew McConaughey"})
MERGE (a2:Actor {name: "Anne Hathaway"})
MERGE (a3:Actor {name: "Jessica Chastain"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

// The Social Network
MERGE (m:Movie {title: "The Social Network", year: "2010"})
ON CREATE SET m.genre = "Biography"
MERGE (d:Director {name: "David Fincher"})
MERGE (g:Genre {name: "Biography"})
MERGE (a1:Actor {name: "Jesse Eisenberg"})
MERGE (a2:Actor {name: "Andrew Garfield"})
MERGE (a3:Actor {name: "Justin Timberlake"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

// The Wolf of Wall Street
MERGE (m:Movie {title: "The Wolf of Wall Street", year: "2013"})
ON CREATE SET m.genre = "Biography"
MERGE (d:Director {name: "Martin Scorsese"})
MERGE (g:Genre {name: "Biography"})
MERGE (a1:Actor {name: "Leonardo DiCaprio"})
MERGE (a2:Actor {name: "Jonah Hill"})
MERGE (a3:Actor {name: "Margot Robbie"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

// Inception
MERGE (m:Movie {title: "Inception", year: "2010"})
ON CREATE SET m.genre = "Sci-Fi"
MERGE (d:Director {name: "Christopher Nolan"})
MERGE (g:Genre {name: "Sci-Fi"})
MERGE (a1:Actor {name: "Leonardo DiCaprio"})
MERGE (a2:Actor {name: "Joseph Gordon-Levitt"})
MERGE (a3:Actor {name: "Elliot Page"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

// Jurassic Park
MERGE (m:Movie {title: "Jurassic Park", year: "1993"})
ON CREATE SET m.genre = "Adventure"
MERGE (d:Director {name: "Steven Spielberg"})
MERGE (g:Genre {name: "Adventure"})
MERGE (a1:Actor {name: "Sam Neill"})
MERGE (a2:Actor {name: "Laura Dern"})
MERGE (a3:Actor {name: "Jeff Goldblum"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

// The Shawshank Redemption
MERGE (m:Movie {title: "The Shawshank Redemption", year: "1994"})
ON CREATE SET m.genre = "Drama"
MERGE (d:Director {name: "Frank Darabont"})
MERGE (g:Genre {name: "Drama"})
MERGE (a1:Actor {name: "Tim Robbins"})
MERGE (a2:Actor {name: "Morgan Freeman"})
MERGE (a3:Actor {name: "Bob Gunton"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

// Forrest Gump
MERGE (m:Movie {title: "Forrest Gump", year: "1994"})
ON CREATE SET m.genre = "Drama"
MERGE (d:Director {name: "Robert Zemeckis"})
MERGE (g:Genre {name: "Drama"})
MERGE (a1:Actor {name: "Tom Hanks"})
MERGE (a2:Actor {name: "Robin Wright"})
MERGE (a3:Actor {name: "Gary Sinise"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

// The Lion King
MERGE (m:Movie {title: "The Lion King", year: "1994"})
ON CREATE SET m.genre = "Animation"
MERGE (d:Director {name: "Roger Allers"})
MERGE (g:Genre {name: "Animation"})
MERGE (a1:Actor {name: "Matthew Broderick"})
MERGE (a2:Actor {name: "Jeremy Irons"})
MERGE (a3:Actor {name: "James Earl Jones"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

// The Silence of the Lambs
MERGE (m:Movie {title: "The Silence of the Lambs", year: "1991"})
ON CREATE SET m.genre = "Thriller"
MERGE (d:Director {name: "Jonathan Demme"})
MERGE (g:Genre {name: "Thriller"})
MERGE (a1:Actor {name: "Jodie Foster"})
MERGE (a2:Actor {name: "Anthony Hopkins"})
MERGE (a3:Actor {name: "Scott Glenn"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

// Star Wars: A New Hope
MERGE (m:Movie {title: "Star Wars: A New Hope", year: "1977"})
ON CREATE SET m.genre = "Sci-Fi"
MERGE (d:Director {name: "George Lucas"})
MERGE (g:Genre {name: "Sci-Fi"})
MERGE (a1:Actor {name: "Mark Hamill"})
MERGE (a2:Actor {name: "Harrison Ford"})
MERGE (a3:Actor {name: "Carrie Fisher"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

// Back to the Future
MERGE (m:Movie {title: "Back to the Future", year: "1985"})
ON CREATE SET m.genre = "Adventure"
MERGE (d:Director {name: "Robert Zemeckis"})
MERGE (g:Genre {name: "Adventure"})
MERGE (a1:Actor {name: "Michael J. Fox"})
MERGE (a2:Actor {name: "Christopher Lloyd"})
MERGE (a3:Actor {name: "Lea Thompson"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

// The Matrix Reloaded
MERGE (m:Movie {title: "The Matrix Reloaded", year: "2003"})
ON CREATE SET m.genre = "Sci-Fi"
MERGE (d:Director {name: "Lana Wachowski"})
MERGE (g:Genre {name: "Sci-Fi"})
MERGE (a1:Actor {name: "Keanu Reeves"})
MERGE (a2:Actor {name: "Carrie-Anne Moss"})
MERGE (a3:Actor {name: "Laurence Fishburne"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

// Gladiator 2
MERGE (m:Movie {title: "Gladiator 2", year: "2025"})
ON CREATE SET m.genre = "Action"
MERGE (d:Director {name: "Ridley Scott"})
MERGE (g:Genre {name: "Action"})
MERGE (a1:Actor {name: "Russell Crowe"})
MERGE (a2:Actor {name: "Joaquin Phoenix"})
MERGE (a3:Actor {name: "Connie Nielsen"})
MERGE (m)-[:DIRECTED_BY]->(d)
MERGE (m)-[:IN_GENRE]->(g)
MERGE (a1)-[:ACTED_IN]->(m)
MERGE (a2)-[:ACTED_IN]->(m)
MERGE (a3)-[:ACTED_IN]->(m);

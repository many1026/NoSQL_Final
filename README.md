# NoSQL_Final

## API

### Extraccion del API

```python
import requests
import pymongo

my_client = pymongo.MongoClient("mongodb://localhost:27017/")
my_db = my_client["count"]
collection = my_db["count"]
response = []
response.append(requests.get(url="https://restcountries.com/v3.1/all", headers={'User-Agent':'Custom'}))
response[0] = response[0].json()
print(response[0])
collection.insert_many(response[0])
```

## Mongodb
Al recibir los datos desde la api, nos dimos cuenta que, todos los datos estaban contenidos dentro de un arreglo data, lo cual fue un problema ya que al intentar hacer distintas llamadas tuvimos que llamar primero a data y despues los distintos atributos de nuestros dos objetos principales (players y team)


#### Queries
Regresa los nombres de los jugadores que su nombre termina con 'ael'
```
db.nba.find({"data.first_name":/ael$/},{"data.data":1,"data.first_name":1})
```
Regresa los nombres de los equipos que son parte de la conferencia sureste

```
db.nba.find({"data.team.division": {$in:["Southeast"]}},{"data.data":1,"data.team.full_name":1})
```
Regresa los nombres y id de los jugadores que juegan en la posición PointGuard o que juegan en la conferencia Este
```
db.nba.find({$or:[{"data.position":"G"},{$and:[{"data.conference":{$ne:["East"]}}]}]},{"data.first_name":1, "data.id":1})


## monetdb
#### Objetivo Base Columnar
El objetivo de esta base de datos columnar es poder facilitar la lectura, la vista, y búsqueda de la información que creímos más pertinente de la API que descargamos. Nosotros escogimos la API de los jugadores de la NBA. Sucesivamente, escogimos ciertos atributos cómo el ID del jugador, su nombre completo, el ID del equipo, el nombre del equipo, la conferencia en la que juegan, la división, y la ciudad. La razón es porque queremos mostrar en la BigTable una visualización sencilla para poder encontrar la información básica del jugador y que visualmente alguien que no sepa nada, pueda encontrar muy fácilmente las especificaciones más importantes del jugador. Finalmente, para lograrlo se tuvo que exportar toda la información a monetdb  usando csv con los comandos:

#### Importacion

```
docker exec monetdb monetdb create -p monetdb nba
docker exec -it monetdb  mclient -u monetdb -d nba

CREATE TABLE nba (ID varchar(80), firstName varchar(80), lastName varchar(80), teamID varchar(80), teamCity varchar(80), teamDivision varchar(80), teamFullName varchar(200));
CREATE TABLE teams (ID varchar(80), teamId varchar(80), teamCity varchar(80), teamDivison varchar(80), teamFullName varchar(80));
CREATE TABLE cities (firstName varchar(80), lastName varchar(80), teamCity varchar(80));

COPY OFFSET 2 INTO nba from '/RUTAALARCHIVO/team.csv' on client using delimiters ',', E'\n', '';
COPY OFFSET 2 INTO teams from '/RUTAALARCHIVO/team.csv' on client using delimiters ',', E'\n', '';
COPY OFFSET 2 INTO cities from '/RUTAALARCHIVO/team.csv' on client using delimiters ',', E'\n', '';
```
#### Queries

¿Cual es el porcentaje de jugadores por division?

```SQL
WITH t1 AS 
 (SELECT teamDivision,count(*) AS number 
  FROM nba
  GROUP BY teamDivision)
SELECT teamDivision, number, 
       (0.0+number)/(COUNT(*) OVER (PARTITION BY teamDivision)) -- 0.0+ es para no hacer division integer
FROM t1;
```

¿Cual es el apellido mas comun?
```SQL
SELECT lastName, count(*) as number
  FROM nba
  GROUP BY lastName
  LIMIT 1;
```

¿Cual es la ciudad con mayor numero de jugadores?

```SQL
SELECT teamCity, count(*) as number
  FROM cities
  GROUP BY teamCity
  LIMIT 1;
```

## Neo4j

#### Importacion

```Cypher
//Drop everything in the data base
match (n) detach delete n

//Creating nodes

//Create players
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/many1026/NoSQL_Final/main/nbaDEF.csv" AS row
CREATE (n:Player)
SET n = row

//Create Teams (note: click overview, then node name and select teamCity property)
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/many1026/NoSQL_Final/main/team_city.csv" AS row
CREATE (n:Team)
SET n = row

//Create Cities (note: click overview, then node name and select teamCity property)
LOAD CSV WITH HEADERS FROM "https://raw.githubusercontent.com/many1026/NoSQL_Final/main/city_city.csv" AS row
CREATE (n:City)
SET n = row


//Creating Relations:

//team-player
match (p:Player), (t:Team) where p.teamFullName=t.full_name create (p)-[:Plays_In]->(t)


//team-city
match (t:Team), (c:City) where t.city=c.city create (t)-[:Home_Is]->(c)
```

#### Queries
```Cypher
//¿Cuál es el equipo con más jugadores?
match (p:Player)-[e:Plays_In]->(t:Team)
return t.full_name as team_name, count(e) as num_players
order by num_players descending limit 1
```
```Cypher
```
¿Cuáles son las 5 ligas más populares (las más grandes)?

```Cypher
match (p:Player) return p.teamDivision, count(p.teamDivision) as player_per_division order by player_per_division descending limit 5

```

```Cypher
// ¿Cual es el numero de jugadores por ciudad?
MATCH (p:Player)
RETURN p.teamName, count(p.teamCity) as n
ORDER BY n DESC
```


## Comparacion entre Columnar (monetdb), Grafica (neo4j) y de Documentos (mongodb)

La diferencia entre monetdb y neo4j almacenan bases de datos radica en la forma en la que almacenan los datos. Las bases de datos columnares guardan los datos en columnas relacionadas, mientras que en las bases de datos graficas los datos se almacenan en nodos y aristas, que representan las entidades y relaciones de la base de datos. Esto significa que las bases de datos columnares sirven para datos que son almacenados en columnas, como hojas de calculo, mientras que las bases de datos graficas sirven para datos cuyas relaciones son de extrema importancia, como las redes.

Asi, se puede ver que el proposito de ambas. Por un lado, las bases de datos columnares permiten la busqueda eficiente de datos dentro de una misma columna, en lugar de buscar en toda la base de datos, haciendo que sea la mejor opcion para analiticas donde se tenga un gran numero de datos; por otro lado, las bases de datos graficas permiten representar y buscar de manera eficiente las relaciones complejas y de gran numero, como cadenas de suministros, algo que no es posible hacer en una columnar, con su tendencia a tener datos duplicados.

Completamente aparte estan las bases de datos basadas en Documentos, que son ideales para datos que no tengan una estructura definida, o datos que contengan subdatos. Son ideales cuando se requiere flexibilidad para guardar datos cuyos atributos sean dinamicos y variables en un mismo formato estandar.

Podemos concluir, entonces, que la implementacion de bases de datos no-relacionales no es tan estandar como lo era SQL, cada una con sus fortalezas y debilidades, donde el cual usar dependera en gran parte de los requerimientos especificos de la aplicacion y el tipo de dato que se guardara.

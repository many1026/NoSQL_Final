# Proyecto Final

### Extraccion del API

Explicacion

#### Codigo


### Importacion a Mongodb

Explicacion

#### Codigo

### Transformacion a csv

Explicacion

#### Codigo

### Importacion a monetdb
#### Objetivo Base Columnar
El objetivo de esta base de datos columnar es poder facilitar la lectura, la vista, y búsqueda de la información que creímos más pertinente de la API que descargamos. Nosotros escogimos la API de los jugadores de la NBA. Sucesivamente, escogimos ciertos atributos cómo el ID del jugador, su nombre completo, el ID del equipo, el nombre del equipo, la conferencia en la que juegan, la división, y la ciudad. La razón es porque queremos mostrar en la BigTable una visualización sencilla para poder encontrar la información básica del jugador y que visualmente alguien que no sepa nada, pueda encontrar muy fácilmente las especificaciones más importantes del jugador. Finalmente, para lograrlo se tuvo que exportar toda la información a monetdb  usando csv con los comandos:

#### Codigo para ingresar datos a monetdb

#+begin_src shell
docker exec monetdb monetdb create -p monetdb nba
docker exec -it monetdb  mclient -u monetdb -d nba

CREATE TABLE nba (ID varchar(80), firstName varchar(80), lastName varchar(80), teamID varchar(80), teamCity varchar(80), teamDivision varchar(80), teamFullName varchar(200));
CREATE TABLE teams (ID varchar(80), teamId varchar(80), teamCity varchar(80), teamDivison varchar(80), teamFullName varchar(80));
CREATE TABLE cities (firstName varchar(80), lastName varchar(80), teamCity varchar(80));


COPY OFFSET 2 INTO nba from '/RUTAALARCHIVO/team.csv' on client using delimiters ',', E'\n', '';
COPY OFFSET 2 INTO teams from '/RUTAALARCHIVO/team.csv' on client using delimiters ',', E'\n', '';
COPY OFFSET 2 INTO cities from '/RUTAALARCHIVO/team.csv' on client using delimiters ',', E'\n', '';
#+end_src

#### Una vez dentro de mongodb, usamos el siguiente bloque de codigo para comprobar que los datos se mandaron

#+begin_src shell
mongo
use monetdb
show collections
db.nba.find()
#+end_src


### Importacion a Base de Datos Grafica

Explicacion

#### Codigo

### Comparacion entre Columnar (monetdb) vs Grafica (neo4j)

PURA EXPLICACION

### Conclusion

PURA EXPLICACION

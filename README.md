# Proyecto Individual 1 Henry

## Introducción

Este proyecto es una API sencilla construida con FastAPI y deployada en render para consultar y recuperar información de un conjunto de datos relacionado con películas y actores. La API proporciona endpoints para obtener información sobre películas basadas en sus títulos o en actores basados en sus nombres.

Fue realizado como metodo eavluatorio de la carrera de DataSciense de Henry

### Endpoints

#### 1. Obtener películas por título
El endpoint _score_titulo()_ recibe un título de pelicula y devuelve como resultado información de su fecha de estreno y popularidad

#### 2. Obtener filmaciones por día
El endpoint _filmaciones_dia(dia: str)_ recibe un día de la semana y devuelve como resultado información de la cantidad de peliculas que se estrenaron ese día de la semana.

#### 3. Obtener filmaciones por mes
El endpoint _filmaciones_mes(dia: str)_ recibe un mes y devuelve como resultado información de la cantidad de peliculas que se estrenaron ese mes en el dataset.

#### 4. Obtener votaciones
El endpoint _votos_titulo(titulo_de_la_filmacion: str)_ recibe como parámetro el título de una pelicula y, en caso de que haya recibido 2000 o más votos, devuelve la cantidad de votos que ha recibido y el promedio de las valoraciones.

#### 5. Obtener información de actor
El endpoint _get_actor(nombre: str):_ recibe como parámetro el nombre y apellido de un actor y devuelve un str con la cantidad de películas en que ha participado y el retorno de esas películas, total y promedio.

#### 6. Obtener información de un director
El endpoint _get_director(nombre: str):_ recibe como parámetro el nombre y apellido de un director y devuelve información del total de retornoconseguido y un listado de todas las películas que dirigió con título, fecha de estreno, costo y retorno.

#### 7. Por último el recomendador
Este endpoint tien la función de recomendación de peliculas, recibe como parámetro una pelicula y devuelve 5 títluos de pelicula similares.

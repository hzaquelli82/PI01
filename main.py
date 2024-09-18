from fastapi import FastAPI
import pandas as pd
import unicodedata
import numpy as np


app = FastAPI()

df = pd.read_parquet('movies_datasets.parquet')
ml =  pd.read_parquet('ml.parquet')

#Funcion para obtener datos de título, año de estreno y popularidad de una pelicula
@app.get("/score_titulo/{titulo_de_la_filmacion}")
async def score_titulo(titulo_de_la_filmacion: str):
    '''
    Esta función recibe como dato un título de película y devuelve título, año de estreno
    y Popularidad.
    
    Parámetros:
    titulo_de_la_filmación (str): Título de la película.
    
    Retorna:
    str: Texto con el título de la pelicula, año de estreno y popularidad
    '''
    # Cambiamos el valor de titulo_de_la_filmación a lowercase para buscar
    titulo_de_la_filmacion = titulo_de_la_filmacion.lower()
    # Filtramos el DataFrame para obtener la fila que corresponde al título de la película
    fila_pelicula = df.loc[df['title'] == titulo_de_la_filmacion]
    
    # Verificamos si se encontró la película
    if not fila_pelicula.empty:
        # Obtenemos el año de estreno y la popularidad de la película
        result_year = int(fila_pelicula['release_year'].values[0])
        result_popularity = fila_pelicula['popularity'].values[0]
        # Volvemos a cambiar el valor de titulo_de_la_filmación a title case para devolverlo
        titulo_de_la_filmacion = titulo_de_la_filmacion.title()        
        # Imprimimos la información de la película
        return {'La película %s fue estrenada en el año %i, y tuvo una popularidad de %f' % (titulo_de_la_filmacion, result_year, result_popularity)}
    else:
        return {'No se encontró la película con el título "%s"' % titulo_de_la_filmacion}


#Función para obtener la cantidad de películas estrenadas en una fecha
@app.get("/filmaciones_dia/{dia}")
async def filmaciones_dia(dia: str):
    '''
    Esta función recibe como dato un día de la semana, escrito en español y 
    devuelve la cantidad de peliculas estrenadas ese día en todo el dataset
    
    Parámetros:
    dia (str): Día de la semana en español

    Return:
    str: string con la cantidad de películas'''
    
    #COnvertir dia a lower case
    dia = dia.lower()

    #Eliminar caracteres no deseados
    dia = unicodedata.normalize('NFD', dia).encode('ascii', 'ignore').decode('utf-8')

    #USar un diccionario para relacionar el día de la semana en español a inglés
    dia_ingles = {
        'lunes': 'Monday',
        'martes': 'Tuesday',
        'miercoles': 'Wednesday',
        'jueves': 'Thursday',
        'viernes': 'Friday',
        'sabado': 'Saturday',
        'domingo': 'Sunday'
    }

    #Guardo la cantidad de películas en la variable cantidad
    cantidad_dia = (df['release_day'] == dia_ingles[dia]).sum()
    return {'%s cantidad de películas fueron estrenadas en los días %s' % (cantidad_dia, dia.capitalize())}


#Función para obtener la cantidad de películas estrenadas en un mes dado
@app.get("/filamaciones_mes/{mes}")
async def filmaciones_mes(mes: str):
    '''Esta función recive el mes como parámetro y devuelve las 
    filmaciones estrenadas a ese mes
    
    Parámetro:
    mes (str): mes de la filmación. Puede ser 'Enero', 'Febrero', ..., 'Diciembre'

    Retorna:
    str: String con la cantidad de filmaciones estrenadas ese mes en todo el datasets
    '''

    #Diccionario con los meses del año
    mes_dic = {'enero':1,
               'febrero':2,
               'marzo':3,
               'abril':4,
               'mayo':5,
               'junio':6,
               'julio':7,
               'agosto':8,
               'septiembre':9,
               'octubre':10,
               'noviembre':11,
               'diciembre':12}
    
    #Cambiamos nombre del mes a minúsculas
    mes = mes.lower()
    #Guardamos la cantidad encotrada en la variable cantidad
    cantidad_mes = (df['release_month'] == mes_dic[mes]).sum()
    mes = mes.capitalize()
    return {'%i peliculas se estrenaron en %s' % (cantidad_mes, mes)}


#Función para obtener votaciones de películas
@app.get("/votaciones/{titulo_de_la_filmacion}")
async def votos_titulo(titulo_de_la_filmacion: str):
    '''Esta función recibe el título de una película y devuelve 
    la cantidad de votos que tiene y la valoración promedio
    en el dataset, siempre que tenga al menos 2000 votos.
    Si no existe la película, devuelve un mensaje de error
    
    Parámetro:
    titulo_de_la_filmacion (str): Título de la película

    Retorna:
    str: String con titulo, cantidad de votos y  valoración promedio
    '''

    #Transformamos el título a minusculas
    titulo_de_la_filmacion = titulo_de_la_filmacion.lower()

    #Generamos máscaras para filtrar el dataframe
    mask1 = df['title'] == titulo_de_la_filmacion
    mask2 = df['vote_count'] > 1999

    #Generamos la lista de índices que coinciden con las máscaras
    lista = df[mask1 & mask2].index.tolist()

    #Proceso de selección y resultados
    if not len(lista) == 0:
        for indice in lista:
            votos = int(df.loc[indice,'vote_count'])
            año_estreno = df.loc[indice,'release_year']
            votacion = df.loc[indice,'vote_average']
            return {f'La pelicula {titulo_de_la_filmacion} fue estrenada en el {año_estreno}.La misma cuenta con un total de {votos} valoraciones, con un promedio de {votacion}'}
    elif titulo_de_la_filmacion in df['title'].values:
        return {'La película posee menos de 2000 valoraciones'}
    else:
        return {'La película no existe en la base de datos'}

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Crea un vectorizador TF-IDF
vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))

# Ajusta el vectorizador a la columna 'overview' y transforma los datos
tfidf_matrix = vectorizer.fit_transform(ml['features'])

# Calcula la similitud coseno entre los vectores
similarity_matrix = cosine_similarity(tfidf_matrix)

#Funcion de recomendacion
@app.get('/recomendador/{titulo}')
def recomendador(titulo: str):

    #Poner titulo en minúsculas
    titulo = titulo.lower()
    # Obtener el id de la película
    movie_id =  ml.loc[ml['title'] == titulo, 'id'].values[0]
    # Obtiene el índice de la película en la matriz de similitud
    idx = np.where(ml['id'] == movie_id)[0][0]
    
    # Obtiene las puntuaciones de similitud para la película
    scores = list(enumerate(similarity_matrix[idx]))
    
    # Ordena las puntuaciones en orden descendente
    scores.sort(key=lambda x: x[1], reverse=True)
    
    # Obtiene las películas similares
    similar_movies = [ml.iloc[i,1] for i, _ in scores[1:6]]
    
    return similar_movies

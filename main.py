from fastapi import FastAPI
import pandas as pd

app = FastAPI()

df = pd.read_parquet('movies_datasets.parquet')

@app.get("/score_titulo/{titulo_de_la_filmacion}")
async def score_titulo(titulo_de_la_filmacion: str):
    '''
    Esta función recibe como dato un título de película y devuelve título, año de estreno
    y valoración.
    
    Parámetros:
    titulo_de_la_filmación (str): Título de la película.
    df (DataFrame): DataFrame que contiene la información de las películas.
    
    Retorna:
    None
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
        titulo_de_la_filmacion = titulo_de_la_filmacion.title()

        
        # Imprimimos la información de la película
        return {'La película %s fue estrenada en el año %i, y tuvo una popularidad de %f' % (titulo_de_la_filmacion, result_year, result_popularity)}
    else:
        return {'No se encontró la película con el título "%s"' % titulo_de_la_filmacion}

@app.get("/filmaciones_dia/{dia}")
async def filmaciones_dia(dia: str):
    '''
    Esta función recibe como dato un día de la semana y devuelve 
    la cantidad de estrenos de ese día.
    
    Parámetros:
    dia (str): Día de la semana

    Return:
    string con la cantidad de películas'''
    dia = pd.to_datetime(dia, format='%Y-%m-%d')
    cantidad = (df['release_date'] == dia).sum()
    return {'En el día %s, se estrenaron %s películas' % (dia.date(), cantidad)}

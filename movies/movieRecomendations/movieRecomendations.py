from dotenv import load_dotenv, find_dotenv
import json
import os
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity
import numpy as np
import requests
from PIL import Image
from io import BytesIO

def generateMovie(search):
  _ = load_dotenv('.env')

  with open('jsons/movie_descriptions_embeddings.json', 'r') as file:
      file_content = file.read()
      movies = json.loads(file_content)

  emb = get_embedding(movies[1]['description'],engine='text-embedding-ada-002')

  req = search
  emb = get_embedding(req,engine='text-embedding-ada-002')

  sim = []
  for i in range(len(movies)):
    sim.append(cosine_similarity(emb,movies[i]['embedding']))
  sim = np.array(sim)
  idx = np.argmax(sim)

  return movies[idx]['title']

def generateDescription(search):
  #Se lee del archivo .env la api key de openai
  _ = load_dotenv('.env')

  def get_completion(prompt, model="gpt-3.5-turbo"):
      messages = [{"role": "user", "content": prompt}]
      response = openai.ChatCompletion.create(
          model=model,
          messages=messages,
          temperature=0,
      )
      return response.choices[0].message["content"]

  instruction = "Vas a actuar como un aficionado del cine que sabe describir de forma clara, concisa y precisa \
  cualquier película en menos de 200 palabras. La descripción debe incluir el género de la película y cualquier \
  información adicional que sirva para crear un sistema de recomendación."

  movie = search
  prompt = f"{instruction} Has una descripción de la película {movie}"

  response = get_completion(prompt)

  return response

def generateImage(search):
    #Se lee del archivo .env la api key de openai
  _ = load_dotenv('openAI.env')



  #Se hace la conexión con la API de generación de imágenes. El prompt en este caso es:
  #Alguna escena de la película + "nombre de la película"
  response = openai.Image.create(
    prompt=f"Alguna escena de la película {search}",
    n=1,
    size="256x256"
  )
  
  image_url = response['data'][0]['url']

  # La API devuelve la url de la imagen, por lo que debemos generar una función auxiliar que
  # descargue la imagen.
  def fetch_image(url):
      response = requests.get(url)
      response.raise_for_status()

      # Convert the response content into a PIL Image
      image = Image.open(BytesIO(response.content))
      return(image)


  return image_url
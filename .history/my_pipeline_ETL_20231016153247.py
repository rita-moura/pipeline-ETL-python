import os
import pandas as pd
import openai
from dotenv import load_dotenv

load_dotenv()

openai.organization = "org-haoEXv47DvV6WA4p8QSlmZAT"
openai.api_key = os.getenv("OPENAI_API_KEY")
openai.Model.list()

if openai.api_key is None:
    raise EnvironmentError("A chave da API da OpenAI não foi encontrada. Verifique seu arquivo config.env.")

df = pd.read_csv("artist_name.csv")
name_artist = df['name'].tolist()
print(name_artist)

for artist in name_artist:
    print(artist)

def generate_ai_text(name):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {
          "role": "system",
          "content": "Você é especialista em artistas da música mundial"
      },
      {
          "role": "name",
          "content": f"Crie uma mensagem sobre o artista {name} contando qual foi sua maior obra (máximo de 100 caracteres)"
      }
    ]
    )
  return completion.choices[0].message.content.strip('\"')

for artist in name_artist:
    message = generate_ai_text(artist);
    print(message)

def update_artist(name):
  artist_index = df[df['name'] == name['name']].index[0]
  df.loc[artist_index] = name

  return True

artists = pd.read_csv("artist_name.csv").to_dict('records')

for artist in artists:
  success = update_artist(artist)
  print(f"Artista {artist['name']} updated? {success}!")
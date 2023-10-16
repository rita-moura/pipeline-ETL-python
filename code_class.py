import os
import pandas as pd
import requests
import json
import openai
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")
sdw2023_api_url = "https://sdw-2023-prd.up.railway.app"

if openai.api_key is None:
    raise EnvironmentError("A chave da API da OpenAI não foi encontrada. Verifique seu arquivo config.env.")

df = pd.read_csv("clients_ids.csv")
user_ids = df['UserID'].tolist()
print(user_ids)

def get_user(id):
  response = requests.get(f'{sdw2023_api_url}/users/{id}')
  return response.json() if response.status_code == 200 else None

users = [user for id in user_ids if (user := get_user(id)) is not None]
print(json.dumps(users, indent=2))

def generate_ai_news(user):
  completion = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
      {
          "role": "system",
          "content": "Você é um especialista em markting bancário."
      },
      {
          "role": "user",
          "content": f"Crie uma mensagem para {user['name']} sobre a importância dos investimentos (máximo de 100 caracteres)"
      }
    ]
    )
  return completion.choices[0].message.content.strip('\"')

for user in users:
  news = generate_ai_news(user)
  print(news)
  user['news'].append({
      "icon": "https://digitalinnovationone.github.io/santander-dev-week-2023-api/icons/credit.svg",
      "description": news
  })

def update_user(user):
  response = requests.put(f"{sdw2023_api_url}/users/{user['id']}", json=user)
  return True if response.status_code == 200 else False

for user in users:
  success = update_user(user)
  print(f"User {user['name']} updated? {success}!")
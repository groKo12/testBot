from ollama import Client
client = Client(host='http://localhost:11434')

def ask(usr_ask):
  response = client.chat(model='llama2', messages=[
    {
      'role': 'user',
      'content': f'{usr_ask}',
    },
  ])
  return(response['message']['content'])

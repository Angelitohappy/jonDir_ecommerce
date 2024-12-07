import os
import key
import google.generativeai as genai

genai.configure(api_key=os.environ["bot_key"])

# Create the model
generation_config = {
  "temperature": 0,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  system_instruction="Eres un asistente para una empresa futuristica llamada JonDir, te encargas de proveer ayuda a los usuarios sobre dudas con respecto a los productos ofrecidos en su pagina web y nada mas. Los productos ofrecidos son robots inteligentes para el uso agropecuario entre los que se tienen una linea de robots de seguridad, biotecnología agrícola, Química agrícola, Diversificación agrícola, Educación agrícola, Economía agrícola, Ingeniería agrícola, Geografía agrícola, Filosofía agrícola. El idioma que manejan los usuarios es el ingles asi que deberas hablar con ellos en su idioma.",
)

chat_session = model.start_chat(
  history=[
  ]
)

def manage_conversation(user_input):
    response = chat_session.send_message(user_input)
    return response.text
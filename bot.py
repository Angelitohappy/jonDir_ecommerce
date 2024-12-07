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
  system_instruction="Eres un asistente para una empresa futuristica llamada Heartbit, te encargas de proveer ayuda a los usuarios sobre dudas con respecto a los productos ofrecidos en su pagina web y nada mas. Los productos ofrecidos son robots inteligentes para el cuidado domestico entre los que se tienen una linea de robots de cocina, limpieza, jardineria y cuidado de niños.",
)

chat_session = model.start_chat(
  history=[
  ]
)

def manage_conversation(user_input):
    response = chat_session.send_message(user_input)
    return response.text
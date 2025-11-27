import openai
import pandas as pd


class GPT41Client:
    def __init__(self, api_key):
        self.client = openai.OpenAI(
            api_key=api_key,
            timeout=54000
        )
    
    def query(self, prompt, temperature=0.1):
        response = self.client.chat.completions.create(
            model="gpt-4.1",  # LM Studio usa este nombre por defecto
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content
       


if __name__ == "__main__":
    
    api_key = "your_api_key"
    client = GPT41Client(api_key)

    class_name = "normal"
    experimento_1 = pd.read_csv('route to a class explanations/explicaciones_{class_name}.csv')
    #experimento_1 = experimento_1[0:5]
    labels = [] # En esta lista guardaremos las etiquetas obtenidas
    #test['Explanations'].values[0]
    for index, row in experimento_1.iterrows():
            # Creamos el prompt
            input_string = (
            f"I have a network flow labeler that assigns flows to one of the following categories:\n\n"
            f"\"normal\" : No attack, normal flow\n"
            f"\"dos\" : denial of service attack\n"
            f"\"portScan\": Port Scan attack\n"
            f"\"bruteForce\": Bruteforce attack\n"
            f"\"pingScan\": Ping Scan attack\n\n"
            f"Next, I will give you 100 explanations of flows that were classified as \"{class_name}\". I want you to provide me with a summary of these explanations that allows me to consider as many relevant factors as possible when classifying flows.\n"
            f"The summary must be in plain text, written in paragraphs, without using bullet points or tables.\n"
            f"{row['Explanations']}\"\n"
            
        )
           
            try:
                label = client.query(input_string)  # Realizamos la consulta
                labels.append(label)   # Agregamos la etiqueta a la lista
                
            except Exception as e:
                print(f"Error en la consulta: {e}")
                

            # Guardar el progreso después de cada iteración
            resultados = pd.DataFrame(labels, columns=['Explicacion'])
            resultados.to_csv('/home/ivan/Desktop/CIDDS/explicacion_gpt41_simple_resumen_normal.csv', index=False)

            print(f"Procesado {index+1}/{len(experimento_1)}")

    print("Procesamiento completado.")

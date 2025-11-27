import openai
import pandas as pd


class GPT41Client:
    def __init__(self, api_key):
        self.client = openai.OpenAI(
            api_key=api_key,
            timeout=54000
        )
    
    def query(self, prompt, temperature=0.2):
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

    
    experimento_1 = pd.read_csv('route to data train/CIDDS_sample_train.csv')
    experimento_1 = experimento_1.groupby('attackType').apply(lambda x: x.sample(n=100, random_state=42)).reset_index(drop=True)
    labels = [] # En esta lista guardaremos las etiquetas obtenidas
    
    for index, row in experimento_1.iterrows():
            # Creamos el prompt
            input_string = (
            f"I have a network flow with the following attributes::\n"
            f"Date first seen (Start time flow first seen) : {row['Date first seen']}\n"
            f"Duration (Duration of the flow) : {row['Duration']}\n"
            f"Proto (Transport protocol (e.g. ICMP, TCP, or UDP)) : {row['Proto']}\n"
            f"Src IP (Source IP address) : {row['Src IP Addr']}\n"
            f"Src port (Source port) : {row['Src Pt']}\n"
            f"Dest IP (Destination IP) : {row['Dst IP Addr']}\n"
            f"Dest port (Destination port) : {row['Dst Pt']}\n"
            f"Packets (Number of transmitted packets) : {row['Packets']}\n"
            f"Bytes (Number of transmitted bytes) : {row['Bytes']}\n"
            f"Flags (concatenation of all TCP Flags, U (URG), A (ACK), P (PSH), R (RST), S(SYN), F(FIN)) : {row['Flags']}\n\n"
            f"This flow can be classified in one of these five possible labels that represent types of cyber attacks:\n\n"
            f"\"---\" : No attack, normal flow\n"
            f"\"dos\" : denial of service attack\n"
            f"\"portScan\": Port Scan attack\n"
            f"\"bruteForce\": Bruteforce attack\n"
            f"\"pingScan\": Ping Scan attack\n\n"
            f"This network flow was classified as: \"{row['attackType']}\", and I need an explanation of why it was classified that way\n"
            
        )
           
            try:
                label = client.query(input_string)  # Realizamos la consulta
                labels.append((index, row['attackType'], label))   # Agregamos la etiqueta a la lista
                
            except Exception as e:
                print(f"Error en la consulta: {e}")
                labels.append((index, row['attackType'], "error"))

            # Guardar el progreso después de cada iteración
            resultados = pd.DataFrame(labels, columns=['ID', 'attackType', 'Explicacion'])
            resultados.to_csv('route to save the explanations', index=False)

            print(f"Procesado {index+1}/{len(experimento_1)}")
    
    print("Procesamiento completado y etiquetas guardadas'.")

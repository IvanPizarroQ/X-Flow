import openai
import pandas as pd
import time
import numpy as np

class GPT41Client:
    def __init__(self, api_key):
        self.client = openai.OpenAI(
            api_key=api_key,
            timeout=18000
        )
    
    def query(self, prompt, temperature=0):
        response = self.client.chat.completions.create(
            model="gpt-4.1",  # LM Studio usa este nombre por defecto
            messages=[
                {"role": "system", "content": "You are a network flow classifier."},
                {"role": "user", "content": prompt}
            ],
            temperature=temperature
        )
        return response.choices[0].message.content

if __name__ == "__main__":
    api_key = "your api key"
    client = GPT41Client(api_key)
    seeds = range(42, 52)  # 42 to 51 inclusive
    explicacion_normal = pd.read_csv('/route to global class explanations/explicacion_gpt41_resumen_normal.csv')
    explicacion_dos = pd.read_csv('/route to global class explanations/explicacion_gpt41_resumen_dos.csv')
    explicacion_portScan = pd.read_csv('/route to global class explanations/explicacion_gpt41_resumen_portscan.csv')
    explicacion_bruteForce = pd.read_csv('/route to global class explanations/explicacion_gpt41_resumen_bruteForce.csv')
    explicacion_pingScan = pd.read_csv('/route to global class explanations/explicacion_gpt41_resumen_pingscan.csv')
    for seed in seeds:
        input_file = f'/route to validation set/validation_set_seed{seed}.csv'
        output_file = f'/route to save predictions/etiquetas_gpt41_megaprompt_seed{seed}.csv'
        experimento_1 = pd.read_csv(input_file)
        labels = []
        tiempos = []

        for idx, row in experimento_1.iterrows():
            input_string = (
            f"I have a network flow labeler that assigns flows to one of the following categories:\n\n"
            f"\"normal\" : No attack, normal flow\n"
            f"\"dos\" : denial of service attack\n"
            f"\"portScan\": Port Scan attack\n"
            f"\"bruteForce\": Bruteforce attack\n"
            f"\"pingScan\": Ping Scan attack\n\n"
            f"Next, I will give you explanations of the labels.\n"
            f"Explanations for \"normal\" flows: {explicacion_normal['Explicacion'].values[0]}\n"
            f"Explanations for \"dos\" flows: {explicacion_dos['Explicacion'].values[0]}\n"
            f"Explanations for \"portScan\" flows: {explicacion_portScan['Explicacion'].values[0]}\n"
            f"Explanations for \"bruteForce\" flows: {explicacion_bruteForce['Explicacion'].values[0]}\n"
            f"Explanations for \"pingScan\" flows: {explicacion_pingScan['Explicacion'].values[0]}\n\n"
            f"Now, I will give you a new network flow with the following attributes:\n\n"
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
            f"I need this flow to be classified in one of the five possible labels that represent types of cyber attacks\n\n"
            f"As a response, I need you to give me only the label, using the format: Label:\n"
            )
            start_time = time.time()
            label = client.query(input_string)
            end_time = time.time()
            infer_time = end_time - start_time
            tiempos.append(infer_time)
            labels.append(label)
            print(f"Seed {seed} - Procesado {idx+1}/{len(experimento_1)}")

    tiempo_promedio = sum(tiempos) / len(tiempos) if tiempos else 0
    tiempo_std = np.std(tiempos) if tiempos else 0
    print(f"Procesamiento completado y etiquetas guardadas para seed {seed}")
    print(f"Tiempo promedio de inferencia para seed {seed}: {tiempo_promedio:.2f} segundos")
    print(f"Desviación estándar del tiempo de inferencia para seed {seed}: {tiempo_std:.2f} segundos")

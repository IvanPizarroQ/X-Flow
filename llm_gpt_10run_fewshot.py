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
        return response.choices[0].message.content, response.usage.prompt_tokens

if __name__ == "__main__":
    api_key = "your api key"
    client = GPT41Client(api_key)
    seeds = range(42, 52)  # 42 to 51 inclusive

    for seed in seeds:
        input_file = f'/route to validation set/experimento0_desbalanceado_sin_labels_seed{seed}.csv'
        train_file = f'/route to train set/experimento0_desbalanceado_train.csv'
        output_file = f'/route to save predictions/etiquetas_gpt41_fewshot_seed{seed}.csv'
        experimento_1 = pd.read_csv(input_file)
        train_df = pd.read_csv(train_file)
        train_df["attackType"] = train_df["attackType"].replace('---', 'normal')
        # Selecciona 6 ejemplos por clase
        fewshot_examples = []
        for clase in ["normal", "dos", "portScan", "bruteForce", "pingScan"]:
            ejemplos_clase = train_df[train_df["attackType"] == clase].sample(n=6, random_state=seed)
            for _, ej in ejemplos_clase.iterrows():
                fewshot_examples.append(
                    f" Input: \n Date first seen (Start time flow first seen): {ej['Date first seen']} \n Duration (Duration of the flow): {ej['Duration']} \n Proto (Transport protocol (e.g. ICMP, TCP, or UDP)): {ej['Proto']} \n Src IP (Source IP address): {ej['Src IP Addr']}\n Src port (Source port): {ej['Src Pt']}\n Dest IP (Destination IP): {ej['Dst IP Addr']}\n Dest port (Destination port): {ej['Dst Pt']}\n Packets (Number of transmitted packets): {ej['Packets']}\n Bytes (Number of transmitted bytes): {ej['Bytes']}\n Flags (concatenation of all TCP Flags, U (URG), A (ACK), P (PSH), R (RST), S(SYN), F(FIN)): {ej['Flags']} \n\n Label: {ej['attackType']}\n\n"
                )
        fewshot_prompt = "Here are some labeled examples:\n" + "\n".join(fewshot_examples) + "\n\n"
        labels = []
        tiempos = []
        for idx, row in experimento_1.iterrows():
            input_string = (
                fewshot_prompt +
                f"Now have a network flow with the following attributes:\n"
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
                f"I need this flow to be classified in one of these five possible labels that represent types of cyber attacks:\n\n"
                f"\"normal\" : No attack\n"
                f"\"dos\" : denial of service attack\n"
                f"\"portScan\": Port Scan attack\n"
                f"\"bruteForce\": Bruteforce attack\n"
                f"\"pingScan\": Ping Scan attack\n"
                f"As a response, I need you to give me only the label, using the format: Label:\n"
            )
            start_time = time.time()
            label, input_tokens = client.query(input_string)
            end_time = time.time()
            infer_time = end_time - start_time
            tiempos.append(infer_time)
            labels.append(label)
            print(f"Seed {seed} - Procesado {idx+1}/{len(experimento_1)}")
            print(f"Tokens de entrada: {input_tokens}")

        resultados = pd.DataFrame({'Etiquetas': labels})
        resultados.to_csv(output_file, index=False)
        print(f"Procesamiento completado y etiquetas guardadas para seed {seed}")
    tiempo_promedio = sum(tiempos) / len(tiempos) if tiempos else 0
    tiempo_std = np.std(tiempos) if tiempos else 0
    print(f"Procesamiento completado y etiquetas guardadas para seed {seed}")
    print(f"Tiempo promedio de inferencia para seed {seed}: {tiempo_promedio:.2f} segundos")
    print(f"Desviación estándar del tiempo de inferencia para seed {seed}: {tiempo_std:.2f} segundos")

from afd import gerar_afd
afd, simbolos, dict_simbolos, estados_finais = gerar_afd()
ESTADO_ATUAL_AL = '0'
FITA = []
TOKEN = ''
TS = []
caminho_atual = ['0']
print(f"\nALFABETO: {simbolos} \nMAPEAMENTO: {dict_simbolos} \nESTADO FINAL: {estados_finais}")
with open('entrada.txt', 'r') as file:
    for num_linha, line in enumerate(file):
        for char in line:
            if char != ' ' and char != '\n':
                if char not in simbolos:
                    ESTADO_ATUAL_AL = '~'
                    caminho_atual.append('~')
                    TOKEN+=char
                else:
                    posicao = dict_simbolos[char]
                    aux = afd[ESTADO_ATUAL_AL][posicao]
                    ESTADO_ATUAL_AL = aux
                    caminho_atual.append(ESTADO_ATUAL_AL)
                    TOKEN+=char
            else:
                FITA.append(ESTADO_ATUAL_AL)
                string_caminho = " -> ".join(caminho_atual)

                if ESTADO_ATUAL_AL in estados_finais:
                    string_caminho = string_caminho.replace(ESTADO_ATUAL_AL, f"*{ESTADO_ATUAL_AL}")
                if ESTADO_ATUAL_AL in estados_finais:
                    ts_token = {
                        'token': TOKEN,
                        'linha': num_linha,
                        'status': 'aceito',
                        'caminho': string_caminho
                    }
                    TS.append(ts_token)
                    TOKEN = ''
                elif ESTADO_ATUAL_AL == '~':
                    ts_token = {
                        'token': TOKEN,
                        'linha': num_linha,
                        'status': 'ERRO',
                        'caminho': string_caminho
                    }
                    TS.append(ts_token)
                    TOKEN = ''
                ESTADO_ATUAL_AL = '0'
                caminho_atual = ['0']

print("\n--- TABELA DE SÍMBOLOS ---")
print(f"{'ENTRADA':<9} | {'LINHA':<5} | {'RÓTULO':<6} | {'SEQUENCIA DE ESTADOS'}")
print("-" * 86)
for item in TS:
    print(f"{item['token']:<9} | {item['linha']:<5} | {item['status']:<6} | {item['caminho']}")

print("\n--- FITA DE SAÍDA ---")
print(" ".join(FITA))
print("\n")
                    
                    
                    


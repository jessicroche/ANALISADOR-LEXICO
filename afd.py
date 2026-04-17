import os

# Constantes globais
ESTADO_INICIAL = 0
PROX_ESTADO_LIVRE = 0

# Funções de impressão
def imprimir_afnd(simbolos: list, afnd: list, finais: list) -> None:
    print("\n============================= AFND =============================")
    print("\t\t" + "\t\t".join(simbolos))
    print("->", end='')

    for r, row in enumerate(afnd):
        celula = f"*{r}" if r in finais else str(r)
        print(f"{celula}\t\t" + "\t\t".join(cell for cell in row))
        print("-----------------"*len(simbolos))


def imprimir_afd(simbolos: list, afd: dict, finais: list) -> None:
    print("\n============================= AFD =============================")
    print("\t\t" + "\t\t".join(simbolos))
    print("->", end='')
    celula = f"*0" if '0' in finais else '0'
    print(f"{celula}\t\t" + "\t\t".join(f"[{cell}]" if ',' in cell else cell for cell in afd['0']))
    print("-----------------"*len(simbolos))
    for key, values in afd.items():
        if key != 'S':
            chave_composta = f"[{key}]" if ',' in key else key
            celula = f"*{chave_composta}" if key in finais else chave_composta
            print(f"{celula}\t\t" + "\t\t".join(f"[{cell}]" if ',' in cell else cell for cell in values))
            print("-----------------"*len(simbolos))
        

# Processar uma palavra e inseri-la na AFND
def processar_palavra(line, dict_simbolos, afnd, estados_finais, tokens_estados):
    global PROX_ESTADO_LIVRE
    eh_simbolo_inicial = True

    for char in line:
        if char != ' ' and char !="\n":
            if eh_simbolo_inicial:
                estado_atual = ESTADO_INICIAL
            else:
                estado_atual = PROX_ESTADO_LIVRE

            if char in dict_simbolos:
                idx = dict_simbolos[char]
                if afnd[estado_atual][idx] == "":
                    afnd[estado_atual][idx] = str(PROX_ESTADO_LIVRE + 1)
                else:
                    afnd[estado_atual][idx] += "," + str(PROX_ESTADO_LIVRE + 1)
                PROX_ESTADO_LIVRE += 1

            eh_simbolo_inicial = False

        elif char == '\n':
            estados_finais.add(PROX_ESTADO_LIVRE)
            nova_linha_estado_final = [''] * len(dict_simbolos)
            tokens_estados[PROX_ESTADO_LIVRE] = line.replace("\n","")
            afnd.append(nova_linha_estado_final)

    if not line.endswith('\n'):
        tokens_estados[PROX_ESTADO_LIVRE] = line
        estados_finais.add(PROX_ESTADO_LIVRE)
        nova_linha_estado_final = [''] * len(dict_simbolos) 
        afnd.append(nova_linha_estado_final)

# Processar uma regra de uma GR e inseri-la na AFND
def processar_gramatica(line, dict_estados, dict_simbolos, afnd, estados_finais):
    global PROX_ESTADO_LIVRE
    line_no_space = line.replace(" ","").replace("<",'').replace(">",'').strip()
    nome_regra = line_no_space.split("::=")[0]
    producoes = (line_no_space.replace(f"{nome_regra}::=", '')).split("|")
    for p in producoes:
        # Casos do tipo aA
        if any(c.isupper() for c in p):
            if dict_estados[p[1]] == -1:
                dict_estados[p[1]] = PROX_ESTADO_LIVRE + 1
                PROX_ESTADO_LIVRE = PROX_ESTADO_LIVRE+1
            if afnd[dict_estados[nome_regra]][dict_simbolos[p[0]]] == "":
                afnd[dict_estados[nome_regra]][dict_simbolos[p[0]]] = str(dict_estados[p[1]])
            else:
                afnd[dict_estados[nome_regra]][dict_simbolos[p[0]]] += ","+str(dict_estados[p[1]])
        # Epsilon produção
        elif "*" in p:
            for i, s in enumerate(afnd[dict_estados[nome_regra]]):
                estados_finais.add(dict_estados[nome_regra])
                if s == "":
                    afnd[dict_estados[nome_regra]][i] = ""
        # Somente um terminal
        else:
            PROX_ESTADO_LIVRE = PROX_ESTADO_LIVRE + 1
            if afnd[dict_estados[nome_regra]][dict_simbolos[p[0]]] == "":
                afnd[dict_estados[nome_regra]][dict_simbolos[p[0]]] = str(PROX_ESTADO_LIVRE)
            else:
                afnd[dict_estados[nome_regra]][dict_simbolos[p[0]]] += ","+ str(PROX_ESTADO_LIVRE)
            estados_finais.add(PROX_ESTADO_LIVRE)
            nova_linha_estado_final = [''] * len(dict_simbolos) 
            nova_linha = [''] * len(dict_simbolos) 
            afnd.append(nova_linha)  
            afnd[PROX_ESTADO_LIVRE] = nova_linha_estado_final

# Determinizar uma AFND transformando-a em uma AFD
def determinizar_afnd(afd,afnd, estados):
    if estados == []: return
    novos_estados = []

    for estado in estados:
            for novo_estado in afd[estado]:
                if novo_estado!='':
                    if novo_estado not in afd.keys():
                        novos_estados.append(novo_estado)
                        if "," in novo_estado:
                            transicoes = [''] * len(afd[estado]) 
                            for c in novo_estado.split(","):
                                    for i, estado_t in enumerate(afnd[int(c)]):
                                        if estado_t != '':
                                            if transicoes[i] == '':
                                                transicoes[i] = estado_t
                                            else:
                                                transicoes[i] += ","+estado_t
                            afd[novo_estado] = transicoes
                        else:
                            if novo_estado not in afd:
                                afd[novo_estado] = afnd[int(novo_estado)]
            determinizar_afnd(afd, afnd,novos_estados)

# Gerar a AFND com base nas palavras e regras do arquivo tokens.txt
def gerar_afnd(simbolos, count_simbolos, dict_estados, dict_simbolos, estados_finais):
    tokens_estado = {}
    afnd = [["" for _ in range(len(simbolos))] for _ in range(count_simbolos)]

    # Processamento de arquivo
    with open("tokens.txt", "r") as tokens:
        for line in tokens:
            if "::" in line:
                processar_gramatica(line, dict_estados, dict_simbolos, afnd, estados_finais)
            else:
                processar_palavra(line, dict_simbolos, afnd, estados_finais, tokens_estado)

    # imprimir_afnd(simbolos, afnd, estados_finais)
    # print(f"Final dos tokens: {tokens_estado}")
    # print(f"Estados finais da AFND: {estados_finais}")

    return afnd

# Transformar o nome dos estados de inteiros para letras maiúsculas
def renomear_estados_letras(dict_estados, afnd, afd:dict):
    # Mapeamento de estados e renomeação
    mapa_final_estados = {str(v): k for k, v in dict_estados.items()}
    ultimos = sorted([k for k in dict_estados if k != 'S'])
    proxima_letra = ord(ultimos[-1]) if ultimos else ord('A')

    # Usa a AFND pois nela o nome dos estados é somente um único inteiro
    for num_linha in range(len(afnd)):
        if str(num_linha) not in mapa_final_estados:
            while chr(proxima_letra) in dict_estados:
                proxima_letra += 1
            novo_nome = chr(proxima_letra)
            mapa_final_estados[str(num_linha)] = novo_nome
            dict_estados[novo_nome] = num_linha
            proxima_letra += 1

    # Substituição de estados por letras na AFD
    for valor in afd.values():
        for i, cell in enumerate(valor):
            if cell !='':
                if "," in cell:
                    nomes = ",".join(mapa_final_estados[e] for e in cell.split(","))
                    valor[i] = f"{nomes}"
                else:
                    valor[i] = mapa_final_estados[cell]
    
    # Renomear chaves da AFD
    for chave in list(afd.keys()):
        if "," in chave:
            nomes = ",".join(mapa_final_estados[e] for e in chave.split(","))
            afd[f"{nomes}"] = afd.pop(chave)
        else:
            afd[mapa_final_estados[chave]] = afd.pop(chave)


def gerar_afd():
    global PROX_ESTADO_LIVRE

    if not os.path.exists("tokens.txt"):
        print("Erro ao abrir arquivo de tokens")
        return
    
    # Coleta de símbolos
    with open("tokens.txt","r") as tokens:
        simbolos = set()
        for line in tokens:
            for char in line.strip():
                if char != ' ' and char not in {':', '<', '>', '=', '|', '*', '\n'} and not char.isupper():
                    simbolos.add(char)
    simbolos = sorted(simbolos)
    dict_simbolos = {s: i for i, s in enumerate(simbolos)}

    # Contagem de estados e configuração inicial
    count_simbolos = sum(len(line.replace("\n",'').strip()) for line in open("tokens.txt") if ("::" not in line))
    uppercase_letters = {
        char for line in open("tokens.txt") for char in line.strip() if char.isupper()
    }

    count_simbolos = count_simbolos + len(uppercase_letters) -1 if count_simbolos !=0 else count_simbolos + len(uppercase_letters)
    dict_estados = {u: -1 for u in uppercase_letters}
    dict_estados["S"] = 0

    estados_finais = set()
    
    afnd = gerar_afnd(simbolos, count_simbolos, dict_estados, dict_simbolos, estados_finais)
    imprimir_afnd(simbolos, afnd, estados_finais)

    # Determinização
    afd = {'0': [cell for cell in afnd[0]]}
    determinizar_afnd(afd, afnd, list(afd.keys()))
    #renomear_estados_letras(dict_estados, afnd, afd)

    # Ajuste de estados finais
    novos_estados_finais = []
    for estados in afd.keys():
        if "," in estados:
            for estado in estados.split(","):
                if int(estado) in estados_finais:
                    novos_estados_finais.append(estados)
                    break
        else:
            if int(estados) in estados_finais:
                novos_estados_finais.append(estados)

    estados_finais = set(novos_estados_finais)

    estado_de_erro = ['~'] * len(simbolos)
    afd['~'] = estado_de_erro
    for values in afd.values():
       for i, cell in enumerate(values):
            values[i] = cell if cell else "~" 
    imprimir_afd(simbolos, dict(sorted(afd.items())), estados_finais)
    #print(afd)
    return afd, simbolos, dict_simbolos, estados_finais
if __name__ == "__main__":
    gerar_afd()
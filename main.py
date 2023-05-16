from collections import deque


def fifo(page_references, num_frames):
    frames = deque(maxlen=num_frames)  # Cria uma fila com tamanho máximo igual ao número de quadros
    page_faults = 0  # Variável para contar as faltas de página

    for page in page_references:
        if page not in frames:  # Verifica se a página está nos quadros
            page_faults += 1  # Incrementa o contador de faltas de página

            if len(frames) == num_frames:  # Verifica se a fila de quadros está cheia
                frames.popleft()  # Remove o quadro mais antigo da fila

            frames.append(page)  # Adiciona a página atual à fila de quadros

    return page_faults


# Implementação do algoritmo Ótimo
def optimal(page_references, num_frames):
    frames = [-1] * num_frames  # Cria uma lista de quadros vazios
    page_faults = 0  # Variável para contar as faltas de página
    page_indices = {}  # Dicionário para armazenar o índice da página no conjunto de referências
    page_index = 0

    for i, page in enumerate(page_references):
        if page not in frames:  # Verifica se a página está nos quadros
            page_faults += 1  # Incrementa o contador de faltas de página

            if -1 in frames:  # Verifica se há quadros vazios
                frame_index = frames.index(-1)  # Encontra o índice do primeiro quadro vazio
            else:
                future_references = page_references[i:]  # Referências futuras a partir do índice atual
                for frame in frames:
                    if frame not in future_references:  # Verifica se o quadro não será referenciado no futuro
                        frame_index = frames.index(frame)
                        break
                    else:
                        frame_index = future_references.index(frames[0])  # Se todos forem referenciados, substitui o primeiro

            frames[frame_index] = page  # Substitui o quadro na posição encontrada pela nova página

        if page not in page_indices:  # Armazena o índice da página se não existir no dicionário
            page_indices[page] = page_index
            page_index += 1

    return page_faults


def lru(page_references, num_frames):
    frames = []  # Lista para armazenar os quadros
    page_faults = 0  # Variável para contar as faltas de página
    page_indices = {}  # Dicionário para armazenar o índice da página no conjunto de referências
    page_index = 0

    for page in page_references:
        if page not in frames:  # Verifica se a página está nos quadros
            page_faults += 1  # Incrementa o contador de faltas de página

            if len(frames) == num_frames:  # Verifica se a lista de quadros está cheia
                oldest_page_index = min(page_indices.values())  # Encontra o índice da página mais antiga
                oldest_page = next(
                    key for key, value in page_indices.items() if value == oldest_page_index
                )# Encontra a página correspondente ao índice mais antigo
                frames.remove(oldest_page) # Remove a página mais antiga dos quadros
                page_indices.pop(oldest_page) # Remove a página mais antiga do dicionário
                

            frames.append(page)# Adiciona a página atual à lista de quadros

        if page not in page_indices: # Armazena o índice da página se não existir no dicionário
            page_indices[page] = page_index
            page_index += 1
        else:
            page_indices[page] = page_index
            page_index += 1

    return page_faults


# Leitura do arquivo
filename = "arquivo.txt"
try:
    with open(filename, "r") as file:
        lines = file.readlines()

        # Primeira linha contém o número de quadros de memória disponíveis
        num_frames = int(lines[0])

        # Demais linhas contêm as referências às páginas
        page_references = [int(line.strip()) for line in lines[1:]]

        # Cálculo das faltas de página
        fifo_faults = fifo(page_references, num_frames)
        optimal_faults = optimal(page_references, num_frames)
        lru_faults = lru(page_references, num_frames)

        # Impressão dos resultados
        print("FIFO", fifo_faults)
        print("OTM", optimal_faults)
        print("LRU", lru_faults)

except FileNotFoundError:
    print("Arquivo não encontrado.")

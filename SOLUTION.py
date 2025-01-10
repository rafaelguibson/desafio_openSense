import os
import re
from bs4 import BeautifulSoup
"""
Passo a passo da solução:
1 - Acessar a pasta /PATENTES
2 - Percorrer cada Arquivo HTML
3 - Verificar Se o arquivo contém ou não Registros
    • 3.1 Se sim: 
        - Pegar o dado do CNPJ.
        - Percorrer a tabela de registro de patentes adicionando eles a lista.
        - Retornar a lista de Registros.
    • 3.2 Se não:
        - Pegar o dado do CNPJ.
        - Preencher demais colunas daquele registro com  -
4 - Gerar tabela em arquivo HTML a partir da lista de registros gerada.
"""

# Definição do caminho da pasta do desafio.
path_to_patentes = "./PATENTES"

# Definição do nome do arquivo de saída
output_file = "PATENTES.HTML"

# Função  para processar os arquivos HTML no diretório especificado.
# Executa passo 2 e 3.
def process_patente_files(directory):
    registros = []

    # Percorre todos os arquivos no diretório fornecido
    for filename in os.listdir(directory):
        # Processa apenas arquivos com extensão .html
        if filename.endswith(".html"):
            file_path = os.path.join(directory, filename)

            with open(file_path, "r", encoding="ISO-8859-1") as file:
                content = file.read()
                # Uso da Biblioteca BeautifulSoup para leitura e manipulação dos arquivos HTML
                soup = BeautifulSoup(content, "html.parser")

                # Verificar se o arquivo contem a frase  "Nenhum resultado foi encontrado para a sua pesquisa"
                # O que significa que não há patentes no arquivo e preenche as demais colunas com -
                # Passo 3.2
                if "Nenhum resultado foi encontrado para a sua pesquisa" in content:
                    cnpj_match = re.search(r"CNPJ do Depositante: '(.+?)'", content)
                    cnpj = cnpj_match.group(1) if cnpj_match else "-"
                    registros.append([filename, cnpj, 0, "-", "-", "-", "-"])

                # Verificar se contém "Foram encontrados N processos que satisfazem à pesquisa."
                # Assim é um arquivo com registros de patentes.
                #Passo 3.1
                elif "Foram encontrados" in content:
                    #Extrai e trata o CNPJ do registro
                    cnpj_match = re.search(r"CNPJ do Depositante: '(.+?)'", content)
                    cnpj = cnpj_match.group(1) if cnpj_match else "-"

                    # Encontra todas as linhas da tabela que contêm os dados dos processos
                    # Raspando os dados pela tag TR que é das linhas da tabela.
                    processos = soup.find_all("tr", bgcolor=["#E0E0E0", "white"])
                    # Pega a quantidade de registros que a tabela contem para coluna resultado.
                    resultado = len(processos)

                    # Percorre as linhas da tabela pegando o registro de cada coluna e adicionando a lista de registros.
                    for processo in processos:
                        cols = processo.find_all("td")
                        if len(cols) == 4:
                            numero_pedido = cols[0].get_text(strip=True)
                            data_deposito = cols[1].get_text(strip=True)
                            titulo = cols[2].get_text(strip=True)
                            ipc = cols[3].get_text(strip=True)

                            registros.append([filename, cnpj, resultado, numero_pedido, data_deposito, titulo, ipc])

    return registros


# Gerar o arquivo de saída HTML
def generate_output_html(registros, output_path):
    """
    Esta função recebe os registros processados e cria um arquivo HTML formatado como tabela.
    Cada registro é uma linha na tabela, e as colunas incluem informações Nome do arquivo, CNPJ,
    resultado, número do pedido, data do depósito, título e IPC. O HTML gerado é salvo no caminho
    especificado por `output_path`.
    """
    with open(output_path, "w", encoding="ISO-8859-1") as file:
        # Início do arquivo HTML
        file.write("<html><head><title>Patentes</title></head><body>")

        # Nome dos Cabeçalhos da tabela
        file.write("<table border='1'>")
        file.write(
            "<tr>"
            "<th>Arquivo</th>"
            "<th>CNPJ</th>"
            "<th>Resultado</th>"
            "<th>Número do Pedido</th>"
            "<th>Data do Depósito</th>"
            "<th>Título</th>"
            "<th>IPC</th>"
            "</tr>"
        )

        # Laço para gerar as linhas da tabela
        for registro in registros:
            file.write("<tr>")
            #  Laço para preencher as colunas da tabela com a lista dos registros encontrados.
            for item in registro:
                file.write(f"<td>{item}</td>")
            file.write("</tr>")

        # Fechamento da tabela e do HTML
        file.write("</table>")
        file.write("</body></html>")


# Função principal para processar os arquivos e gerar o HTML
if __name__ == "__main__":
    registros = process_patente_files(path_to_patentes)
    generate_output_html(registros, output_file)
    print(f"Arquivo {output_file} gerado com sucesso!")

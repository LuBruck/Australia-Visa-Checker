import requests
from bs4 import BeautifulSoup
import time
import os

URL = "https://immi.homeaffairs.gov.au/what-we-do/whm-program/status-of-country-caps"
FILE_NAME = "brazil_status.txt"

def get_status():
    """Busca o status do Brasil e a data de atualização na página."""
    try:
        response = requests.get(URL)
        response.raise_for_status()  # Levanta um erro se a requisição falhar
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Encontra a tabela de países
        table = soup.find('table', {'class': 'responsive'})

        if not table:
            print("Tabela não encontrada. Verifique se a estrutura do site mudou.")
            return None, None
            
        # Encontra a linha (<tr>) que contém "Brazil"
        brazil_row = None
        for row in table.find_all('tr'):
            if row.find('td', string='Brazil'):
                brazil_row = row
                break
        
        if not brazil_row:
            print("Linha 'Brazil' não encontrada.")
            return None, None
            
        # Extrai as células (<td>) da linha
        cells = brazil_row.find_all('td')
        
        if len(cells) < 4:
            print("Estrutura da linha de dados para o Brasil é inesperada.")
            return None, None

        status = cells[1].text.strip()
        last_updated = cells[3].text.strip()

        return status, last_updated
        
    except requests.RequestException as e:
        print(f"Erro ao acessar a página: {e}")
        return None, None

def check_for_changes():
    """Verifica se o status ou a data de atualização mudaram."""
    current_status, current_last_updated = get_status()
    
    if current_status is None:
        print("Não foi possível obter os dados atuais. Tentando novamente mais tarde.")
        return

    # Tenta ler o status e a data anteriores do arquivo
    previous_status = None
    previous_last_updated = None
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, 'r') as f:
            lines = f.readlines()
            if len(lines) >= 2:
                previous_status = lines[0].strip()
                previous_last_updated = lines[1].strip()

    # Compara os dados
    if current_status != previous_status or current_last_updated != previous_last_updated:
        print("\n--- MUDANÇA DETECTADA! ---")
        print(f"Status anterior: {previous_status}")
        print(f"Novo status: {current_status}")
        print(f"Última atualização anterior: {previous_last_updated}")
        print(f"Nova última atualização: {current_last_updated}")
        print("--------------------------\n")

        # Salva o novo status para a próxima verificação
        with open(FILE_NAME, 'w') as f:
            f.write(f"{current_status}\n")
            f.write(f"{current_last_updated}\n")
    else:
        print("Nenhuma mudança detectada. O status e a data continuam os mesmos.")
        print(f"Status atual: {current_status}")
        print(f"Última atualização: {current_last_updated}")


if __name__ == "__main__":
    print("Iniciando monitoramento. Pressione Ctrl+C para parar.")
    # Loop infinito para checar a cada 10 minutos (600 segundos)
    try:
        while True:
            check_for_changes()
            print(f"\nPróxima checagem em 10 minutos...")
            time.sleep(600) 
    except KeyboardInterrupt:
        print("\nMonitoramento encerrado.")
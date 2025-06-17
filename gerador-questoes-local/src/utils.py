import os
import zipfile
from pathlib import Path

def display_banner_simple_green():
    """
    Simple ASCII art banner in green color.
    """
    GREEN = '\033[92m'
    RESET = '\033[0m'
    
    banner = f"""{GREEN}
 ___  ____    _    ____  
|_ _||___ \  / \  |___ \ 
 | |   __) |/ _ \   __) |
 | |  / __// ___ \ / __/ 
|___|_____/_/   \_\_____|
                        
      challenge 2       
{RESET}"""
    print(banner)

def extract_zip_files(zip_path: str, destination_dir: str) -> None:
    """
    Extrai arquivos de um .zip para o diretório de destino.
    
    Args:
        zip_path (str): Caminho do arquivo .zip.
        destination_dir (str): Diretório de destino para os arquivos extraídos.
    """
    try:
        os.makedirs(destination_dir, exist_ok=True)
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(destination_dir)
    except Exception as e:
        raise ValueError(f"Erro ao extrair o arquivo .zip: {e}")

def get_csv_path() -> str:
    """
    Solicita ao usuário o caminho do arquivo .zip e o nome do arquivo .csv,
    extrai o .zip e verifica a existência do .csv.

    Returns:
        str: Caminho completo do arquivo .csv extraído.

    Raises:
        ValueError: Se o arquivo .zip ou .csv não for encontrado ou for inválido.
    """
    try:
        
        # Apresenta display
        display_banner_simple_green()

        # Solicitar o caminho do arquivo .zip
        zip_path = input("Digite o caminho completo do arquivo .zip: ").strip()
        if not zip_path.lower().endswith('.zip'):
            raise ValueError("O arquivo fornecido não é um .zip válido.")
        if not os.path.exists(zip_path):
            raise ValueError(f"Arquivo .zip não encontrado: {zip_path}")

        # Solicitar o nome do arquivo .csv
        csv_name = input("Digite o nome do arquivo .csv a ser processado (ex: 202401_NFs_Itens.csv): ").strip()
        if not csv_name.lower().endswith('.csv'):
            csv_name += '.csv'  # Adicionar extensão se não fornecida

        # Definir diretório de destino para extração
        base_dir = "gerador-questoes-local/data"
        destination_dir = os.path.join(base_dir, "csv")
        os.makedirs(destination_dir, exist_ok=True)

        # Extrair o arquivo .zip
        print(f"Extraindo {zip_path} para {destination_dir}...")
        extract_zip_files(zip_path, destination_dir)

        # Construir o caminho completo do arquivo .csv
        csv_path = os.path.join(destination_dir, csv_name)

        # Verificar se o arquivo .csv existe
        if not os.path.exists(csv_path):
            raise ValueError(f"Arquivo .csv não encontrado: {csv_path}")

        print(f"Arquivo .csv encontrado: {csv_path}")
        return csv_path

    except Exception as e:
        raise ValueError(f"Erro ao processar entrada: {e}")
    
if __name__ == "__main__":
    pass
import zipfile
import os
from pathlib import Path

def extract_zip_files(source_dir: str, dest_dir: str):
    """
    Extrai todos os arquivos zip da pasta de origem para a pasta de destino
    """
    # Converte strings para objetos Path
    source_dir = Path(source_dir)
    dest_dir = Path(dest_dir)
    
    # Cria o diretório de destino se não existir
    dest_dir.mkdir(parents=True, exist_ok=True)
    
    # Verifica se o diretório de origem existe
    if not source_dir.exists():
        print(f"Erro: Diretório de origem '{source_dir}' não existe.")
        return
    
    # Encontra todos os arquivos zip no diretório de origem
    zip_files = list(source_dir.glob("*.zip"))
    
    if not zip_files:
        print(f"Nenhum arquivo zip encontrado em '{source_dir}'")
        return
    
    # Extrai cada arquivo zip
    for zip_path in zip_files:
        try:
            print(f"Extraindo {zip_path.name}...")
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                # Extrai todo o conteúdo para o diretório de destino
                zip_ref.extractall(dest_dir)
                
            print(f"✓ {zip_path.name} extraído com sucesso")
            
        except zipfile.BadZipFile:
            print(f"✗ Erro: {zip_path.name} não é um arquivo zip válido")
        except Exception as e:
            print(f"✗ Erro ao extrair {zip_path.name}: {str(e)}")
    
    print(f"\nExtração concluída. Arquivos extraídos para: {dest_dir}")

if __name__ == "__main__":
    pass
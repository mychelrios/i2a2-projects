
from processador_consultas_csv import *
from utils import *

def main():
    """
    Função principal para execução da solução de consulta interativa ao CSV.
    """

    print("\n" + "*"*50)
    print("INICIANDO SISTEMA DE CONSULTAS INTERATIVAS...")
    print("*"*50)

    caminho_completo_origem_arquivo_notas_fiscais_csv = get_csv_path()
   
    try:
        # Instanciar o processador de consultas
        processor = ProcessadorConsultasCSV(caminho_completo_origem_arquivo_notas_fiscais_csv)
        processor.run_interactive_shell()
    except Exception as e:
        print(f"Erro ao executar o sistema de consultas: {e}")

if __name__ == "__main__":
    main()
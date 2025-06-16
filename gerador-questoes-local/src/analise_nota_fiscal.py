
from processador_consultas_csv import *
from utils import *

# def main():
#     """
#     Função principal  para execução da solução.
#     """

#     # Extraindo os arquivos à partir de um arquivo comprimido no formato .zip
#     diretorio_origem_notas_fiscais_zip = "gerador-questoes-local/data/compressed"
#     diretorio_destino_notas_fiscais_csv = "gerador-questoes-local/data/csv"
#     diretorio_destino_perguntas_respostas_json = "gerador-questoes-local/result" 

#     arquivo_origem_notas_fiscais_csv = "202401_NFs_Itens.csv"
#     arquivo_destino_perguntas_respostas_json = "resultado_analise.json"

#     extract_zip_files(diretorio_origem_notas_fiscais_zip, diretorio_destino_notas_fiscais_csv)

#     # Instancia objeto CSVAnalyzer
#     analyzer = CSVAnalyzer(model_name="llama3")
    
#     # Caminho CSV
#     caminho_completo_origem_arquivo_notas_fiscais_csv = f"gerador-questoes-local/data/csv/{arquivo_origem_notas_fiscais_csv}"
    
#     if not os.path.exists(caminho_completo_origem_arquivo_notas_fiscais_csv):
#         print(f"Arquivo não encontrado: {caminho_completo_origem_arquivo_notas_fiscais_csv}")
#         print("Por favor, verifique o caminho do arquivo.")
#         return
   
#     # Generate questions and answers
#     print("\n" + "*"*50)
#     print("GERANDO PERGUNTAS E RESPOSTAS...")
#     print("*"*50)
    
#     perguntas_respostas = analyzer.generate_questions_and_answers()
    
#     if perguntas_respostas:
#         print("\nPERGUNTAS E RESPOSTAS GERADAS:")
#         print("*"*50)
        
#         for i, qa in enumerate(perguntas_respostas, 1):
#             print(f"\n{i}. PERGUNTA: {qa['pergunta']}")
#             print(f"   RESPOSTA: {qa['resposta']}")
        
#         # Save results
#         analyzer.save_results(perguntas_respostas, f"{diretorio_destino_perguntas_respostas_json}/{arquivo_destino_perguntas_respostas_json}")
        
#     else:
#         print("Não foi possível gerar perguntas e respostas.")

# if __name__ == "__main__":
#     main()


def main():
    """
    Função principal para execução da solução de consulta interativa ao CSV.
    """
    # Definir o caminho do arquivo CSV
        # Extraindo os arquivos à partir de um arquivo comprimido no formato .zip
    diretorio_origem_notas_fiscais_zip = "gerador-questoes-local/data/compressed"
    diretorio_destino_notas_fiscais_csv = "gerador-questoes-local/data/csv"

    arquivo_origem_notas_fiscais_csv = "202401_NFs_Itens.csv"

    extract_zip_files(diretorio_origem_notas_fiscais_zip, diretorio_destino_notas_fiscais_csv)
   
#     # Caminho CSV
#     caminho_completo_origem_arquivo_notas_fiscais_csv = f"gerador-questoes-local/data/csv/{arquivo_origem_notas_fiscais_csv}"

#     # Verificar se o arquivo existe
#     if not os.path.exists(caminho_completo_origem_arquivo_notas_fiscais_csv):
#         print(f"Arquivo não encontrado: {caminho_completo_origem_arquivo_notas_fiscais_csv}")
#         print("Por favor, verifique o caminho do arquivo.")
#         return

#     # Instanciar o processador de consultas
#     print("\n" + "*"*50)
#     print("INICIANDO SISTEMA DE CONSULTAS INTERATIVAS...")
#     print("*"*50)
    
#     try:
#         processor = ProcessadorConsultasCSV(caminho_completo_origem_arquivo_notas_fiscais_csv, model_name="mistral")
#         processor.run_interactive_shell()
#     except Exception as e:
#         print(f"Erro ao executar o sistema de consultas: {e}")

if __name__ == "__main__":
    main()
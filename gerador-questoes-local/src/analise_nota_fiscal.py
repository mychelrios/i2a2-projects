
from tratamento_nota_fiscal import *
from utils import *

def main():
    """
    Função principal  para execução da solução.
    """

    # Extraindo os arquivos à partir de um arquivo comprimido no formato .zip
    diretorio_origem_notas_fiscais_zip = "csv-question-generator/data/compressed"
    diretorio_destino_notas_fiscais_csv = "csv-question-generator/data/csv"
    diretorio_destino_perguntas_respostas_json = "csv-question-generator/result" 

    arquivo_origem_notas_fiscais_csv = "202401_NFs_Itens.csv"
    arquivo_destino_perguntas_respostas_json = "resultado_analise.json"

    extract_zip_files(diretorio_origem_notas_fiscais_zip, diretorio_destino_notas_fiscais_csv)

    # Instancia objeto CSVAnalyzer
    analyzer = CSVAnalyzer(model_name="llama3")
    
    # Caminho CSV
    caminho_completo_origem_arquivo_notas_fiscais_csv = f"csv-question-generator/data/csv/{arquivo_origem_notas_fiscais_csv}"
    
    if not os.path.exists(caminho_completo_origem_arquivo_notas_fiscais_csv):
        print(f"Arquivo não encontrado: {caminho_completo_origem_arquivo_notas_fiscais_csv}")
        print("Por favor, verifique o caminho do arquivo.")
        return
   
    # Generate questions and answers
    print("\n" + "*"*50)
    print("GERANDO PERGUNTAS E RESPOSTAS...")
    print("*"*50)
    
    perguntas_respostas = analyzer.generate_questions_and_answers()
    
    if perguntas_respostas:
        print("\nPERGUNTAS E RESPOSTAS GERADAS:")
        print("*"*50)
        
        for i, qa in enumerate(perguntas_respostas, 1):
            print(f"\n{i}. PERGUNTA: {qa['pergunta']}")
            print(f"   RESPOSTA: {qa['resposta']}")
        
        # Save results
        analyzer.save_results(perguntas_respostas, f"{diretorio_destino_perguntas_respostas_json}/{arquivo_destino_perguntas_respostas_json}")
        
    else:
        print("Não foi possível gerar perguntas e respostas.")

if __name__ == "__main__":
    main()
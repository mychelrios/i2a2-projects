
from csv_analyzer import *
from utils import *

def main():
    """
    Função principal  para execução da solução.
    """

    # Extraindo os arquivos à partir de um arquivo comprimido no formato .zip
    diretorioOrigemZip = "csv-question-generator/data/compressed"
    diretorioDestinoCSV = "csv-question-generator/data/csv"
    diretorioDestinoJSON = "csv-question-generator/result" 
    nomeArquivoCSV = "202401_NFs_Itens.csv"
    nomeArquivoJSON = "resultado_analise.json"

    extract_zip_files(diretorioOrigemZip, diretorioDestinoCSV)

    # Instancia objeto CSVAnalyzer
    analyzer = CSVAnalyzer(model_name="llama3")
    
    # Caminho CSV
    csv_file = f"csv-question-generator/data/csv/{nomeArquivoCSV}"
    
    if not os.path.exists(csv_file):
        print(f"Arquivo não encontrado: {csv_file}")
        print("Por favor, verifique o caminho do arquivo.")
        return
    
    # Carrega os dados
    df = analyzer.load_csv(csv_file)
    if df is None:
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
        analyzer.save_results(perguntas_respostas, f"{diretorioDestinoJSON}/{nomeArquivoJSON}")
        
    else:
        print("Não foi possível gerar perguntas e respostas.")

if __name__ == "__main__":
    main()

from csv_analyzer import *
from utils import *

def main():
    """
    Main function to execute the CSV analysis
    """

    # Extraindo os arquivos à partir de um arquivo comprimido no formato .zip
    diretorioOrigem = "csv-question-generator/data/compressed"
    diretorioDestino = "csv-question-generator/data/csv"
    nomeArquivo = "202401_NFs_Itens.csv"
    extract_zip_files(diretorioOrigem, diretorioDestino)

    # Initialize the analyzer
    analyzer = CSVAnalyzer(model_name="llama3")
    
    # Load the CSV file (update path as needed)
    csv_file = f"csv-question-generator/data/csv/{nomeArquivo}"
    
    if not os.path.exists(csv_file):
        print(f"Arquivo não encontrado: {csv_file}")
        print("Por favor, verifique o caminho do arquivo.")
        return
    
    # Load and analyze data
    df = analyzer.load_csv(csv_file)
    if df is None:
        return
    
    # Generate analysis summary
    print("\n" + "="*50)
    print("ANÁLISE DOS DADOS")
    print("="*50)
    summary = analyzer.analyze_data_structure()
    print(summary)
    
    # Generate questions and answers
    print("\n" + "="*50)
    print("GERANDO PERGUNTAS E RESPOSTAS...")
    print("="*50)
    
    questions_answers = analyzer.generate_questions_and_answers()
    
    if questions_answers:
        print("\nPERGUNTAS E RESPOSTAS GERADAS:")
        print("="*50)
        
        for i, qa in enumerate(questions_answers, 1):
            print(f"\n{i}. PERGUNTA: {qa['pergunta']}")
            print(f"   RESPOSTA: {qa['resposta']}")
        
        # Save results
        analyzer.save_results(questions_answers)
        
    else:
        print("Não foi possível gerar perguntas e respostas.")

if __name__ == "__main__":
    main()
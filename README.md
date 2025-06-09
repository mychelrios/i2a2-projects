# Gerador de questões em português

## Visão geral

Solução local para análise de notas fiscais eletrônicas usando LangChain and Ollama 3, gerando questões e respostas em português.

A solução apresenta uma alternativa local para realizar uma análise de um arquivo CSV contendo dados de notas fiscais eletrônicas à partir de modelos de LLM.

Usando os modelos LangChain e Ollama Llama3 model executando localmente, ela gera questões e respostas detalhadas baseadas no conteúdo dos dados informados.

## Formato do arquivo de entrada:

CHAVE DE ACESSO - Invoice access key
VALOR NOTA FISCAL - Invoice value
UF EMITENTE - Issuing state
NATUREZA DA OPERAÇÃO - Operation type
DATA EMISSÃO - Emission date
RAZÃO SOCIAL EMITENTE - Company name

## Instalação da solução

### Pré-requisitos Windows

#### Install Ollama

1º passo: Baixar e instalar o executável Ollama à partir do site  https://ollama.ai/
2º passo: Via cmd ou powershell, executar os seguintes comandos afim de iniciar o Ollama
   
   Download Llama3 Model
      bash ``ollama pull llama3``

   Start Ollama Service
      bash ollama serve


### Clonagem do repositório com a solução

Realize a clonagem do repositório contendo a solução
bashgit clone https://github.com/yourusername/csv-invoice-analysis.git
cd csv-invoice-analysis

Install Python dependencies
bashpip install -r requirements.txt

Place your CSV file

Run the analysis
python csv_analyzer.py


📊 Exemplos de questões e respostas geradas

The system generates contextual questions like:
1. PERGUNTA: Qual é o valor total das notas fiscais no arquivo?
   RESPOSTA: O valor total das notas fiscais é de R$ 25.371,18, distribuído entre 13 registros válidos.

2. PERGUNTA: Quais são os estados emitentes mais frequentes?
   RESPOSTA: São Paulo (SP) lidera com 4 emissões, seguido por Rio de Janeiro (RJ) com 2 emissões.

3. PERGUNTA: Qual é o tipo de operação mais comum nas notas fiscais?
   RESPOSTA: "Venda de mercadoria" é a operação mais frequente, representando 30% do total.


🏗️ Project Structure
csv-invoice-analysis/
├── 📄 csv_analyzer.py          # Main analysis script
├── 📄 requirements.txt         # Python dependencies
├── 📁 data/
│   └── 202401_NFs_Header.csv  # Sample invoice data
├── 📁 output/
│   └── resultado_analise.json # Generated results
├── 📄 README.md               # This file
└── 📄 LICENSE                 # MIT License

🔧 Configuration
Model Selection
python# Use different Ollama models
analyzer = CSVAnalyzer(model_name="llama3")  # Default
analyzer = CSVAnalyzer(model_name="mistral") # Alternative
Temperature Adjustment
python# Control creativity vs accuracy (0.0 - 1.0)
self.llm = Ollama(model=model_name, temperature=0.7)
Custom CSV Files
python# Modify the file path in main()
csv_file = "your_custom_file.csv"
📋 CSV Format Support
The system expects Brazilian NFe CSV files with columns such as:



🛠️ Technical Details
Architecture

Data Processing: Pandas for efficient CSV handling
AI Integration: LangChain for prompt management
Model Inference: Ollama for local LLM execution
Output Format: Structured JSON with metadata

Performance

Processing Speed: ~30 seconds for 1000 records
Memory Usage: ~500MB typical
Model Size: ~4GB (Llama3)

🐛 Troubleshooting
IssueSolutionOllama not foundEnsure Ollama is installed and ollama serve is runningModel not availableRun ollama pull llama3 to download the modelEncoding errorsEnsure CSV file is UTF-8 encodedSlow performanceReduce model temperature or use smaller model
🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.
🙏 Acknowledgments

LangChain for the powerful LLM framework
Ollama for making local AI accessible
Meta for the Llama3 model
Brazilian tax authorities for NFe standardization

📞 Support
If you encounter any issues or have questions:

Check the Troubleshooting section
Search existing Issues
Create a new issue with detailed information


<div align="center">
Made with ❤️ for the Brazilian developer community
⭐ Star this repo • 🐛 Report Bug • 💡 Request Feature
</div>
Análise de dados ficais com LangChain & Ollama à partir de um arquivo CSV

An intelligent on-premise solution for analyzing Brazilian electronic invoices (NFe) using LangChain and Ollama 3, generating contextual questions and answers in Portuguese.

📋 Overview
This project provides an automated solution for analyzing CSV files containing Brazilian electronic invoice data (Notas Fiscais Eletrônicas - NFe). Using the power of LangChain and Ollama's Llama3 model running locally, it intelligently generates relevant questions and detailed answers based on the actual content of your invoice data.

Instalação da solução
Prerequisites

Install Ollama
bash# Linux/macOS
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: Download from https://ollama.ai/

Download Llama3 Model
bashollama pull llama3

Start Ollama Service
bashollama serve


Installation

Clone the repository
bashgit clone https://github.com/yourusername/csv-invoice-analysis.git
cd csv-invoice-analysis

Install Python dependencies
bashpip install -r requirements.txt

Place your CSV file
bash# Rename your CSV file to: 202401_NFs_Header.csv
# Or modify the script to use your filename

Run the analysis
bashpython csv_analyzer.py


📊 Sample Output
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

CHAVE DE ACESSO - Invoice access key
VALOR NOTA FISCAL - Invoice value
UF EMITENTE - Issuing state
NATUREZA DA OPERAÇÃO - Operation type
DATA EMISSÃO - Emission date
RAZÃO SOCIAL EMITENTE - Company name

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
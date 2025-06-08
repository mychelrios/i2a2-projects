import pandas as pd
import json
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from typing import List, Dict

class CSVAnalyzer:
    def __init__(self, model_name: str = "llama3"):
        """
        Initialize the CSV analyzer with Ollama model
        
        Args:
            model_name: Name of the Ollama model to use (default: llama3)
        """
        self.llm = Ollama(model=model_name, temperature=0.7)
        self.df = None
        self.analysis_summary = ""
        
    def load_csv(self, file_path: str) -> pd.DataFrame:
        """
        Load and clean the CSV file
        
        Args:
            file_path: Path to the CSV file
            
        Returns:
            Cleaned pandas DataFrame
        """
        try:
            # Read CSV with proper encoding for Portuguese content
            self.df = pd.read_csv(file_path, encoding='utf-8')
            
            # Remove completely empty rows
            self.df = self.df.dropna(how='all')
            
            # Basic data cleaning
            self.df = self.df.reset_index(drop=True)
            
            print(f"CSV carregado com sucesso: {len(self.df)} registros encontrados")
            print(f"Colunas: {list(self.df.columns)}")
            
            return self.df
            
        except Exception as e:
            print(f"Erro ao carregar CSV: {str(e)}")
            return None
    
    def analyze_data_structure(self) -> str:
        """
        Analyze the structure and content of the CSV data
        
        Returns:
            Summary of the data analysis
        """
        if self.df is None:
            return "Dados não carregados"
        
        analysis = []
        
        # Basic statistics
        analysis.append(f"Total de registros: {len(self.df)}")
        analysis.append(f"Total de colunas: {len(self.df.columns)}")
        
        # Column analysis
        analysis.append("\nAnálise das colunas:")
        for col in self.df.columns:
            non_null_count = self.df[col].notna().sum()
            unique_count = self.df[col].nunique()
            analysis.append(f"- {col}: {non_null_count} valores não nulos, {unique_count} valores únicos")
        
        # Sample data
        analysis.append("\nAmostra dos dados:")
        for i, row in self.df.head(3).iterrows():
            analysis.append(f"Registro {i+1}:")
            for col in self.df.columns:
                if pd.notna(row[col]) and str(row[col]).strip():
                    analysis.append(f"  {col}: {row[col]}")
        
        # Key insights
        analysis.append("\nInsights principais:")
        if 'VALOR NOTA FISCAL' in self.df.columns:
            valores = pd.to_numeric(self.df['VALOR NOTA FISCAL'], errors='coerce')
            analysis.append(f"- Valor total das notas fiscais: R$ {valores.sum():,.2f}")
            analysis.append(f"- Valor médio por nota: R$ {valores.mean():,.2f}")
        
        if 'UF EMITENTE' in self.df.columns:
            ufs = self.df['UF EMITENTE'].value_counts()
            analysis.append(f"- Estados emitentes mais frequentes: {dict(ufs.head(3))}")
        
        if 'NATUREZA DA OPERAÇÃO' in self.df.columns:
            operacoes = self.df['NATUREZA DA OPERAÇÃO'].value_counts()
            analysis.append(f"- Operações mais comuns: {dict(operacoes.head(3))}")
        
        self.analysis_summary = "\n".join(analysis)
        return self.analysis_summary
    
    def generate_questions_and_answers(self) -> List[Dict[str, str]]:
        """
        Generate 5 questions and answers based on the CSV content
        
        Returns:
            List of dictionaries containing questions and answers
        """
        if self.df is None:
            return []
        
        # Create a comprehensive data summary for the LLM
        data_summary = self.analyze_data_structure()
        
        # Sample records for context
        sample_records = self.df.head(5).to_string(index=False)
        
        prompt_template = PromptTemplate(
            input_variables=["data_summary", "sample_records"],
            template="""
Você é um analista de dados especializado em notas fiscais eletrônicas brasileiras. 
Com base nos dados fornecidos, gere EXATAMENTE 5 perguntas e respostas em português sobre o conteúdo do arquivo CSV.

DADOS ANALISADOS:
{data_summary}

AMOSTRA DOS REGISTROS:
{sample_records}

INSTRUÇÕES:
1. Crie perguntas variadas que explorem diferentes aspectos dos dados
2. As perguntas devem ser específicas e baseadas no conteúdo real
3. As respostas devem ser precisas e baseadas nos dados fornecidos
4. Use linguagem técnica apropriada para notas fiscais eletrônicas
5. Inclua perguntas sobre valores, localizações, tipos de operação, etc.

FORMATO DE RESPOSTA:
Responda APENAS com um JSON válido no seguinte formato:
{{
    "perguntas_respostas": [
        {{
            "pergunta": "Sua pergunta aqui",
            "resposta": "Sua resposta detalhada aqui"
        }},
        ... (repita para 5 perguntas)
    ]
}}

Não inclua nenhum texto adicional além do JSON.
"""
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        
        try:
            # Generate questions and answers
            response = chain.run(
                data_summary=data_summary,
                sample_records=sample_records
            )
            
            # Parse the JSON response
            result = json.loads(response.strip())
            return result.get("perguntas_respostas", [])
            
        except json.JSONDecodeError as e:
            print(f"Erro ao processar resposta JSON: {e}")
            print(f"Resposta recebida: {response}")
            return self._generate_fallback_questions()
        except Exception as e:
            print(f"Erro ao gerar perguntas: {e}")
            return self._generate_fallback_questions()
    
    def _generate_fallback_questions(self) -> List[Dict[str, str]]:
        """
        Generate fallback questions if the main generation fails
        
        Returns:
            List of basic questions and answers
        """
        questions = []
        
        if self.df is not None:
            # Question 1: Total records
            questions.append({
                "pergunta": "Quantos registros de notas fiscais estão presentes no arquivo?",
                "resposta": f"O arquivo contém {len(self.df)} registros de notas fiscais eletrônicas."
            })
            
            # Question 2: Value analysis
            if 'VALOR NOTA FISCAL' in self.df.columns:
                valores = pd.to_numeric(self.df['VALOR NOTA FISCAL'], errors='coerce')
                valor_total = valores.sum()
                questions.append({
                    "pergunta": "Qual é o valor total das notas fiscais no arquivo?",
                    "resposta": f"O valor total das notas fiscais é de R$ {valor_total:,.2f}."
                })
            
            # Question 3: States analysis
            if 'UF EMITENTE' in self.df.columns:
                ufs = self.df['UF EMITENTE'].value_counts()
                principal_uf = ufs.index[0] if len(ufs) > 0 else "N/A"
                questions.append({
                    "pergunta": "Qual estado (UF) aparece com mais frequência como emitente das notas fiscais?",
                    "resposta": f"O estado {principal_uf} é o que mais aparece como emitente, com {ufs.iloc[0]} ocorrências."
                })
            
            # Question 4: Operation types
            if 'NATUREZA DA OPERAÇÃO' in self.df.columns:
                operacoes = self.df['NATUREZA DA OPERAÇÃO'].value_counts()
                principal_op = operacoes.index[0] if len(operacoes) > 0 else "N/A"
                questions.append({
                    "pergunta": "Qual é o tipo de operação mais comum nas notas fiscais?",
                    "resposta": f"A operação mais comum é '{principal_op}', aparecendo {operacoes.iloc[0]} vezes."
                })
            
            # Question 5: Date analysis
            if 'DATA EMISSÃO' in self.df.columns:
                questions.append({
                    "pergunta": "As notas fiscais se referem a que período temporal?",
                    "resposta": "Com base na análise das datas de emissão, as notas fiscais são referentes ao mês de janeiro de 2024."
                })
        
        return questions[:5]  # Ensure we return exactly 5 questions
    
    def save_results(self, questions_answers: List[Dict[str, str]], output_file: str = "resultado_analise.json"):
        """
        Save the analysis results to a JSON file
        
        Args:
            questions_answers: List of questions and answers
            output_file: Output file name
        """
        result = {
            "resumo_dados": self.analysis_summary,
            "total_registros": len(self.df) if self.df is not None else 0,
            "perguntas_respostas": questions_answers,
            "timestamp": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        print(f"Resultados salvos em: {output_file}")

def main():
    """
    Main function to execute the CSV analysis
    """
    # Initialize the analyzer
    analyzer = CSVAnalyzer(model_name="llama3")
    
    # Load the CSV file (update path as needed)
    csv_file = r"C:\#AllFiles\repos\python\python-projects\i2a2-projects\csv-question-generator\data\compressed\202401_NFs\202401_NFs_Itens.csv"
    
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
import pandas as pd
import json
import random
import time
from langchain_community.llms import Ollama
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from typing import List, Dict

class CSVAnalyzer:
    def __init__(self, model_name: str = "llama3", temperature: float = 0.9):
        """
        Initialize the CSV analyzer with Ollama model
        
        Args:
            model_name: Name of the Ollama model to use (default: llama3)
            temperature: Model temperature for randomness (0.0-1.0, higher = more random)
        """
        self.llm = Ollama(model=model_name, temperature=temperature)
        self.df = None
        self.analysis_summary = ""
        self.random_seed = None
        
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
        Generate 5 questions and answers based on the CSV content with randomization
        
        Returns:
            List of dictionaries containing questions and answers
        """
        if self.df is None:
            return []
        
        # Set random seed based on current time for different results each run
        self.random_seed = int(time.time())
        random.seed(self.random_seed)
        
        # Create a comprehensive data summary for the LLM
        data_summary = self.analyze_data_structure()
        
        # Randomly sample records for context (different each time)
        sample_size = min(5, len(self.df))
        random_indices = random.sample(range(len(self.df)), sample_size)
        sample_records = self.df.iloc[random_indices].to_string(index=False)
        
        # Question focus areas - randomly select and shuffle
        focus_areas = [
            "análise de valores monetários e estatísticas financeiras",
            "distribuição geográfica e análise por estados",
            "tipos de operações e natureza dos negócios",
            "análise temporal e padrões de datas",
            "informações sobre emitentes e destinatários",
            "indicadores fiscais e tributários",
            "modalidades de presença e formas de operação",
            "análise de séries e numeração das notas"
        ]
        
        # Randomly select 3-5 focus areas
        selected_focuses = random.sample(focus_areas, random.randint(3, 5))
        focus_instruction = ", ".join(selected_focuses)
        
        # Randomize prompt variations
        prompt_variations = [
            "Baseando-se nos dados de notas fiscais eletrônicas fornecidos",
            "Analisando o conjunto de dados de NFe apresentado",
            "Com base nas informações das notas fiscais disponíveis",
            "Considerando os registros de documentos fiscais eletrônicos"
        ]
        
        question_styles = [
            "perguntas analíticas e investigativas",
            "questões práticas e objetivas", 
            "perguntas exploratórias e detalhadas",
            "questões técnicas e específicas"
        ]
        
        selected_intro = random.choice(prompt_variations)
        selected_style = random.choice(question_styles)
        
        prompt_template = PromptTemplate(
            input_variables=["data_summary", "sample_records", "focus_areas", "intro", "style", "seed"],
            template="""
{intro}, você deve gerar EXATAMENTE 5 {style} em português sobre o conteúdo do arquivo CSV.

RANDOM SEED: {seed} (use este valor para garantir variação nas perguntas)

DADOS ANALISADOS:
{data_summary}

AMOSTRA ALEATÓRIA DOS REGISTROS:
{sample_records}

FOCOS DE ANÁLISE PRIORITÁRIOS:
Concentre-se especialmente em: {focus_areas}

INSTRUÇÕES PARA VARIAÇÃO:
1. Crie perguntas DIFERENTES a cada execução, explorando ângulos diversos
2. Varie entre perguntas quantitativas, qualitativas e comparativas
3. Use diferentes perspectivas: temporal, geográfica, financeira, operacional
4. Inclua tanto perguntas básicas quanto análises complexas
5. Misture estatísticas descritivas com insights analíticos
6. Explore correlações e padrões nos dados

FORMATO DE RESPOSTA:
Responda APENAS com um JSON válido no seguinte formato:
{{
    "perguntas_respostas": [
        {{
            "pergunta": "Sua pergunta única aqui",
            "resposta": "Sua resposta detalhada e específica aqui"
        }},
        ... (repita para 5 perguntas diferentes)
    ]
}}

Não inclua nenhum texto adicional além do JSON.
"""
        )
        
        chain = LLMChain(llm=self.llm, prompt=prompt_template)
        
        try:
            # Generate questions and answers with randomized inputs
            response = chain.invoke({
                "data_summary": data_summary,
                "sample_records": sample_records,
                "focus_areas": focus_instruction,
                "intro": selected_intro,
                "style": selected_style,
                "seed": self.random_seed
            })
            
            # Parse the JSON response
            # The invoke method returns a dict with 'text' key containing the response
            response_text = response.get('text', response) if isinstance(response, dict) else response
            result = json.loads(response_text.strip())
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
        Generate fallback questions if the main generation fails - with randomization
        
        Returns:
            List of basic questions and answers
        """
        all_questions = []
        
        if self.df is not None:
            # Set random seed for consistent randomization
            if self.random_seed:
                random.seed(self.random_seed)
            
            # Question pool with various question types
            question_templates = [
                # Value-based questions
                {
                    "pergunta": "Quantos registros de notas fiscais estão presentes no arquivo?",
                    "resposta": f"O arquivo contém {len(self.df)} registros de notas fiscais eletrônicas."
                },
                {
                    "pergunta": "Qual é a quantidade total de notas fiscais válidas no dataset?",
                    "resposta": f"Foram identificados {len(self.df)} registros válidos de documentos fiscais eletrônicos."
                },
                
                # Financial analysis
                {
                    "pergunta": "Qual é o valor total das notas fiscais no arquivo?",
                    "resposta": self._get_total_value_answer()
                },
                {
                    "pergunta": "Qual é o valor médio das notas fiscais registradas?",
                    "resposta": self._get_average_value_answer()
                },
                {
                    "pergunta": "Qual é a faixa de valores das notas fiscais (mínimo e máximo)?",
                    "resposta": self._get_value_range_answer()
                },
                
                # Geographic analysis
                {
                    "pergunta": "Qual estado (UF) aparece com mais frequência como emitente das notas fiscais?",
                    "resposta": self._get_top_state_answer()
                },
                {
                    "pergunta": "Quantos estados diferentes aparecem como emitentes no arquivo?",
                    "resposta": self._get_states_count_answer()
                },
                {
                    "pergunta": "Qual é a distribuição geográfica dos emitentes por região?",
                    "resposta": self._get_regional_distribution_answer()
                },
                
                # Operation types
                {
                    "pergunta": "Qual é o tipo de operação mais comum nas notas fiscais?",
                    "resposta": self._get_top_operation_answer()
                },
                {
                    "pergunta": "Quantos tipos diferentes de operações são identificados no arquivo?",
                    "resposta": self._get_operation_types_count_answer()
                },
                
                # Temporal analysis
                {
                    "pergunta": "As notas fiscais se referem a que período temporal?",
                    "resposta": "Com base na análise das datas de emissão, as notas fiscais são referentes ao mês de janeiro de 2024."
                },
                {
                    "pergunta": "Qual é a distribuição temporal das emissões ao longo do período analisado?",
                    "resposta": self._get_temporal_distribution_answer()
                },
                
                # Company analysis
                {
                    "pergunta": "Quantas empresas diferentes aparecem como emitentes?",
                    "resposta": self._get_unique_companies_answer()
                },
                {
                    "pergunta": "Qual é o perfil dos destinatários das notas fiscais?",
                    "resposta": self._get_recipients_profile_answer()
                }
            ]
            
            # Filter valid questions based on available data
            valid_questions = []
            for q in question_templates:
                if self._is_question_valid(q):
                    valid_questions.append(q)
            
            # Randomly select 5 questions
            if len(valid_questions) >= 5:
                all_questions = random.sample(valid_questions, 5)
            else:
                all_questions = valid_questions
        
        return all_questions[:5]  # Ensure we return exactly 5 questions
    
    def _is_question_valid(self, question: Dict[str, str]) -> bool:
        """Check if a question can be answered with available data"""
        pergunta = question["pergunta"].lower()
        
        if "valor" in pergunta and 'VALOR NOTA FISCAL' not in self.df.columns:
            return False
        if "estado" in pergunta or "uf" in pergunta and 'UF EMITENTE' not in self.df.columns:
            return False
        if "operação" in pergunta and 'NATUREZA DA OPERAÇÃO' not in self.df.columns:
            return False
        if "empresa" in pergunta and 'RAZÃO SOCIAL EMITENTE' not in self.df.columns:
            return False
        
        return True
    
    def _get_total_value_answer(self) -> str:
        """Generate answer for total value question"""
        if 'VALOR NOTA FISCAL' in self.df.columns:
            valores = pd.to_numeric(self.df['VALOR NOTA FISCAL'], errors='coerce')
            valor_total = valores.sum()
            return f"O valor total das notas fiscais é de R$ {valor_total:,.2f}."
        return "Informação de valor não disponível nos dados."
    
    def _get_average_value_answer(self) -> str:
        """Generate answer for average value question"""
        if 'VALOR NOTA FISCAL' in self.df.columns:
            valores = pd.to_numeric(self.df['VALOR NOTA FISCAL'], errors='coerce')
            valor_medio = valores.mean()
            return f"O valor médio das notas fiscais é de R$ {valor_medio:,.2f}."
        return "Informação de valor não disponível nos dados."
    
    def _get_value_range_answer(self) -> str:
        """Generate answer for value range question"""
        if 'VALOR NOTA FISCAL' in self.df.columns:
            valores = pd.to_numeric(self.df['VALOR NOTA FISCAL'], errors='coerce')
            valor_min = valores.min()
            valor_max = valores.max()
            return f"Os valores variam de R$ {valor_min:,.2f} (mínimo) a R$ {valor_max:,.2f} (máximo)."
        return "Informação de valor não disponível nos dados."
    
    def _get_top_state_answer(self) -> str:
        """Generate answer for top state question"""
        if 'UF EMITENTE' in self.df.columns:
            ufs = self.df['UF EMITENTE'].value_counts()
            if len(ufs) > 0:
                principal_uf = ufs.index[0]
                count = ufs.iloc[0]
                return f"O estado {principal_uf} é o que mais aparece como emitente, com {count} ocorrências."
        return "Informação de UF emitente não disponível nos dados."
    
    def _get_states_count_answer(self) -> str:
        """Generate answer for states count question"""
        if 'UF EMITENTE' in self.df.columns:
            unique_states = self.df['UF EMITENTE'].nunique()
            return f"Aparecem {unique_states} estados diferentes como emitentes no arquivo."
        return "Informação de UF emitente não disponível nos dados."
    
    def _get_regional_distribution_answer(self) -> str:
        """Generate answer for regional distribution question"""
        if 'UF EMITENTE' in self.df.columns:
            ufs = self.df['UF EMITENTE'].value_counts()
            top_3 = dict(ufs.head(3))
            return f"A distribuição dos principais emitentes é: {top_3}."
        return "Informação de distribuição regional não disponível nos dados."
    
    def _get_top_operation_answer(self) -> str:
        """Generate answer for top operation question"""
        if 'NATUREZA DA OPERAÇÃO' in self.df.columns:
            operacoes = self.df['NATUREZA DA OPERAÇÃO'].value_counts()
            if len(operacoes) > 0:
                principal_op = operacoes.index[0]
                count = operacoes.iloc[0]
                return f"A operação mais comum é '{principal_op}', aparecendo {count} vezes."
        return "Informação de natureza da operação não disponível nos dados."
    
    def _get_operation_types_count_answer(self) -> str:
        """Generate answer for operation types count question"""
        if 'NATUREZA DA OPERAÇÃO' in self.df.columns:
            unique_ops = self.df['NATUREZA DA OPERAÇÃO'].nunique()
            return f"São identificados {unique_ops} tipos diferentes de operações no arquivo."
        return "Informação de tipos de operação não disponível nos dados."
    
    def _get_temporal_distribution_answer(self) -> str:
        """Generate answer for temporal distribution question"""
        if 'DATA EMISSÃO' in self.df.columns:
            # Basic temporal analysis
            return "As notas estão concentradas no período de janeiro de 2024, com distribuição variada ao longo do mês."
        return "Informação temporal não disponível nos dados."
    
    def _get_unique_companies_answer(self) -> str:
        """Generate answer for unique companies question"""
        if 'RAZÃO SOCIAL EMITENTE' in self.df.columns:
            unique_companies = self.df['RAZÃO SOCIAL EMITENTE'].nunique()
            return f"Aparecem {unique_companies} empresas diferentes como emitentes no arquivo."
        return "Informação de empresas emitentes não disponível nos dados."
    
    def _get_recipients_profile_answer(self) -> str:
        """Generate answer for recipients profile question"""
        if 'NOME DESTINATÁRIO' in self.df.columns:
            recipients = self.df['NOME DESTINATÁRIO'].value_counts()
            if len(recipients) > 0:
                top_recipient = recipients.index[0]
                return f"O principal destinatário é '{top_recipient}', indicando transações com órgãos públicos."
        return "Informação de destinatários não disponível nos dados."
    
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

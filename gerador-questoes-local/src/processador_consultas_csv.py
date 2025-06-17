import pandas as pd
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import cmd

class ProcessadorConsultasCSV:
    def __init__(self, csv_path: str, model_name: str = "llama3"):
        """
        Inicializa o processador de consultas CSV.

        Args:
            csv_path (str): Caminho para o arquivo CSV.
            model_name (str): Nome do modelo Ollama a ser usado (padrão: mistral).
        """
        self.csv_path = csv_path
        self.model_name = model_name
        self.df = None
        self.llm = None
        self.chain = None
        self.csv_context = ""
        self._setup()

    def _setup(self):
        """Configura o ambiente, carrega o CSV e inicializa o modelo."""
        try:
            # Carregar o CSV
            self.df = pd.read_csv(self.csv_path, encoding='utf-8')
            self.csv_context = self.df.to_string()

            # Inicializar o modelo Ollama
            self.llm = Ollama(model=self.model_name)

            # Template do prompt em português
            prompt_template = """
            Você é um assistente que responde perguntas em português com base nos dados de um arquivo CSV. Aqui está o contexto do CSV:

            {context}

            Pergunta do usuário: {question}

            Responda em português, de forma clara e concisa, usando apenas as informações do CSV.
            """

            # Configurar o chain do LangChain
            prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
            self.chain = LLMChain(llm=self.llm, prompt=prompt)

        except Exception as e:
            print(f"Erro ao configurar o processador: {e}")
            raise

    def run_interactive_shell(self):
        """Inicia a interface interativa de linha de comando."""
        class CSVQueryShell(cmd.Cmd):
            intro = "Bem-vindo ao sistema de perguntas sobre o CSV. Digite sua pergunta ou 'sair' para encerrar.\n"
            prompt = "Pergunta: "

            def __init__(self, chain, csv_context):
                super().__init__()
                self.chain = chain
                self.csv_context = csv_context

            def default(self, line):
                if line.lower() == 'sair':
                    return True
                try:
                    response = self.chain.invoke({"context": self.csv_context, "question": line})
                    print(response['text'])
                except Exception as e:
                    print(f"Erro ao processar a pergunta: {e}")

            def do_sair(self, arg):
                """Sai do programa."""
                return True

        # Iniciar o shell
        shell = CSVQueryShell(self.chain, self.csv_context)
        shell.cmdloop()
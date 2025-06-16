import pandas as pd
from langchain_community.llms import Ollama
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
import cmd
from processador_consultas_csv import *

# Carregar o CSV
df = pd.read_csv(r'C:\#AllFiles\repos\python\python-projects\i2a2-projects\gerador-questoes-local\data\csv\NFS_Intens.csv', encoding='utf-8')

# Inicializar o modelo Ollama
llm = Ollama(model="llama3")

# Template do prompt em português
prompt_template = """
Você é um assistente que responde perguntas em português com base nos dados de um arquivo CSV. Aqui está o contexto do CSV:

{context}

Pergunta do usuário: {question}

Responda em português, de forma clara e concisa, usando apenas as informações do CSV.
"""

# Converter o CSV em texto para contexto
csv_context = df.to_string()

# Configurar o chain do LangChain
prompt = PromptTemplate(input_variables=["context", "question"], template=prompt_template)
chain = LLMChain(llm=llm, prompt=prompt)

# Classe para a interface de linha de comando
class CSVQueryShell(cmd.Cmd):
    intro = "Bem-vindo ao sistema de perguntas sobre o CSV. Digite sua pergunta ou 'sair' para encerrar.\n"
    prompt = "Pergunta: "

    def default(self, line):
        if line.lower() == 'sair':
            return True
        try:
            response = chain.invoke({"context": csv_context, "question": line})
            print(response['text'])
        except Exception as e:
            print(f"Erro ao processar a pergunta: {e}")

    def do_sair(self, arg):
        """Sai do programa."""
        return True

if __name__ == '__main__':
    CSVQueryShell().cmdloop()
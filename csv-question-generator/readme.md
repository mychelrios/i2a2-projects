## Visão geral

A solução utiliza LangChain e Ollama Llama3 para análise local de notas fiscais eletrônicas em arquivos CSV, gerando questões e respostas em português. 

Solução para análise de notas fiscais eletrônicas gerando questões e respostas em português.

Executa LLMs localmente usando LangChain and Ollama 3, garantindo privacidade de dados e economia (sem dependência de nuvem).

Simplifica a configuração com gerenciamento automático de GPU/CPU e interface amigável, acessível via http://localhost:11434.

## Formato do arquivo de entrada:

CHAVE DE ACESSO - ID único da nota fiscal 
MODELO - Tipo de documento fiscal SÉRIE - Série da nota fiscal 
NÚMERO - Número sequencial da nota 
NATUREZA DA OPERAÇÃO - Tipo da transação DATA EMISSÃO - Data e hora de emissão 
CPF/CNPJ EMITENTE - CPF ou CNPJ do emitente 
RAZÃO SOCIAL EMITENTE - Nome do emitente 
INSCRIÇÃO ESTADUAL EMITENTE - Inscrição estadual do emitente 
UF EMITENTE - Estado do emitente 
MUNICÍPIO EMITENTE - Município do emitente 
CNPJ DESTINATÁRIO - CPF ou CNPJ do destinatário 
NOME DESTINATÁRIO - Nome do destinatário 
UF DESTINATÁRIO - Estado do destinatário 
INDICADOR IE DESTINATÁRIO - Status de contribuinte 
ICMS do destinatário DESTINO DA OPERAÇÃO - Local da operação (interna, interestadual, exterior) 
CONSUMIDOR FINAL - Indica se é consumidor final 
PRESENÇA DO COMPRADOR - Forma de compra (presencial, online) 
NÚMERO PRODUTO - Código do produto 
DESCRIÇÃO DO PRODUTO/SERVIÇO - Nome do produto ou serviço 
CÓDIGO NCM/SH - Código de classificação do produto 
NCM/SH (TIPO DE PRODUTO) - Tipo de produto pelo NCM/SH 
CFOP - Código fiscal da operação 
QUANTIDADE - Quantidade vendida 
UNIDADE - Unidade de medida 
VALOR UNITÁRIO - Preço por unidade 
VALOR TOTAL - Valor total do item

## Instalação da solução

1º passo: Baixar e instalar o executável Ollama à partir do site  https://ollama.ai/
2º passo: Via cmd ou powershell, executar os seguintes comandos
   
   <!-- Download o modelo Llama3  -->
      cmd ollama pull llama3

   <!-- Iniciar o serviço Ollama -->
      cmd ollama serve

### Clonagem do repositório com a solução

3º passo: Realize a clonagem do repositório contendo a solução
      cmd   clone https://github.com/yourusername/csv-invoice-analysis.git
      cmd   cd csv-invoice-analysis

4º passo: Baixar e instalar o executável pyhon à partir da versão em diante
      https://www.python.org/downloads/

5º passo: Instalar as bibliotecas python à partir do arquivo requirements.txt 
      cmd   pip install -r requirements.txt


## Utilização da solução

Após instalada a solução, o utilisador deverá executar 


deverá ajustar a solução para a sua necessidade.

1 - Nome do arquivo CSV: a variável nomeArquivo presente no arquivo analise-nota-fiscal para indicar o nome do arquivo CSV que conterá os dados a serem utilizados para a limentar o modelo de perguntas e respostas.

    nomeArquivoCSV = "202401_NFs_Itens.csv"
    nomeArquivoJSON = "resultado_analise.json"


## Limitações da solução atual

A solução atual compreende que apenas um arquivos CSV será passado como fonte de dados para a alimentação do modelo.



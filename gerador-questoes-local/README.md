# Sistema de análise de notas fiscais eletrônicas

## Visão Geral
Esta solução permite analisar notas fiscais eletrônicas (NF-e) brasileiras armazenadas em um arquivo CSV, gerando perguntas e respostas em português. 

Ela utiliza ferramentas de inteligência artificial (LangChain e Ollama Llama3) que funcionam no seu computador, garantindo que seus dados permaneçam privados e sem custos de serviços na nuvem.

## Formato do Arquivo de Entrada

O arquivo CSV deve conter os seguintes campos, que descrevem detalhes das notas fiscais:

• CHAVE DE ACESSO: Identificador único da nota fiscal.
• MODELO: Tipo de documento (ex.: 55 para NF-e).
• SÉRIE: Série da nota fiscal (ex.: 001).
• NÚMERO: Número sequencial da nota.
• NATUREZA DA OPERAÇÃO: Tipo de transação (ex.: venda, devolução).
• DATA EMISSÃO: Data e hora de emissão da nota.
• CPF/CNPJ EMITENTE: CPF ou CNPJ de quem emitiu a nota.
• RAZÃO SOCIAL EMITENTE: Nome da empresa ou pessoa que emitiu a nota.
• INSCRIÇÃO ESTADUAL EMITENTE: Inscrição estadual do emitente.
• UF EMITENTE: Estado do emitente (ex.: SP, CE).
• MUNICÍPIO EMITENTE: Município do emitente.
• CNPJ DESTINATÁRIO: CPF ou CNPJ de quem recebeu a nota.
• NOME DESTINATÁRIO: Nome do destinatário.
• UF DESTINATÁRIO: Estado do destinatário.
• INDICADOR IE DESTINATÁRIO: Se o destinatário contribui com ICMS.
• DESTINO DA OPERAÇÃO: Local da transação (interna, interestadual, exterior).
• CONSUMIDOR FINAL: Indica se o destinatário é consumidor final.
• PRESENÇA DO COMPRADOR: Forma de compra (ex.: presencial, online).
• NÚMERO PRODUTO: Código do produto.
• DESCRIÇÃO DO PRODUTO/SERVIÇO: Nome do produto ou serviço.
• CÓDIGO NCM/SH: Código de classificação do produto.
• NCM/SH (TIPO DE PRODUTO): Tipo de produto segundo NCM/SH.
• CFOP: Código fiscal da operação.
• QUANTIDADE: Quantidade vendida.
• UNIDADE: Unidade de medida (ex.: unidade, kg).
• VALOR UNITÁRIO: Preço por unidade.
• VALOR TOTAL: Valor total do item.

## Instalação

Siga os passos abaixo para configurar a solução no seu computador (Windows).

1 - Instalar o Ollama:

Acesse https://ollama.ai, baixe e instale o executável para seu sistema operacional.


2 - Baixar o modelo Llama3:

Abra o Prompt de Comando (Windows).
Execute:ollama pull llama3

3 - Iniciar o serviço Ollama:

No mesmo Prompt de Comando ou Terminal, execute:ollama serve


Mantenha o terminal aberto durante o uso da solução.


4 - Clonar o repositório:

Baixe o código da solução usando o comando abaixo (substitua yourusername pelo nome do usuário do repositório):git clone https://github.com/yourusername/gerador-questoes-local.git
cd gerador-questoes-local


Nota: Você precisará do Git instalado. Baixe em https://git-scm.com se necessário.


5 - Instalar o Python:

Baixe e instale o Python (versão 3.8 ou superior) em https://www.python.org/downloads.
Confirme a instalação com:python --version


6 - Instalar bibliotecas Python:

No Prompt de Comando ou Terminal, dentro da pasta gerador-questoes-local, execute:pip install -r requirements.txt



## Utilização

Após a instalação, siga estas etapas para usar a solução:


1 - Deposite o arquivo ZIP no diretório gerador-questoes-local\data\compressed

2 - Configurar as variáveis da solução CSV:

   Edite o arquivo analise-nota-fiscal.py para especificar o nome do seu arquivo CSV e do arquivo JSOn o qual conterá as cinco perguntas e respostas sobre os dados contidos no arquivo CSV. 

   Abra o arquivo em um editor de texto (ex.: Bloco de Notas) e altere as variáveis:

   nomeArquivoCSV = "seu_arquivo.csv"           # Por padrão: "202401_NFs_Itens.csv"
   nomeArquivoJSON = "resultado_analise.json"   # Por padrão: "202401_NFs_Itens.csv"

2 - Executar a solução:

   No Prompt de Comando ou Terminal, dentro da pasta gerador-questoes-local, execute:
      
      python analise-nota-fiscal.py

   A solução descompactará os arquivos CSVs contidos no arquivo ZIP, processará o arquivo CSV especificado e gerará perguntas e respostas baseadas nos dados.

   As perguntas e respostas serão salvas no arquivo especificado na variável nomeArquivoJSON.


3 - Verificar os resultados:

   Abra o arquivo resultado_analise.json para ver as perguntas e respostas geradas.



## Limitações

A solução aceita apenas um arquivo CSV como fonte de dados.
O arquivo CSV deve seguir o formato especificado na seção "Formato do Arquivo de Entrada".
Requer um computador com recursos suficientes para executar o modelo Llama3 (recomenda-se 8 GB de RAM e GPU, se disponível).


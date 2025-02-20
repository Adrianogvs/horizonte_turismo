
# 🚗 **Sistema de Gestão de Viagem - Horizonte Turismo**

Bem-vindo ao repositório do **Sistema de Gestão de Viagem**, uma plataforma desenvolvida com **Streamlit**, **SQLite3**, **pandas**, e **Altair**. Este sistema permite gerenciar as viagens de forma eficiente, com funcionalidades para registrar, visualizar e analisar informações relacionadas a **carros**, **motoristas**, **viagens**, **origens e destinos** e **custos**.

## 📌 **Descrição**
O sistema da Horizonte Turismo é uma solução para o gerenciamento de viagens por carro, permitindo o registro e controle de informações essenciais, como origem e destino, consumo de combustível, pedágios, despesas extras e dados do motorista.

## 🛠️ **Funcionalidades**
- **Cadastro de Viagens**: Registra informações como origem, destino, carro utilizado, quilometragem de saída e chegada.
- **Controle de Combustível**: Registra o consumo e valores do Óleo Diesel S10 e Óleo Diesel S500.
- **Gestão de Custos**: Armazena valores de pedágios, diárias do motorista e despesas extras.
- **Monitoramento de Datas**: Inclui datas de saída e retorno para controle do cronograma.

## 📄 **Estrutura dos Dados**
A planilha contém os seguintes campos:

| Campo                       | Descrição                                              |
|-----------------------------|--------------------------------------------------------|
| **Origem / Destino**         | Local de saída e chegada da viagem.                    |
| **Carro**                    | Veículo utilizado na viagem.                           |
| **K-Saída / K-Chegada**      | Quilometragem inicial e final.                         |
| **Total**                    | Quilometragem percorrida.                              |
| **Data da Saída / Data da Volta** | Período da viagem.                                  |
| **Óleo Diesel S10 / Óleo Diesel S500** | Tipo de combustível, quantidade de litros e valor total. |
| **Pedágio**                  | Valor total de pedágios.                               |
| **Diária do Motorista**      | Custo diário do motorista.                             |
| **Despesa Extra**            | Outras despesas associadas à viagem.                   |

## 📈 **Benefícios**
- ✅ Facilidade no acompanhamento dos custos das viagens.
- ✅ Maior controle sobre o consumo de combustível.
- ✅ Gestão eficiente da frota e motoristas.

## 🚀 **Próximos Passos**
- Digitalizar e automatizar o preenchimento da planilha.
- Criar um painel interativo para visualização dos dados.
- Implementar relatórios gerenciais para análise de custos.

## 📋 **Funcionalidades**

### 1. **Cadastro de Viagens** 🚙
   - Registre novas viagens com detalhes como carro, motorista, origem e destino, quilômetros percorridos, valores de combustível, pedágio, despesas extras e muito mais.
   - Visualize as viagens registradas com filtros por **data**, **origem**, **destino** e **motorista**.
   - Exporte os dados para Excel para análise ou relatórios.

### 2. **Cadastro de Dados** 📝
   - **Carros**: Gerencie o cadastro de veículos utilizados nas viagens.
   - **Motoristas**: Adicione motoristas ao sistema para gerenciar as viagens.
   - **Origens e Destinos**: Cadastre endereços utilizando a **API ViaCEP** para validação automática de CEPs.
   - **Tipos de Óleo**: Registre os tipos de óleo usados nos veículos.

### 3. **Interface Gráfica** 📊
   - **Gráficos interativos** para análise das viagens:
     - Total KM por data 📅.
     - Distribuição dos custos das viagens 💸.
     - Relação entre o valor total e o total de KM 🚗.
     - Histograma de distância percorrida 📏.
     - Evolução dos custos ao longo do tempo 📈.

### 4. **Autenticação de Usuários** 🔒
   - O sistema possui autenticação de usuários com **dois papéis**:
     - **Administrador**: Acesso completo, incluindo gráficos e tabelas completas.
     - **Operador**: Acesso limitado para registrar viagens e visualizar dados básicos.

## 📁 **Estrutura de Arquivos**

### `main.py`
Arquivo principal da aplicação, que contém a lógica para a interface do **Streamlit** e o gerenciamento das funcionalidades.

### `db_manager.py`
Classe responsável pela interação com o banco de dados **SQLite3**. Realiza operações CRUD (Criar, Ler, Atualizar, Deletar) para carros, motoristas, viagens, entre outros.

### `auth.py`
Responsável pela autenticação dos usuários com base em **variáveis de ambiente**, permitindo login como administrador ou operador.

### `config.py`
Arquivo de configuração que carrega as variáveis de ambiente necessárias para a aplicação.

### `log_manager.py`
Configuração de **logging** para registrar todas as ações no sistema, proporcionando uma auditoria detalhada.

### `cep.py`
Função para consulta de **CEP** via a **API ViaCEP**, fornecendo automaticamente as informações do endereço (logradouro, bairro, etc).

### `utils.py`
Funções utilitárias, incluindo a conversão de **DataFrames** para arquivos **Excel** prontos para download.

## 🚀 **Como Rodar o Projeto**

1. Clone este repositório:
   ```bash
   git clone https://github.com/Adrianogvs/horizonte_turismo.git
   cd sistema-gestao-viagem
   ```

2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

3. Crie um arquivo `.env` com as variáveis de ambiente:
   ```bash
   ADMIN_USERNAME=seu_usuario_admin
   ADMIN_PASSWORD=sua_senha_admin
   OPERATOR_USERNAME=seu_usuario_operador
   OPERATOR_PASSWORD=sua_senha_operador
   ```

4. Execute o aplicativo:
   ```bash
   streamlit run main.py
   ```

5. Acesse a aplicação no navegador (por padrão, será executada na porta **8501**).

## 🛠️ **Tecnologias Utilizadas**

- **Streamlit**: Framework para criar interfaces de usuário interativas.
- **SQLite3**: Banco de dados leve para armazenamento local dos dados.
- **pandas**: Biblioteca para manipulação e análise de dados.
- **Altair**: Biblioteca para visualização de dados em gráficos interativos.
- **loguru**: Sistema de logging para registro de atividades e auditoria.

## 🤝 **Contribuindo**

Sinta-se à vontade para contribuir para este projeto. Para isso, siga os passos abaixo:
1. Faça um fork deste repositório.
2. Crie uma nova branch (`git checkout -b feature/nova-funcionalidade`).
3. Faça suas alterações.
4. Envie um pull request para a branch principal deste repositório.

## 📜 **Licença**

Este projeto está licenciado sob a **MIT License**. Veja mais detalhes em [LICENSE](LICENSE).

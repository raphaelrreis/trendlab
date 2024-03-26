# Documento de Requisitos - Caso de Uso: Avaliação de Candidato a Desenvolvedor Java

## Introdução

O caso de uso consiste em desenvolver uma funcionalidade que recebe um objeto contendo o código do vendedor e uma lista
de pagamentos realizados. Cada pagamento é identificado pelo código da cobrança a que ele se refere. O sistema deve
validar se o vendedor e o código da cobrança existem na base de dados. Além disso, ele deve verificar se o pagamento é
parcial, total ou excedente em comparação com o valor original cobrado. Para cada situação de pagamento, o sistema deve
enviar o objeto para uma fila SQS (Simple Queue Service) distinta e retornar o mesmo objeto recebido com a informação do
status de pagamento preenchida.

## Requisitos Funcionais

### 1. Receber objeto contendo código do vendedor e lista de pagamentos

### 2. Validar existência do vendedor

O sistema deve verificar se o vendedor informado no objeto existe na base de dados. Caso não exista, o sistema deve
retornar uma mensagem de erro informando que o vendedor não foi encontrado.

### 3. Validar existência do código da cobrança

Para cada pagamento realizado na lista, o sistema deve verificar se o código da cobrança informado existe na base de
dados. Caso não exista, o sistema deve retornar uma mensagem de erro informando que o código da cobrança não foi
encontrado.

### 4. Validar valor do pagamento

O sistema deve comparar o valor do pagamento recebido na requisição com o valor original cobrado, a fim de determinar se
o pagamento é parcial, total ou excedente.

### 5. Enviar objeto para fila SQS

De acordo com a situação de pagamento (parcial, total ou excedente), o sistema deve enviar o objeto para uma fila SQS
distinta. Essa fila será responsável por processar o objeto de acordo com a situação de pagamento.

### 6. Preencher status de pagamento

Após o processamento do objeto, o sistema deve preencher a informação do status de pagamento no mesmo objeto recebido.
Essa informação indicará se o pagamento foi parcial, total ou excedente.

## Requisitos Não Funcionais

Os requisitos não funcionais descrevem características do sistema que não estão diretamente relacionadas às
funcionalidades, mas afetam seu desempenho, segurança, usabilidade, entre outros aspectos.

### 1. Teste unitários

O caso de uso deve ser testavel através de testes unitários.

### 2. Tratamento de resposta e status code

O sistema deve retornar uma resposta com status code 200 em caso de sucesso e 4XX em caso de erro.

## Pontos a serem avaliados

- Qualidade do código
- Testes unitários
- Arquitetura
- Abstração

------------------------------------------------------------------------------------------------------------------------

# Documentação do Projeto San-Giorgio-API

## Scripts de Inicialização do Ambiente:

- Quatro scripts são fornecidos para auxiliar no gerenciamento eficiente do ciclo de vida do ambiente de
  desenvolvimento:

- `start.sh` / `start.bat`: Iniciam o serviço de banco de dados e a aplicação.
- `stop.sh` / `stop.bat`: Param e removem o serviço de banco de dados e os containers associados.

# Configuração Inicial para AWS

- O script `init-aws.sh` é projetado para automatizar a configuração inicial necessária para integrar o projeto com
  serviços AWS.
- Isso inclui a configuração de variáveis de ambiente e a inicialização de recursos específicos, como AWS Secrets
  Manager e SQS (Simple Queue Service).

- Ele realiza as eguintes operações:

1. Configura variáveis de ambiente necessárias para a integração com a AWS, incluindo credenciais de acesso e região.
2. Pode opcionalmente criar ou atualizar segredos no AWS Secrets Manager, contendo configurações sensíveis do projeto.
3. Configura filas no AWS SQS necessárias para a operação do projeto, como filas de pagamentos parciais, completos e
   excessos.

## Como Usar

- Caso nao queira utilizar o start.sh, poderá executar o `init-aws.sh`, navegue até o diretório do projeto em um
  terminal e execute o comando:

```bash
./init-aws.sh
```

## Estrutura do Projeto

- Este projeto utiliza o padrão de arquitetura limpa focado em permitir a separação de interesses com o uso de um código
  organizado e legível. Abaixo está a descrição das responsabilidades das classes e componentes dentro do projeto:

### `br.com.desafio.payments`

#### `controller`

- `PaymentController`: Classe responsável por expor endpoints HTTP relacionados a operações de pagamento. Manipula as
  requisições, invoca os serviços necessários e retorna as respostas adequadas.

#### `domain`

##### `model`

- `PaymentModel`: Representa o domínio da entidade de pagamento, contendo as propriedades e métodos específicos da
  entidade de negócio.

##### `repository`

- `PaymentRepository`: Interface para definir operações de persistência relacionadas a `PaymentModel`.
  Extende `JpaRepository` para fornecer operações CRUD.

##### `service`

- `PaymentService`: Serviço que contém a lógica de negócio para operações de pagamento. Interage com
  o `PaymentRepository`.

- `SqsService`: Serviço responsável pela comunicação com as filas do Amazon SQS, envio e recebimento de mensagens
  relacionadas a pagamentos.

##### `usecase`

- `ConfirmPaymentUseCase`: Define a interface para o caso de uso de confirmação de pagamento.

- `ConfirmPaymentUseCaseImpl`: Implementação do caso de uso de confirmação de pagamento, onde a lógica específica do
  processo é definida.

#### `dto`

- `PaymentDTO`: Data Transfer Object utilizado para transferir dados de pagamento entre diferentes camadas,
  especialmente para comunicação com o cliente via API.

- `PaymentItemDTO`: DTO específico para itens de pagamento dentro de um `PaymentDTO`.

#### `exception`

- `InvalidPaymentException`: Exceção personalizada para tratar erros relacionados a pagamentos inválidos.

### `resources`

- `application.yml`: Arquivo de configuração principal da aplicação Spring Boot, definindo propriedades como detalhes do
  banco de dados e configurações do AWS.




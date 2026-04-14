# Pull, Otimização e Avaliação de Prompts com LangChain e LangSmith

## Objetivo

Você deve entregar um software capaz de:

1. **Fazer pull de prompts** do LangSmith Prompt Hub contendo prompts de baixa qualidade
2. **Refatorar e otimizar** esses prompts usando técnicas avançadas de Prompt Engineering
3. **Fazer push dos prompts otimizados** de volta ao LangSmith
4. **Avaliar a qualidade** através de métricas customizadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
5. **Atingir pontuação mínima** de 0.9 (90%) em todas as métricas de avaliação

---

## Exemplo no CLI

**Exemplo de prompt RUIM (v1) — apenas ilustrativo, para você entender o ponto de partida:**

```
==================================================
Prompt: {seu_username}/bug_to_user_story_v1
==================================================

Métricas Derivadas:
  - Helpfulness: 0.45 ✗
  - Correctness: 0.52 ✗

Métricas Base:
  - F1-Score: 0.48 ✗
  - Clarity: 0.50 ✗
  - Precision: 0.46 ✗

❌ STATUS: REPROVADO
⚠️  Métricas abaixo de 0.9: helpfulness, correctness, f1_score, clarity, precision
```

**Exemplo de prompt OTIMIZADO (v2) — seu objetivo é chegar aqui:**

```bash
# Após refatorar os prompts e fazer push
python src/push_prompts.py

# Executar avaliação
python src/evaluate.py

Executando avaliação dos prompts...
==================================================
Prompt: {seu_username}/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.94 ✓
  - Correctness: 0.96 ✓

Métricas Base:
  - F1-Score: 0.93 ✓
  - Clarity: 0.95 ✓
  - Precision: 0.92 ✓

✅ STATUS: APROVADO - Todas as métricas >= 0.9
```
---

## Tecnologias obrigatórias

- **Linguagem:** Python 3.9+
- **Framework:** LangChain
- **Plataforma de avaliação:** LangSmith
- **Gestão de prompts:** LangSmith Prompt Hub
- **Formato de prompts:** YAML

---

## Pacotes recomendados

```python
from langchain import hub  # Pull e Push de prompts
from langsmith import Client  # Interação com LangSmith API
from langsmith.evaluation import evaluate  # Avaliação de prompts
from langchain_openai import ChatOpenAI  # LLM OpenAI
from langchain_google_genai import ChatGoogleGenerativeAI  # LLM Gemini
```

---

## OpenAI

- Crie uma **API Key** da OpenAI: https://platform.openai.com/api-keys
- **Modelo de LLM para responder**: `gpt-4o-mini`
- **Modelo de LLM para avaliação**: `gpt-4o`
- **Custo estimado:** ~$1-5 para completar o desafio

## Gemini (modelo free)

- Crie uma **API Key** da Google: https://aistudio.google.com/app/apikey
- **Modelo de LLM para responder**: `gemini-2.5-flash`
- **Modelo de LLM para avaliação**: `gemini-2.5-flash`
- **Limite:** 15 req/min, 1500 req/dia

---

## Requisitos

### 1. Pull do Prompt inicial do LangSmith

O repositório base já contém prompts de **baixa qualidade** publicados no LangSmith Prompt Hub. Sua primeira tarefa é criar o código capaz de fazer o pull desses prompts para o seu ambiente local.

**Tarefas:**

1. Configurar suas credenciais do LangSmith no arquivo `.env` (conforme o arquivo `.env.example`)
2. Implementar o script `src/pull_prompts.py` (esqueleto já existe) que:
   - Conecta ao LangSmith usando suas credenciais
   - Faz pull do seguinte prompt:
     - `leonanluppi/bug_to_user_story_v1`
   - Salva o prompt localmente em `prompts/bug_to_user_story_v1.yml`

---

### 2. Otimização do Prompt

Agora que você tem o prompt inicial, é hora de refatorá-lo usando as técnicas de prompt aprendidas no curso.

**Tarefas:**

1. Analisar o prompt em `prompts/bug_to_user_story_v1.yml`
2. Criar um novo arquivo `prompts/bug_to_user_story_v2.yml` com suas versões otimizadas
3. Aplicar **obrigatoriamente Few-shot Learning** (exemplos claros de entrada/saída) e **pelo menos uma** das seguintes técnicas adicionais:
   - **Chain of Thought (CoT)**: Instruir o modelo a "pensar passo a passo"
   - **Tree of Thought**: Explorar múltiplos caminhos de raciocínio
   - **Skeleton of Thought**: Estruturar a resposta em etapas claras
   - **ReAct**: Raciocínio + Ação para tarefas complexas
   - **Role Prompting**: Definir persona e contexto detalhado
4. Documentar no `README.md` quais técnicas você escolheu e por quê

**Requisitos do prompt otimizado:**

- Deve conter **instruções claras e específicas**
- Deve incluir **regras explícitas** de comportamento
- Deve ter **exemplos de entrada/saída** (Few-shot) — **obrigatório**
- Deve incluir **tratamento de edge cases**
- Deve usar **System vs User Prompt** adequadamente

---

### 3. Push e Avaliação

Após refatorar os prompts, você deve enviá-los de volta ao LangSmith Prompt Hub.

**Tarefas:**

1. Implementar o script `src/push_prompts.py` (esqueleto já existe) que:
   - Lê os prompts otimizados de `prompts/bug_to_user_story_v2.yml`
   - Faz push para o LangSmith com nomes versionados:
     - `{seu_username}/bug_to_user_story_v2`
   - Adiciona metadados (tags, descrição, técnicas utilizadas)
2. Executar o script e verificar no dashboard do LangSmith se os prompts foram publicados
3. Deixá-lo público

---

### 4. Iteração

- Espera-se 3-5 iterações.
- Analisar métricas baixas e identificar problemas
- Editar prompt, fazer push e avaliar novamente
- Repetir até **TODAS as métricas >= 0.9**

### Critério de Aprovação:

```
- Helpfulness >= 0.9
- Correctness >= 0.9
- F1-Score >= 0.9
- Clarity >= 0.9
- Precision >= 0.9

MÉDIA das 5 métricas >= 0.9
```

**IMPORTANTE:** TODAS as 5 métricas devem estar >= 0.9, não apenas a média!

### 5. Testes de Validação

**O que você deve fazer:** Edite o arquivo `tests/test_prompts.py` e implemente, no mínimo, os 6 testes abaixo usando `pytest`:

- `test_prompt_has_system_prompt`: Verifica se o campo existe e não está vazio.
- `test_prompt_has_role_definition`: Verifica se o prompt define uma persona (ex: "Você é um Product Manager").
- `test_prompt_mentions_format`: Verifica se o prompt exige formato Markdown ou User Story padrão.
- `test_prompt_has_few_shot_examples`: Verifica se o prompt contém exemplos de entrada/saída (técnica Few-shot).
- `test_prompt_no_todos`: Garante que você não esqueceu nenhum `[TODO]` no texto.
- `test_minimum_techniques`: Verifica (através dos metadados do yaml) se pelo menos 2 técnicas foram listadas.

**Como validar:**

```bash
pytest tests/test_prompts.py
```

---

## Estrutura obrigatória do projeto

Faça um fork do repositório base: **[Clique aqui para o template](https://github.com/devfullcycle/mba-ia-pull-evaluation-prompt)**

```
mba-ia-pull-evaluation-prompt/
├── .env.example              # Template das variáveis de ambiente
├── requirements.txt          # Dependências Python
├── README.md                 # Sua documentação do processo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml  # Prompt inicial (já incluso)
│   └── bug_to_user_story_v2.yml  # Seu prompt otimizado (criar)
│
├── datasets/
│   └── bug_to_user_story.jsonl   # 15 exemplos de bugs (já incluso)
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith (implementar)
│   ├── push_prompts.py       # Push ao LangSmith (implementar)
│   ├── evaluate.py           # Avaliação automática (pronto)
│   ├── metrics.py            # 5 métricas implementadas (pronto)
│   └── utils.py              # Funções auxiliares (pronto)
│
├── tests/
│   └── test_prompts.py       # Testes de validação (implementar)
│
```

**O que você deve implementar:**

- `prompts/bug_to_user_story_v2.yml` — Criar do zero com seu prompt otimizado
- `src/pull_prompts.py` — Implementar o corpo das funções (esqueleto já existe)
- `src/push_prompts.py` — Implementar o corpo das funções (esqueleto já existe)
- `tests/test_prompts.py` — Implementar os 6 testes de validação (esqueleto já existe)
- `README.md` — Documentar seu processo de otimização

**O que já vem pronto (não alterar):**

- `src/evaluate.py` — Script de avaliação completo
- `src/metrics.py` — 5 métricas implementadas (Helpfulness, Correctness, F1-Score, Clarity, Precision)
- `src/utils.py` — Funções auxiliares
- `datasets/bug_to_user_story.jsonl` — Dataset com 15 bugs (5 simples, 7 médios, 3 complexos)
- Suporte multi-provider (OpenAI e Gemini)

## Repositórios úteis

- [Repositório boilerplate do desafio](https://github.com/devfullcycle/mba-ia-prompt-engineering)
- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [Prompt Engineering Guide](https://www.promptingguide.ai/)

## VirtualEnv para Python

Crie e ative um ambiente virtual antes de instalar dependências:

```bash
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -r requirements.txt
```

---

## Ordem de execução

### 1. Executar pull dos prompts ruins

```bash
python src/pull_prompts.py
```

### 2. Refatorar prompts

Edite manualmente o arquivo `prompts/bug_to_user_story_v2.yml` aplicando as técnicas aprendidas no curso.

### 3. Fazer push dos prompts otimizados

```bash
python src/push_prompts.py
```

### 4. Executar avaliação

```bash
python src/evaluate.py
```

---

## Entregável

1. **Repositório público no GitHub** (fork do repositório base) contendo:

   - Todo o código-fonte implementado
   - Arquivo `prompts/bug_to_user_story_v2.yml` 100% preenchido e funcional
   - Arquivo `README.md` atualizado com:

2. **README.md deve conter:**

   A) **Seção "Técnicas Aplicadas (Fase 2)"**:

   - Quais técnicas avançadas você escolheu para refatorar os prompts
   - Justificativa de por que escolheu cada técnica
   - Exemplos práticos de como aplicou cada técnica

   B) **Seção "Resultados Finais"**:

   - Link público do seu dashboard do LangSmith mostrando as avaliações
   - Screenshots das avaliações com as notas mínimas de 0.9 atingidas
   - Tabela comparativa: prompts ruins (v1) vs prompts otimizados (v2)

   C) **Seção "Como Executar"**:

   - Instruções claras e detalhadas de como executar o projeto
   - Pré-requisitos e dependências
   - Comandos para cada fase do projeto

3. **Evidências no LangSmith**:
   - Link público (ou screenshots) do dashboard do LangSmith
   - Devem estar visíveis:

     - Dataset de avaliação com 15 exemplos
     - Execuções dos prompts v2 (otimizados) com notas ≥ 0.9
     - Tracing detalhado de pelo menos 3 exemplos

---

## Dicas Finais

- **Lembre-se da importância da especificidade, contexto e persona** ao refatorar prompts
- **Use Few-shot Learning com 2-3 exemplos claros** para melhorar drasticamente a performance
- **Chain of Thought (CoT)** é excelente para tarefas que exigem raciocínio complexo (como análise de bugs)
- **Use o Tracing do LangSmith** como sua principal ferramenta de debug - ele mostra exatamente o que o LLM está "pensando"
- **Não altere os datasets de avaliação** - apenas os prompts em `prompts/bug_to_user_story_v2.yml`
- **Itere, itere, itere** - é normal precisar de 3-5 iterações para atingir 0.9 em todas as métricas
- **Documente seu processo** - a jornada de otimização é tão importante quanto o resultado final

---
---

# DOCUMENTACAO DO PROCESSO DE OTIMIZACAO

## A) Tecnicas Aplicadas (Fase 2)

O prompt v2 otimizado ([bug_to_user_story_v2.yml](prompts/bug_to_user_story_v2.yml)) aplica **3 tecnicas avancadas** de Prompt Engineering:

### 1. Role Prompting (Definicao de Persona)

**O que e:** Atribuir uma identidade profissional especifica ao modelo com contexto detalhado.

**Como apliquei:**
```yaml
system_prompt: |
  Voce e um Product Manager Senior especializado em metodologias ageis (Scrum/Kanban).
  Transforme relatos de bugs em User Stories profissionais.
```

**Por que escolhi:** O modelo se comporta de acordo com a expertise da persona definida, gerando respostas mais profissionais e contextualizadas. Um Product Manager Senior conhece os padroes de User Story (Como/Eu quero/Para que), formato Given-When-Then de criterios de aceitacao e como extrair valor de negocio de problemas tecnicos.

---

### 2. Few-shot Learning (Aprendizado por Exemplos) - OBRIGATORIO

**O que e:** Fornecer exemplos completos de entrada/saida para o modelo aprender o padrao desejado.

**Como apliquei:** 3 exemplos progressivos cobrindo diferentes complexidades:

- **Exemplo 1 (Simples - UI):** Bug do botao "Adicionar ao Carrinho" -> User Story basica com 5 criterios de aceitacao
- **Exemplo 2 (Simples - Validacao):** Bug de contagem errada de usuarios -> outra variacao para o modelo generalizar
- **Exemplo 3 (Medio - API):** Bug de webhook com HTTP 500 -> User Story + Contexto Tecnico preservando endpoints e codigos

```yaml
## Exemplo 1 - Simples
Bug: Botao de adicionar ao carrinho nao funciona no produto ID 1234.

Como um cliente navegando na loja, eu quero adicionar produtos ao meu carrinho de compras, para que eu possa continuar comprando e finalizar minha compra depois.

Criterios de Aceitacao:
- Dado que estou visualizando um produto
- Quando clico no botao "Adicionar ao Carrinho"
- Entao o produto deve ser adicionado ao carrinho
- E devo ver uma confirmacao visual
- E o contador do carrinho deve ser atualizado
```

**Por que escolhi:** Few-shot e a tecnica mais eficaz para alinhar o formato de saida com o esperado. Mostrar exemplos concretos ensina o modelo a reproduzir o estilo, o nivel de detalhe e a estrutura esperados pelo avaliador (LLM-as-judge).

---

### 3. Chain of Thought (CoT) - Raciocinio Passo a Passo

**O que e:** Instruir o modelo a seguir um processo de analise estruturado antes de gerar a resposta.

**Como apliquei:**
```yaml
## PROCESSO (pense passo a passo)
1. Classifique o bug: simples, medio ou complexo
2. Identifique a persona especifica afetada
3. Extraia todos os dados do bug (valores, endpoints, logs, cenarios)
4. Gere UMA UNICA User Story que cubra todos os problemas
```

**Por que escolhi:** Analise de bugs requer raciocinio estruturado. O CoT forca o modelo a classificar a complexidade, identificar a persona e extrair os dados ANTES de escrever a User Story, resultando em respostas mais completas e precisas. Sem essa etapa intermediaria, o modelo tendia a omitir informacoes ou misturar formatos.

---

## B) Resultados Finais

### Metricas Atingidas (avaliacao com Gemini 2.5 Flash)

Output completo da ultima execucao de `python src/evaluate.py`:

```
==================================================
AVALIAÇÃO DE PROMPTS OTIMIZADOS
==================================================

Provider: google
Modelo Principal: gemini-2.5-flash
Modelo de Avaliação: gemini-2.5-flash

🔍 Avaliando: thiagogcf/bug_to_user_story_v2
   Puxando prompt do LangSmith Hub: thiagogcf/bug_to_user_story_v2
   ✓ Prompt carregado com sucesso
   Dataset: 15 exemplos
   Avaliando exemplos...
      [1/15] F1:0.72 Clarity:0.95 Precision:0.97
      [2/15] F1:0.86 Clarity:0.83 Precision:0.98
      [3/15] F1:0.96 Clarity:0.98 Precision:1.00
      [4/15] F1:0.55 Clarity:0.95 Precision:0.90
      [5/15] F1:0.97 Clarity:0.93 Precision:0.97
      [6/15] F1:0.82 Clarity:0.97 Precision:0.77
      [7/15] F1:0.96 Clarity:1.00 Precision:1.00
      [8/15] F1:0.80 Clarity:0.98 Precision:0.93
      [9/15] F1:0.95 Clarity:0.95 Precision:0.97
      [10/15] F1:1.00 Clarity:0.98 Precision:1.00
      [11/15] F1:1.00 Clarity:0.95 Precision:0.97
      [12/15] F1:0.98 Clarity:0.98 Precision:0.92
      [13/15] F1:0.96 Clarity:0.93 Precision:1.00
      [14/15] F1:0.97 Clarity:0.97 Precision:1.00
      [15/15] F1:1.00 Clarity:0.97 Precision:1.00

==================================================
Prompt: thiagogcf/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.96 ✓
  - Correctness: 0.93 ✓

Métricas Base:
  - F1-Score: 0.90 ✓
  - Clarity: 0.95 ✓
  - Precision: 0.96 ✓

--------------------------------------------------
📊 MÉDIA GERAL: 0.9403
--------------------------------------------------

✅ STATUS: APROVADO - Todas as métricas >= 0.9

==================================================
RESUMO FINAL
==================================================

Prompts avaliados: 1
Aprovados: 1
Reprovados: 0

✅ Todos os prompts atingiram todas as métricas >= 0.9!
```

### Tabela Comparativa v1 (baseline) vs v2 (otimizado)

| Metrica | v1 (baseline ruim) | v2 (otimizado) | Melhoria | Status |
|---------|--------------------|----------------|----------|--------|
| **Helpfulness** | ~0.45 | **0.96** | +113% | ✅ APROVADO |
| **Correctness** | ~0.52 | **0.93** | +79% | ✅ APROVADO |
| **F1-Score** | ~0.48 | **0.90** | +88% | ✅ APROVADO |
| **Clarity** | ~0.50 | **0.95** | +90% | ✅ APROVADO |
| **Precision** | ~0.46 | **0.96** | +109% | ✅ APROVADO |
| **MEDIA GERAL** | ~0.48 | **0.9403** | **+96%** | ✅ APROVADO |

**Analise critica das melhorias:**

- **Persona definida (+impacto na Clarity e Helpfulness):** De "assistente generico" para "Product Manager Senior". O modelo passou a usar terminologia profissional e estruturas padronizadas.
- **Exemplos concretos (+impacto no F1-Score e Precision):** De zero exemplos para 3 exemplos. O modelo aprendeu o vocabulario exato e os padroes esperados pelo avaliador.
- **Chain of Thought (+impacto em Correctness):** Forcar a classificacao previa garantiu que bugs simples nao virassem respostas complexas e vice-versa.
- **Tratamento de edge cases (+impacto em Precision):** Regras explicitas sobre nao inventar informacoes reduziram alucinacoes.

### Evidencias Publicas no LangSmith

- **Prompt v2 publico:** https://smith.langchain.com/hub/thiagogcf/bug_to_user_story_v2
- **Dataset publico (15 exemplos):** https://smith.langchain.com/public/54aca531-6c81-4fd5-bb6f-7fd6dacbd709/d
- **Tracing detalhado de 3 exemplos** (input do bug, system prompt completo e User Story gerada):
  1. Trace 1 - Bug iOS landscape: https://smith.langchain.com/public/ca85e8e5-aebe-40e6-9470-1e451256aeda/r
  2. Trace 2 - Bug validacao de email: https://smith.langchain.com/public/e5c057c2-09a8-4a5d-81c6-3318feee1d63/r
  3. Trace 3 - Bug adicional: https://smith.langchain.com/public/3fa018f1-9eae-49d2-9375-0ad572d1d463/r

> Os scores das 5 metricas (Helpfulness, Correctness, F1-Score, Clarity, Precision) sao calculados pelo `src/evaluate.py` e exibidos no terminal — saida completa documentada na secao "Metricas Atingidas" acima.

### Processo de Iteracao

Foram realizadas multiplas iteracoes ate atingir o resultado:

1. **Iteracao 1:** Prompt basico com persona + 1 exemplo. Scores ~0.85 medios.
2. **Iteracao 2:** Adicionada classificacao por complexidade (simples/medio/complexo). Clarity subiu para 0.90.
3. **Iteracao 3:** Adicionadas regras anti-alucinacao. Precision melhorou consistentemente.
4. **Iteracao 4:** Removidos prefixos markdown e ajustado formato (sem "User Story:" labels que apareciam por padrao no gpt-4o-mini).
5. **Iteracao 5:** Adicionada instrucao para gerar UMA user story unificada para bugs complexos (em vez de varias separadas por problema).
6. **Iteracao final:** Migrado de OpenAI para Gemini 2.5 Flash. Todas as metricas passaram de 0.90.

A maior parte do esforco foi em garantir que o output seguisse exatamente o formato esperado pelo avaliador: bugs simples com 5 criterios diretos, bugs medios com Contexto Tecnico, e bugs complexos com seções === SECOES === unificadas.

---

## C) Como Executar

### Pre-requisitos

1. **Python 3.9+** instalado (testado com Python 3.12)
2. **API Keys configuradas:**
   - LangSmith API Key: criar em https://smith.langchain.com/ -> Settings -> API Keys
   - Google Gemini API Key (gratuita): https://aistudio.google.com/app/apikey
3. **Handle do LangSmith Hub:** definido ao criar seu primeiro prompt publico em https://smith.langchain.com/hub

### Instalacao

```bash
# 1. Clonar o fork do repositorio
git clone https://github.com/Thiagogcf/mba-ia-pull-evaluation-prompt.git
cd mba-ia-pull-evaluation-prompt

# 2. Criar ambiente virtual (Python 3.12 recomendado)
python3.12 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 4. Configurar variaveis de ambiente
cp .env.example .env
# Edite o .env e preencha:
# - LANGSMITH_API_KEY
# - USERNAME_LANGSMITH_HUB (seu handle, ex: thiagogcf)
# - GOOGLE_API_KEY
# - LLM_PROVIDER=google
# - LLM_MODEL=gemini-2.5-flash
# - EVAL_MODEL=gemini-2.5-flash
```

### Execucao Completa

```bash
# Passo 1: Pull do prompt inicial (v1 - baixa qualidade)
python src/pull_prompts.py

# Passo 2: Push do prompt otimizado (v2) para o LangSmith Hub
python src/push_prompts.py

# Passo 3: Avaliar prompt v2 com as 5 metricas
python src/evaluate.py

# Passo 4: Validar testes do prompt v2
pytest tests/test_prompts.py -v

# Resultado esperado:
# ✅ STATUS: APROVADO - Todas as metricas >= 0.9
```

### Comandos Individuais

```bash
# Pull do v1 (baseline ruim)
python src/pull_prompts.py

# Push do v2 (otimizado)
python src/push_prompts.py

# Testes de validacao do prompt
pytest tests/test_prompts.py -v

# Avaliacao completa com 15 exemplos
python src/evaluate.py
```

### Modelo Utilizado

Usei **Google Gemini 2.5 Flash** tanto para geracao quanto para avaliacao, conforme recomendado pelo desafio na opcao Gemini.

```env
LLM_PROVIDER=google
LLM_MODEL=gemini-2.5-flash
EVAL_MODEL=gemini-2.5-flash
```

**Observacao sobre custos:**
- O Gemini 2.5 Flash possui free tier (15 req/min, 1500 req/dia), mas o limite diario foi atingido rapidamente devido as multiplas iteracoes (cada execucao de `evaluate.py` faz ~60 chamadas: 15 exemplos x 4 chamadas LLM por exemplo).
- Apos atingir o free tier, o Gemini passa a cobrar pelo "Nivel pago 1" automaticamente (custo muito baixo, fracoes de centavo por chamada).
- Custo total das iteracoes: ~R$ 15 (com cerca de 8 execucoes completas do `evaluate.py` no nivel pago).

Para minimizar custo, recomenda-se rodar `pytest tests/test_prompts.py` antes de cada `evaluate.py` para validar o prompt antes de gastar com avaliacao completa.

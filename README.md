# Pull, Otimizacao e Avaliacao de Prompts com LangChain e LangSmith

## Objetivo

Software que faz pull de prompts de baixa qualidade do LangSmith Prompt Hub, otimiza usando tecnicas avancadas de Prompt Engineering, faz push de volta e avalia a qualidade atingindo >= 0.9 em todas as 5 metricas (Helpfulness, Correctness, F1-Score, Clarity, Precision).

---

## Tecnicas Aplicadas (Fase 2)

### 1. Role Prompting

**Justificativa:** Definir uma persona clara de Product Manager Senior deu ao modelo contexto e autoridade para gerar User Stories profissionais. A persona inclui experiencia em metodologias ageis (Scrum, Kanban), garantindo que as respostas sigam padroes da industria.

**Como foi aplicada:**
- System prompt define: "Voce e um Product Manager Senior especializado em metodologias ageis (Scrum/Kanban)"
- A persona influencia o tom profissional, a estrutura das User Stories e o nivel de detalhe tecnico

### 2. Few-shot Learning (Obrigatoria)

**Justificativa:** Few-shot e a tecnica mais eficaz para alinhar o formato de saida com o esperado. Ao fornecer 3 exemplos (2 simples + 1 medio), o modelo aprendeu exatamente o formato, nivel de detalhe e estrutura esperados para cada complexidade.

**Como foi aplicada:**
- **Exemplo 1 (Simples - UI):** Bug do botao "Adicionar ao Carrinho" - mostra User Story concisa com 5 criterios de aceitacao
- **Exemplo 2 (Simples - dashboard):** Bug de contagem errada - mostra outra variacao de bug simples para o modelo generalizar
- **Exemplo 3 (Medio - API):** Bug de webhook com HTTP 500 - mostra User Story com criterios + Contexto Tecnico

### 3. Chain of Thought (CoT)

**Justificativa:** Analise de bugs requer raciocinio estruturado. O CoT forca o modelo a classificar a complexidade, identificar a persona e extrair os dados ANTES de escrever a User Story, resultando em respostas mais completas e precisas.

**Como foi aplicada:**
- Processo de analise em 4 passos: Classificacao -> Persona -> Dados do bug -> User Story unificada
- O modelo analisa internamente cada bug antes de gerar a resposta

---

## Resultados Finais

### Metricas Atingidas (avaliacao com Gemini 2.5 Flash)

| Metrica       | v1 (Ruim)  | v2 (Otimizado) | Status   |
|---------------|------------|----------------|----------|
| Helpfulness   | ~0.45      | **0.95**       | Aprovado |
| Correctness   | ~0.52      | **0.94**       | Aprovado |
| F1-Score      | ~0.48      | **0.91**       | Aprovado |
| Clarity       | ~0.50      | **0.94**       | Aprovado |
| Precision     | ~0.46      | **0.96**       | Aprovado |
| **Media**     | ~0.48      | **0.9395**     | Aprovado |

### Output da avaliacao (`python src/evaluate.py`)

```
==================================================
Prompt: thiagogcf/bug_to_user_story_v2
==================================================

Métricas Derivadas:
  - Helpfulness: 0.95 ✓
  - Correctness: 0.94 ✓

Métricas Base:
  - F1-Score: 0.91 ✓
  - Clarity: 0.94 ✓
  - Precision: 0.96 ✓

--------------------------------------------------
📊 MÉDIA GERAL: 0.9395
--------------------------------------------------

✅ STATUS: APROVADO - Todas as métricas >= 0.9
```

### Links Publicos no LangSmith

- **Prompt v2 publico:** https://smith.langchain.com/hub/thiagogcf/bug_to_user_story_v2
- **Dataset publico (15 exemplos):** https://smith.langchain.com/public/54aca531-6c81-4fd5-bb6f-7fd6dacbd709/d

### Tracing detalhado (3 exemplos)

Cada link abaixo mostra a execucao completa do prompt v2 sobre um bug do dataset, incluindo system prompt, input, output gerado e tokens consumidos:

1. **Trace 1:** https://smith.langchain.com/public/f61f0424-5f25-4db2-9733-a556d5a3c094/r
2. **Trace 2:** https://smith.langchain.com/public/31ac400b-341f-4660-8b93-5dcfc9a4fa11/r
3. **Trace 3:** https://smith.langchain.com/public/d4d326ca-d70b-44a5-9f69-3afc8383d592/r

### Principais melhorias v1 -> v2

- **Persona definida:** De "assistente generico" para "Product Manager Senior"
- **Exemplos concretos:** De zero exemplos para 3 exemplos (2 simples + 1 medio)
- **Formato estruturado:** De formato livre para Given-When-Then com secoes claras
- **Classificacao de complexidade:** Sistema adapta nivel de detalhe ao bug
- **Tratamento de edge cases:** Regras explicitas sobre formato, anti-alucinacao e separacao System vs User

### Processo de Iteracao

Foram realizadas multiplas iteracoes ate atingir o resultado:

1. **Iteracao 1:** Prompt basico com persona + 1 exemplo. Scores ~0.85
2. **Iteracao 2:** Adicionado classificacao por complexidade. Clarity subiu para 0.90
3. **Iteracao 3:** Adicionado regras anti-alucinacao. Precision melhorou
4. **Iteracao 4:** Removido prefixos markdown e ajustado formato para evitar "User Story:" labels
5. **Iteracao 5:** Adicionado instrucoes para gerar UMA user story unificada para bugs complexos
6. **Iteracao final (Gemini):** Migrado de OpenAI para Gemini 2.5 Flash. Todas as metricas passaram de 0.90

A maior parte do esforco foi em garantir que o output seguisse exatamente o formato esperado pelo avaliador, especialmente para bugs simples (5 criterios diretos) e complexos (uma user story unificada com seções === SECOES ===).

---

## Como Executar

### Pre-requisitos

- Python 3.9+ (testado com 3.12)
- Conta gratuita no [LangSmith](https://smith.langchain.com/)
- API Key gratuita do [Google AI Studio](https://aistudio.google.com/app/apikey)

### Instalacao

```bash
# Clonar repositorio
git clone https://github.com/Thiagogcf/mba-ia-pull-evaluation-prompt.git
cd mba-ia-pull-evaluation-prompt

# Criar e ativar ambiente virtual (Python 3.12 recomendado)
python3.12 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate

# Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt
```

### Configuracao

```bash
# Copiar template de variaveis de ambiente
cp .env.example .env

# Editar .env com suas credenciais:
# - LANGSMITH_API_KEY (criar em https://smith.langchain.com -> Settings -> API Keys)
# - USERNAME_LANGSMITH_HUB (seu handle do LangSmith Hub)
# - GOOGLE_API_KEY (criar em https://aistudio.google.com/app/apikey)
```

### Execucao

```bash
# 1. Pull dos prompts iniciais (v1)
python src/pull_prompts.py

# 2. Push dos prompts otimizados (v2)
python src/push_prompts.py

# 3. Avaliacao com 15 exemplos
python src/evaluate.py

# 4. Testes de validacao do prompt
pytest tests/test_prompts.py -v
```

---

## Estrutura do Projeto

```
mba-ia-pull-evaluation-prompt/
├── .env.example              # Template das variaveis de ambiente
├── requirements.txt          # Dependencias Python
├── README.md                 # Este arquivo
│
├── prompts/
│   ├── bug_to_user_story_v1.yml  # Prompt inicial (baixa qualidade)
│   └── bug_to_user_story_v2.yml  # Prompt otimizado
│
├── datasets/
│   └── bug_to_user_story.jsonl   # 15 exemplos de bugs (5 simples, 7 medios, 3 complexos)
│
├── src/
│   ├── pull_prompts.py       # Pull do LangSmith Hub (implementado)
│   ├── push_prompts.py       # Push ao LangSmith Hub (implementado)
│   ├── evaluate.py           # Avaliacao automatica
│   ├── metrics.py            # 5 metricas implementadas
│   └── utils.py              # Funcoes auxiliares
│
└── tests/
    └── test_prompts.py       # 6 testes de validacao (implementados)
```

---

## Modelos Utilizados

Foi usado o **Google Gemini 2.5 Flash** (gratuito) tanto para geracao quanto para avaliacao, conforme recomendado pelo desafio na opcao Gemini.

```env
LLM_PROVIDER=google
LLM_MODEL=gemini-2.5-flash
EVAL_MODEL=gemini-2.5-flash
```

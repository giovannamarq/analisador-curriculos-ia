# 🤖 ATS Inteligente — Analisador e Otimizador de Currículos com IA

Este é um sistema inteligente de triagem e otimização de currículos baseado em **Processamento de Linguagem Natural (PLN)** e Modelos de Linguagem de Grande Escala (LLMs). A aplicação realiza o cruzamento de dados contextuais (*Match Making*) entre o perfil profissional do candidato (extraído de arquivos PDF) e os requisitos técnicos de uma vaga de emprego, gerando insights automatizados de aderência e melhorias.

---

## 🚀 Funcionalidades Mapeadas

* **Pipeline de Extração de Texto:** Processamento automatizado de arquivos PDF estruturados utilizando a biblioteca `pypdf`.
* **Análise de Aderência (Match Making):** Algoritmo baseado em IA que calcula a porcentagem de compatibilidade com a vaga e separa pontos fortes e lacunas técnicas (*skills* faltantes).
* **Engenharia de Prompt Avançada:** Instruções de sistema que geram recomendações acionáveis de melhoria de portfólio e reformulam dinamicamente o resumo profissional do candidato para passar pelos filtros automáticos de RH (ATS).
* **Interface Web Responsiva:** Front-end simples e intuitivo desenvolvido com `Streamlit`, permitindo uploads e interações em tempo real.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3.13** (Linguagem base)
* **Streamlit** (Interface gráfica do usuário)
* **Google Gemini 2.5 Flash** (Modelo de IA Generativa)
* **LangChain** (Framework de orquestração de IA)
* **PyPDF** (Extração de dados de documentos)

---

## 🔧 Como Executar o Projeto Localmente

### 1. Clonar o repositório
```bash
### 1. Clonar o repositório
```bash
git clone [https://github.com/giovannamarq/analisador-curriculos-ia.git](https://github.com/giovannamarq/analisador-curriculos-ia.git)
cd analisador-curriculos-ia

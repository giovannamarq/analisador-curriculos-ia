import os
import streamlit as st 
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI

# Configuração segura da API
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = st.secrets.get("GOOGLE_API_KEY", "")
    
def extrair_texto_curriculo(arquivo_upload):
    """Lê o arquivo PDF enviado pelo Streamlit e extrai o texto."""
    try:
        leitor = PdfReader(arquivo_upload)
        texto = ""
        for pagina in leitor.pages:
            texto += pagina.extract_text() or ""
        return texto
    except Exception as e:
        st.error(f"Erro ao ler o arquivo PDF: {e}")
        return None

def analisar_aderencia(texto_curriculo, descricao_vaga):
    """Envia os dados para o Gemini estruturar a análise."""
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.3)
    
    prompt = f"""
    Você é um Engenheiro de IA especializado em Recrutamento, Seleção e ATS.
    Análise o currículo em relação à vaga e gere um relatório estruturado.

    --- DESCRIÇÃO DA VAGA ---
    {descricao_vaga}

    --- CURRÍCULO DO CANDIDATO ---
    {texto_curriculo}

    --- INSTRUÇÕES DE SAÍDA ---
    Gere o resultado exatamente no seguinte formato:

    📊 **COMPATIBILIDADE**: [Insira uma porcentagem de 0% a 100%]

    ✅ **PONTOS FORTES**:
    - [Lista de pontos fortes]

    ❌ **HABILIDADES FALTANTES**:
    - [Lista de lacunas]

    💡 **SUGESTÕES DE MELHORIA**:
    - [Lista de melhorias]

    🚀 **RESUMO PROFISSIONAL OTIMIZADO**:
    [Escreva o resumo de impacto focado na vaga]
    """
    resposta = llm.invoke(prompt)
    return resposta.content

# === INTERFACE WEB COM STREAMLIT ===
st.set_page_config(page_title="ATS AI Matcher", page_icon="🤖", layout="centered")

st.title("🤖 ATS Inteligente — Analisador de Currículos")
st.write("Suba o currículo em PDF, cole a vaga desejada e veja o casamento de dados acontecer com IA.")

st.divider()

arquivo_pdf = st.file_uploader("📂 Faça o upload do seu currículo (PDF)", type=["pdf"])

vaga_texto = st.text_area("📝 Cole aqui a descrição completa da vaga", height=200, placeholder="Requisitos, atividades, diferenciais...")

if st.button("🚀 Analisar Compatibilidade", type="primary"):
    if not arquivo_pdf:
        st.warning("⚠️ Por favor, envie um arquivo PDF do seu currículo.")
    elif not vaga_texto.strip():
        st.warning("⚠️ Por favor, cole a descrição da vaga para análise.")
    else:
        with st.spinner("🧠 Cruzando dados contextuais com IA... Aguarde."):
            # Executa a extração e a chamada do modelo
            texto_cv = extrair_texto_curriculo(arquivo_pdf)
            
            if texto_cv:
                relatorio = analisar_aderencia(texto_cv, vaga_texto)
                
                st.success("✅ Análise concluída com sucesso!")
                st.divider()
                st.markdown(relatorio)
import os
import streamlit as st
from pypdf import PdfReader
from langchain_google_genai import ChatGoogleGenerativeAI
from PIL import Image

# Configuração segura da API
if "GOOGLE_API_KEY" not in os.environ:
    os.environ["GOOGLE_API_KEY"] = st.secrets.get("GOOGLE_API_KEY", "")

def extrair_texto_curriculo(arquivo_upload):
    """Lê o arquivo PDF enviado e extrai o texto."""
    try:
        leitor = PdfReader(arquivo_upload)
        texto = ""
        for pagina in leitor.pages:
            texto += pagina.extract_text() or ""
        return texto
    except Exception as e:
        st.error(f"Erro ao ler o arquivo PDF: {e}")
        return None

def analisar_aderencia(texto_curriculo, descricao_vaga_texto, imagem_vaga=None):
    """Envia o currículo e a descrição da vaga (texto ou imagem) para o Gemini."""
    # Temperatura em 0.0 para diminuir a variação de notas que você notou!
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", temperature=0.0)
    
    prompt = f"""
    Você é um Engenheiro de IA especializado em Recrutamento, Seleção e ATS.
    Analise o currículo fornecido em relação à vaga apresentada (que pode estar em formato de texto abaixo ou contida na imagem anexa) e gere um relatório estruturado.

    --- CURRÍCULO DO CANDIDATO ---
    {texto_curriculo}

    --- DESCRIÇÃO DA VAGA (SE FORNECIDA EM TEXTO) ---
    {descricao_vaga_texto if descricao_vaga_texto.strip() else 'Descrição enviada via imagem anexa.'}

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
    
    # Se o usuário mandou uma imagem da vaga, enviamos o prompt + a imagem na estrutura multimodal
    if imagem_vaga:
        img = Image.open(imagem_vaga)
        conteudo = [prompt, img]
    else:
        conteudo = prompt
        
    resposta = llm.invoke(conteudo)
    return resposta.content

# === INTERFACE WEB COM STREAMLIT ===
st.set_page_config(page_title="ATS AI Matcher", page_icon="🤖", layout="centered")

st.title("🤖 ATS Inteligente — Analisador de Currículos")
st.write("Suba o currículo em PDF, cole a descrição da vaga OU envie um print dela!")

st.divider()

# Coluna 1: Upload do Currículo
arquivo_pdf = st.file_uploader("📂 Faça o upload do seu currículo (PDF)", type=["pdf"])

st.subheader("📝 Dados da Vaga")
# Criando abas para o usuário escolher como quer fornecer a vaga
aba_texto, aba_imagem = st.tabs(["Copiar/Colar Texto", "Enviar Print/Imagem"])

with aba_texto:
    vaga_texto = st.text_area("Cole aqui a descrição completa da vaga", height=150, placeholder="Requisitos, atividades...")

with aba_imagem:
    vaga_imagem = st.file_uploader("Suba o print da tela com os requisitos da vaga", type=["png", "jpg", "jpeg"])

# Botão de Ação
if st.button("🚀 Analisar Compatibilidade", type="primary"):
    if not arquivo_pdf:
        st.warning("⚠️ Por favor, envie um arquivo PDF do seu currículo.")
    elif not vaga_texto.strip() and not vaga_imagem:
        st.warning("⚠️ Por favor, insira o texto ou o print da vaga para análise.")
    else:
        with st.spinner("🧠 Cruzando dados contextuais e analisando imagens com IA... Aguarde."):
            texto_cv = extrair_texto_curriculo(arquivo_pdf)
            
            if texto_cv:
                relatorio = analisar_aderencia(texto_cv, vaga_texto, vaga_imagem)
                
                st.success("✅ Análise concluída com sucesso!")
                st.divider()
                st.markdown(relatorio)
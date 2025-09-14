from zipfile import ZipFile
import streamlit as st
import traditional.lark_parser
import traditional.utils
import llm.llm as llm


def trad_ui(excel_file):
    prelude = f"import pandas as pd\n\ndf = pd.read_excel('{excel_file.name}')\n"
    script = traditional.utils.transform_excel(
        excel_file, traditional.lark_parser.PandasTransformer
    )
    full_script = prelude + "\n".join(script)
    st.code(full_script, language="python")
    st.download_button(
        "Download equivalent Python script",
        data=full_script,
        file_name="traditional.py",
        mime="text/x-python",
    )


def llm_ui(excel_file):
    selected_provider = st.selectbox(
        "Select a provider", options=["Local", "Gemini", "OpenRouter"], index=None
    )
    with ZipFile(excel_file) as zf:
        with zf.open(zf.namelist()[0]) as file:
            excel_content = file.read().decode("utf-8")
    new_script = None
    with st.spinner("Generating Python code using LLM..."):
        if selected_provider == "Local":
            new_script = llm.generate_formula_ollama(
                llm.system_prompt_formula,
                excel_content,
            )
        elif selected_provider == "Gemini":
            new_script = llm.generate_formula_gemini(
                llm.system_prompt_formula,
                excel_content,
            )
        elif selected_provider == "OpenRouter":
            new_script = llm.generate_formula_openrouter(
                llm.system_prompt_formula, excel_content
            )
    if new_script:
        st.code(new_script, language="python")
        st.download_button(
            "Download equivalent Python script (LLM)",
            data=new_script,
            file_name="llm.py",
            mime="text/x-python",
        )


excel_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])
if excel_file:
    selected_compiler = st.selectbox(
        "Select a compiler", options=["Traditional", "LLM-powered", "Both"]
    )
    if selected_compiler == "Traditional":
        trad_ui(excel_file)
    elif selected_compiler == "LLM-powered":
        llm_ui(excel_file)
    else:
        st.subheader("Traditional Compiler Output")
        trad_ui(excel_file)
        st.subheader("LLM-powered Compiler Output")
        llm_ui(excel_file)

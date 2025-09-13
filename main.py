import streamlit as st
import traditional.lark_parser
import traditional.utils

def trad_ui(excel_file):
    prelude = f"import pandas as pd\n\ndf = pd.read_excel('{excel_file.name}')\n"
    script = traditional.utils.transform_excel(excel_file, traditional.lark_parser.PandasTransformer)
    full_script = prelude + "\n".join(script)
    st.code(full_script, language="python")
    st.download_button("Download Script", data=full_script, file_name="traditional.py", mime="text/x-python")
def llm_ui(excel_file):
    # new_script = traditional.utils.transform_excel(excel_file)
    st.code(new_script, language="python")
    st.download_button("Download Script", data=new_script, file_name="llm.py", mime="text/x-python")

excel_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])
if excel_file:
    selected_compiler = st.selectbox("Select a compiler", options=["Traditional", "LLM-powered", "Both"])
    if selected_compiler == "Traditional":
        trad_ui(excel_file)
    elif selected_compiler == "LLM-powered":
        llm_ui(excel_file)
    else:
        st.subheader("Traditional Compiler Output")
        trad_ui(excel_file)
        st.subheader("LLM-powered Compiler Output")
        llm_ui(excel_file)

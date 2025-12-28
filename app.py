import streamlit as st
import pandas as pd
from io import StringIO
from data_generation import generate_synthetic_data, refine_data
from data_query_module import text_to_sql, execute_sql_on_dataframe

# 1. PAGE CONFIG
st.set_page_config(page_title="GenAI Studio", layout="wide", page_icon="🔮")

# 2. INJECT CUSTOM CSS (The "Glass" Look)
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# Session State Setup
if "generated_df" not in st.session_state:
    st.session_state["generated_df"] = None
if "table_name" not in st.session_state:
    st.session_state["table_name"] = "my_table"

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.title("🔮 GenAI Studio")
    st.markdown("---")
    page = st.radio("Navigation", ["Data Generation", "Talk to your data"])
    st.markdown("---")
    st.caption("Powered by Gemini 2.0 Flash")

# --- ANIMATED HEADER ---
st.markdown("""
    <h1 style='text-align: center; margin-bottom: 50px;'>
        ✨ Synthetic Data Architect
    </h1>
""", unsafe_allow_html=True)

# --- PAGE 1: DATA GENERATION ---
if page == "Data Generation":
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("🛠 Configuration")
        # File Uploader
        uploaded_file = st.file_uploader("Upload Schema (.sql, .ddl)", type=['sql', 'txt', 'json', 'ddl'])
        
        # DDL Logic
        default_ddl = "CREATE TABLE employees (id INT, name VARCHAR(100), department VARCHAR(50), salary INT);"
        if uploaded_file is not None:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            ddl_input = stringio.read()
            st.success(f"loaded: {uploaded_file.name}")
        else:
            ddl_input = st.text_area("Or paste SQL here", value=default_ddl, height=150)

        # Controls
        temperature = st.slider("Creativity Level", 0.0, 2.0, 1.0)
        num_rows = st.slider("Rows to Generate", 5, 50, 10)
        
        if st.button("🚀 Generate Data", type="primary"):
            with st.spinner("AI is dreaming up data..."):
                df = generate_synthetic_data(ddl_input, num_rows, "", temperature)
                if not df.empty:
                    st.session_state["generated_df"] = df
                    st.rerun()
                else:
                    st.error("Generation failed.")

    with col2:
        st.subheader("💎 Data Preview")
        if st.session_state["generated_df"] is not None:
            st.dataframe(st.session_state["generated_df"], use_container_width=True, height=400)
            
            # Quick Edit Bar
            st.markdown("### ⚡ Quick Actions")
            c1, c2 = st.columns([3, 1])
            with c1:
                edit_instruction = st.text_input("Instruct AI to change data...", placeholder="e.g. Make all salaries higher than 50k")
            with c2:
                st.write("") # Spacer
                st.write("") # Spacer
                if st.button("Apply"):
                    with st.spinner("Refining..."):
                        new_df = refine_data(st.session_state["generated_df"], edit_instruction)
                        st.session_state["generated_df"] = new_df
                        st.rerun()
        else:
            st.info("👈 Configure settings and click Generate to see the magic.")

# --- PAGE 2: TALK TO YOUR DATA ---
elif page == "Talk to your data":
    
    if st.session_state["generated_df"] is None:
        st.warning("⚠️ Please generate data in the first tab.")
    else:
        # Chat Interface
        st.chat_message("assistant").write("I am ready to analyze your data. Ask me anything!")
        
        # Display Data snippet
        with st.expander("View Source Data"):
            st.dataframe(st.session_state["generated_df"])

        user_query = st.chat_input("Ask a question (e.g., Who has the highest salary?)")
        
        if user_query:
            st.chat_message("user").write(user_query)
            
            with st.spinner("Thinking..."):
                df = st.session_state["generated_df"]
                # 1. Convert Question to SQL
                sql = text_to_sql(user_query, "my_table", df.columns.tolist())
                clean_sql = sql.replace(st.session_state["table_name"], "my_table")
                
                # 2. Show SQL
                st.chat_message("assistant").code(sql, language="sql")
                
                # 3. Execute and Show Result
                result = execute_sql_on_dataframe(df, clean_sql)
                st.chat_message("assistant").dataframe(result)
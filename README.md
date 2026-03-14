# 🔮 GenAI Studio — Synthetic Data Architect

> Generate realistic synthetic data from a SQL schema and query it in plain English — powered by **Gemini 2.0 Flash** and **Streamlit**.

---

## ✨ Features

- **Data Generation** — Paste or upload a DDL/SQL schema and generate synthetic rows instantly
- **AI Refinement** — Instruct the AI to tweak the generated data (e.g. *"make all salaries above 50k"*)
- **Talk to Your Data** — Ask natural language questions; the app converts them to SQL and runs them live
- **Creativity Slider** — Control LLM temperature for varied or realistic data output

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| **LLM** | Google Gemini 2.0 Flash |
| **Frontend** | Streamlit |
| **Data** | Pandas + PandasSQL |
| **Modules** | `data_generation.py`, `data_query_module.py` |

---

## 📂 Project Structure

```
├── app.py                  # Main Streamlit UI
├── data_generation.py      # Synthetic data + refinement logic
├── data_query_module.py    # Text-to-SQL + DataFrame execution
├── style.css               # Custom glass UI styles
└── README.md
```

---

## 🚀 Getting Started

```bash
pip install streamlit pandas google-generativeai
streamlit run app.py
```

---

## 💡 Usage

1. **Data Generation tab** — Upload a `.sql`/`.ddl` schema or paste DDL directly → set row count → click **Generate**
2. Use **Quick Actions** to refine the data with a plain English instruction
3. Switch to **Talk to your data** → ask questions like *"Who has the highest salary?"*

---

## 📄 Example DDL

```sql
CREATE TABLE employees (
  id INT,
  name VARCHAR(100),
  department VARCHAR(50),
  salary INT
);
```

# 🧪 LLM Evaluation Dashboard

A tool that benchmarks and compares AI models on quality, hallucination risk, and latency.

## 🔍 Key Findings
- Llama3.2 1B (Meta) outperformed Gemma 2B (Google) on overall quality (63.5% vs 55.1%)
- Llama3.2 scored 16% higher on relevance, meaning it stays more on-topic
- Gemma showed lower hallucination risk (65% vs 62.2%), making it safer for sensitive use cases
- Both models had similar latency (~19-21 seconds) running locally on CPU

## 🛠️ Tech Stack
- Python
- Ollama (local AI models)
- Streamlit (dashboard)
- Pandas (data processing)
- Plotly (charts)

## 🤖 Models Compared
- Llama3.2 1B — Meta
- Gemma 2B — Google

## 🚀 How to Run
1. Install Ollama and pull models: `ollama pull llama3.2:1b` and `ollama pull gemma:2b`
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `streamlit run app.py`
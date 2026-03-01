# app.py
# This is the DASHBOARD — the visual interface of your project.
# Run it with: streamlit run app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import os

from evaluator import run_full_evaluation, save_results, load_results

# ─────────────────────────────────────────────
# Page Config
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="LLM Evaluation Dashboard",
    page_icon="🧪",
    layout="wide"
)

st.title("🧪 LLM Evaluation Dashboard")
st.markdown("*Compare AI models on quality, hallucination risk, cost, and speed*")
st.divider()

# ─────────────────────────────────────────────
# Sidebar Controls
# ─────────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Controls")
    
    results_file = "eval_results.json"
    results_exist = os.path.exists(results_file)
    
    if results_exist:
        st.success("✅ Results file found")
        use_cached = st.radio(
            "Data source:",
            ["Use saved results", "Run fresh evaluation"],
            index=0
        )
    else:
        st.warning("No results yet. Run evaluation first.")
        use_cached = "Run fresh evaluation"
    
    run_button = st.button("▶️ Run Evaluation", type="primary", use_container_width=True)
    
    st.divider()
    st.markdown("**Filter Results**")

# ─────────────────────────────────────────────
# Load or Run Evaluation
# ─────────────────────────────────────────────
@st.cache_data
def get_cached_results():
    return load_results()

results = None

if run_button:
    if use_cached == "Use saved results" and results_exist:
        results = load_results()
        st.sidebar.success("Loaded from file!")
    else:
        with st.spinner("Running evaluation... this may take 1-2 minutes..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            def update_progress(pct, msg):
                progress_bar.progress(pct)
                status_text.text(msg)
            
            results = run_full_evaluation(progress_callback=update_progress)
            save_results(results)
            progress_bar.empty()
            status_text.empty()
            st.success(f"✅ Evaluation complete! {len(results)} results collected.")
            st.cache_data.clear()

elif results_exist:
    results = load_results()

# ─────────────────────────────────────────────
# Main Dashboard (only shows if results exist)
# ─────────────────────────────────────────────
if results:
    df = pd.DataFrame(results)
    df_success = df[df["status"] == "success"].copy()
    
    # Sidebar filters
    with st.sidebar:
        selected_models = st.multiselect(
            "Models",
            options=df_success["model_name"].unique().tolist(),
            default=df_success["model_name"].unique().tolist()
        )
        selected_categories = st.multiselect(
            "Categories",
            options=df_success["category"].unique().tolist(),
            default=df_success["category"].unique().tolist()
        )
    
    # Apply filters
    filtered = df_success[
        df_success["model_name"].isin(selected_models) &
        df_success["category"].isin(selected_categories)
    ]
    
    # ── Summary Cards ──
    st.subheader("📊 Summary by Model")
    summary = filtered.groupby("model_name").agg(
        Avg_Quality=("overall_quality", "mean"),
        Avg_Relevance=("relevance_score", "mean"),
        Avg_Hallucination=("hallucination_score", "mean"),
        Avg_Latency=("latency_seconds", "mean"),
        Total_Cost=("cost_usd", "sum"),
        Questions_Tested=("question_id", "count")
    ).round(3).reset_index()
    
    cols = st.columns(len(summary))
    for i, row in summary.iterrows():
        with cols[i]:
            st.metric("Model", row["model_name"])
            st.metric("Overall Quality", f"{row['Avg_Quality']:.2%}")
            st.metric("Relevance", f"{row['Avg_Relevance']:.2%}")
            st.metric("Hallucination Safety", f"{row['Avg_Hallucination']:.2%}")
            st.metric("Avg Latency", f"{row['Avg_Latency']:.2f}s")
            st.metric("Total Cost", f"${row['Total_Cost']:.4f}")
    
    st.divider()
    
    # ── Bar Charts ──
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Quality Scores by Model")
        fig = px.bar(
            summary,
            x="model_name",
            y=["Avg_Quality", "Avg_Relevance", "Avg_Hallucination"],
            barmode="group",
            color_discrete_sequence=["#2ecc71", "#3498db", "#e74c3c"],
            labels={"value": "Score (0-1)", "model_name": "Model", "variable": "Metric"}
        )
        fig.update_layout(yaxis_range=[0, 1])
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("⚡ Cost vs Quality Tradeoff")
        fig2 = px.scatter(
            summary,
            x="Total_Cost",
            y="Avg_Quality",
            text="model_name",
            size="Avg_Latency",
            color="model_name",
            labels={"Total_Cost": "Total Cost (USD)", "Avg_Quality": "Avg Quality Score"},
            title="Cost vs Quality (bubble size = latency)"
        )
        fig2.update_traces(textposition="top center")
        st.plotly_chart(fig2, use_container_width=True)
    
    st.divider()
    
    # ── Performance by Category ──
    st.subheader("📂 Performance by Category")
    cat_summary = filtered.groupby(["model_name", "category"]).agg(
        Avg_Quality=("overall_quality", "mean")
    ).round(3).reset_index()
    
    fig3 = px.bar(
        cat_summary,
        x="category",
        y="Avg_Quality",
        color="model_name",
        barmode="group",
        labels={"Avg_Quality": "Avg Quality Score", "category": "Category"}
    )
    fig3.update_layout(yaxis_range=[0, 1])
    st.plotly_chart(fig3, use_container_width=True)
    
    st.divider()
    
    # ── Question-Level Explorer ──
    st.subheader("🔍 Question-Level Explorer")
    st.markdown("Compare model responses side-by-side for each question.")
    
    questions = filtered["question"].unique().tolist()
    selected_q = st.selectbox("Select a question:", questions)
    
    q_data = filtered[filtered["question"] == selected_q]
    
    # Show ideal answer
    ideal = q_data["ideal_answer"].iloc[0]
    st.info(f"**Ideal Answer:** {ideal}")
    
    # Show each model's response and scores
    response_cols = st.columns(len(q_data))
    for i, (_, row) in enumerate(q_data.iterrows()):
        with response_cols[i]:
            st.markdown(f"**{row['model_name']}**")
            st.markdown(f"_{row['response_text']}_")
            st.markdown("---")
            st.metric("Quality", f"{row['overall_quality']:.2%}")
            st.metric("Relevance", f"{row['relevance_score']:.2%}")
            st.metric("Hallucination Safety", f"{row['hallucination_score']:.2%}")
            st.metric("Latency", f"{row['latency_seconds']:.2f}s")
            st.metric("Cost", f"${row['cost_usd']:.6f}")
    
    st.divider()
    
    # ── Raw Data Table ──
    st.subheader("📋 Full Results Table")
    display_cols = ["question_id", "category", "question", "model_name",
                    "overall_quality", "relevance_score", "hallucination_score",
                    "latency_seconds", "cost_usd", "word_count"]
    st.dataframe(filtered[display_cols].sort_values(["question_id", "model_name"]),
                 use_container_width=True)
    
    # Download button
    csv = filtered[display_cols].to_csv(index=False)
    st.download_button(
        label="⬇️ Download Results as CSV",
        data=csv,
        file_name="llm_eval_results.csv",
        mime="text/csv"
    )

else:
    st.info("👈 Click **Run Evaluation** in the sidebar to get started.")
    st.markdown("""
    ### What this dashboard does:
    - Sends 15 test questions to Llama3 running locally via Ollama
    - Scores each response on **relevance**, **hallucination risk**, and **quality**
    - Tracks **latency** for each call
    - Shows how **prompt engineering alone** changes model performance
    
    ### Prompt configurations being tested:
    - Llama3 — Simple Prompt
    - Llama3 — Expert Prompt  
    - Llama3 — Concise Prompt
    
    ### Requirements:
    - Ollama must be running on your machine
    - Llama3 model must be pulled (`ollama pull llama3`)
    """)

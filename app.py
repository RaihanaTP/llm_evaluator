# app.py

import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os

from evaluator import run_full_evaluation, save_results, load_results

st.set_page_config(page_title="LLM Evaluation Dashboard", page_icon="🧪", layout="wide")

st.title(" LLM Evaluation Dashboard")
st.markdown("*Compare AI models on quality, hallucination risk, and relevance*")
st.divider()

# Sidebar
with st.sidebar:
    st.header("⚙️ Controls")
    results_file = "eval_results.json"
    results_exist = os.path.exists(results_file)

    if results_exist:
        st.success("✅ Results file found")
        use_cached = st.radio("Data source:", ["Use saved results", "Run fresh evaluation"], index=0)
    else:
        st.warning("No results yet. Run evaluation first.")
        use_cached = "Run fresh evaluation"

    run_button = st.button("▶️ Run Evaluation", type="primary", use_container_width=True)
    st.divider()
    st.markdown("**Filter Results**")

results = None

if run_button:
    if use_cached == "Use saved results" and results_exist:
        results = load_results()
        st.sidebar.success("Loaded!")
    else:
        with st.spinner("Running evaluation... this may take a few minutes..."):
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

elif results_exist:
    results = load_results()

if results:
    df = pd.DataFrame(results)
    df = df[df["status"] == "success"].copy()

    with st.sidebar:
        selected_models = st.multiselect(
            "Models",
            options=df["model_name"].unique().tolist(),
            default=df["model_name"].unique().tolist()
        )
        selected_categories = st.multiselect(
            "Categories",
            options=df["category"].unique().tolist(),
            default=df["category"].unique().tolist()
        )

    df = df[
        df["model_name"].isin(selected_models) &
        df["category"].isin(selected_categories)
    ]

    st.subheader("📊 Model Summary")
    summary = df.groupby("model_name").agg(
        Avg_Quality=("overall_quality", "mean"),
        Avg_Relevance=("relevance_score", "mean"),
        Avg_Hallucination=("hallucination_score", "mean"),
        Avg_Latency=("latency_seconds", "mean"),
    ).round(3).reset_index()

    cols = st.columns(len(summary))
    for i, row in summary.iterrows():
        with cols[i]:
            st.markdown(f"### {row['model_name']}")
            st.metric("Overall Quality", f"{row['Avg_Quality']:.2%}")
            st.metric("Relevance", f"{row['Avg_Relevance']:.2%}")
            st.metric("Hallucination Safety", f"{row['Avg_Hallucination']:.2%}")
            st.metric("Avg Latency", f"{row['Avg_Latency']:.2f}s")

    st.divider()

    st.subheader("📂 Performance by Category")
    cat_summary = df.groupby(["model_name", "category"]).agg(
        Avg_Quality=("overall_quality", "mean")
    ).round(3).reset_index()

    fig = px.bar(
        cat_summary,
        x="category",
        y="Avg_Quality",
        color="model_name",
        barmode="group",
        labels={"Avg_Quality": "Avg Quality Score", "category": "Category", "model_name": "Model"},
        color_discrete_sequence=["#2ecc71", "#3498db"]
    )
    fig.update_layout(yaxis_range=[0, 1], legend_title="Model")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.info("👈 Click **Run Evaluation** in the sidebar to get started.")
    st.markdown("""
    ### What this dashboard does:
    - Tests AI models from Meta and Google on 15 real-world questions
    - Scores each model on quality, relevance, and hallucination risk
    - Shows performance broken down by category

    ### Models being tested:
    - Llama3.2 1B (Meta)
    - Gemma 2B (Google)

    ### Requirements:
    - Ollama must be running
    - Models pulled: ollama pull llama3.2:1b and ollama pull gemma:2b
    """)
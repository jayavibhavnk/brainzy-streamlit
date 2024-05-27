import streamlit as st
import pandas as pd
import plotly.express as px

# Metrics for GraphRAG and VDB RAG
metrics = {
    'Metric': [
        'context_precision', 'faithfulness', 'answer_relevancy', 
        'context_recall', 'context_relevancy', 'answer_correctness', 
        'answer_similarity', 'Inference_time'
    ],
    'GraphRAG': [
        0.8687, 0.9375, 0.9106, 1.0000, 0.0464, 0.6676, 0.9532, 1.0000
    ],
    'VDB RAG': [
        0.8792, 0.9242, 0.9361, 1.0000, 0.0445, 0.7614, 0.9525, 0.4513
    ]
}

# Create a DataFrame
df = pd.DataFrame(metrics)

# Set the title of the app
st.title('Comparison of RAG Techniques: Vector Database vs GraphRAG')

# Display the DataFrame
st.write("## Metrics Comparison")
st.dataframe(df)

# Interactive bar chart for metrics comparison
st.write("## Metrics Comparison Bar Chart")
fig = px.bar(df, x='Metric', y=['GraphRAG', 'VDB RAG'], barmode='group', title="GraphRAG vs VDB RAG Metrics Comparison")
st.plotly_chart(fig)

# Interactive radar chart for metrics comparison
st.write("## Metrics Comparison Radar Chart")
fig_radar = px.line_polar(df, r=['GraphRAG', 'VDB RAG'], theta='Metric', line_close=True,
                          title="GraphRAG vs VDB RAG Metrics Comparison (Radar Chart)")
fig_radar.update_traces(fill='toself')
st.plotly_chart(fig_radar)

# Interactive line chart for inference time comparison
st.write("## Inference Time Comparison")
fig_time = px.line(df, x='Metric', y=['GraphRAG', 'VDB RAG'], title="Inference Time Comparison",
                   labels={'value': 'Inference Time', 'Metric': 'Metrics'})
st.plotly_chart(fig_time)

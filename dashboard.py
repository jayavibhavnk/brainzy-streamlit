import streamlit as st
import plotly.graph_objects as go
import numpy as np

def plot_comparison(vdb_rag, graph_rag, metrics, selected_metrics, plot_type):
    if plot_type == 'Bar Chart':
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=metrics,
            y=vdb_rag,
            name='VDB-RAG',
            marker_color='indianred'
        ))
        fig.add_trace(go.Bar(
            x=metrics,
            y=graph_rag,
            name='GraphRAG',
            marker_color='lightsalmon'
        ))

        fig.update_layout(
            title='Comparison of RAG Techniques (Bar Chart)',
            xaxis_title='Metrics',
            yaxis_title='Scores',
            barmode='group'
        )

        st.plotly_chart(fig)

    elif plot_type == 'Scatter Plot':
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=vdb_rag,
            y=graph_rag,
            mode='markers',
            marker=dict(
                color='blue',
                size=10,
                opacity=0.5
            ),
            name='RAG Techniques'
        ))

        fig.update_layout(
            title='Comparison of RAG Techniques (Scatter Plot)',
            xaxis_title='VDB-RAG',
            yaxis_title='GraphRAG'
        )

        st.plotly_chart(fig)

def main():
    st.set_page_config(page_title='RAG Techniques Comparison', layout='wide')

    st.title('RAG Techniques Comparison')
    st.markdown('### Analyze and Compare Retrieval Augmented Generation (RAG) Techniques')

    st.sidebar.header('Customize Plot')

    metrics = ['Context Precision', 'Faithfulness', 'Answer Relevancy', 'Context Recall', 'Context Relevancy', 'Answer Correctness', 'Answer Similarity', 'Inference Time']

    selected_metrics = st.sidebar.multiselect('Select Metrics', metrics, default=['Context Precision', 'Faithfulness'])
    plot_type = st.sidebar.selectbox('Select Plot Type', ['Bar Chart', 'Scatter Plot'])

    vdb_rag = [0.8792, 0.9242, 0.9361, 1.0, 0.0445, 0.7614, 0.9525, 0.4513]
    graph_rag = [0.8687, 0.9375, 0.9106, 1.0, 0.0464, 0.6676, 0.9532, 1.0]

    plot_comparison(vdb_rag, graph_rag, metrics, selected_metrics, plot_type)

if __name__ == "__main__":
    main()

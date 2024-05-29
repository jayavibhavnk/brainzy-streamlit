import streamlit as st
import plotly.graph_objects as go
import numpy as np

def plot_comparison(data_rag, data_vector_db_rag, selected_metrics, plot_type):
    rag_values = [data_rag[metric] for metric in selected_metrics]
    vector_db_rag_values = [data_vector_db_rag[metric] for metric in selected_metrics]

    if plot_type == 'Bar Chart':
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=selected_metrics,
            y=vector_db_rag_values,
            name='Vector DB RAG',
            marker_color='indianred'
        ))
        fig.add_trace(go.Bar(
            x=selected_metrics,
            y=rag_values,
            name='Graph RAG',
            marker_color='lightsalmon'
        ))

        fig.update_layout(
            title='Comparison of RAG Techniques (Bar Chart)',
            xaxis_title='Metrics',
            yaxis_title='Scores',
            barmode='group'
        )

        st.plotly_chart(fig)

    elif plot_type == 'Polar Scatter Plot':
        fig = go.Figure()

        fig.add_trace(go.Scatterpolar(
            r=vector_db_rag_values,
            theta=selected_metrics,
            fill='toself',
            name='Vector DB RAG',
            line_color='blue',
            marker=dict(color='blue')
        ))
        fig.add_trace(go.Scatterpolar(
            r=rag_values,
            theta=selected_metrics,
            fill='toself',
            name='RAG Techniques',
            line_color='red',
            marker=dict(color='red')
        ))

        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 1]
                )
            ),
            showlegend=True,
            title='Comparison of RAG Techniques (Polar Scatter Plot)',
            width=800
        )

        st.plotly_chart(fig)

    elif plot_type == 'Line Plot':
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=selected_metrics,
            y=vector_db_rag_values,
            mode='lines+markers',
            name='Vector DB RAG',
            line=dict(color='blue', width=2),
            marker=dict(color='blue')
        ))
        fig.add_trace(go.Scatter(
            x=selected_metrics,
            y=rag_values,
            mode='lines+markers',
            name='RAG Techniques',
            line=dict(color='red', width=2),
            marker=dict(color='red')
        ))

        fig.update_layout(
            title='Comparison of RAG Techniques (Line Plot)',
            xaxis_title='Metrics',
            yaxis_title='Scores',
            showlegend=True
        )

        st.plotly_chart(fig)

def main():
    st.set_page_config(page_title='RAG Techniques Comparison', layout='wide')

    st.title('RAG Techniques Comparison')
    st.markdown('### Analyze and Compare Retrieval Augmented Generation (RAG) Techniques')

    st.sidebar.header('Customize Plot')

    selected_metrics = ['context_precision', 'faithfulness', 'answer_relevancy', 'context_recall', 'context_relevancy', 'answer_correctness', 'answer_similarity', 'Inference_time']
    plot_type = st.sidebar.selectbox('Select Plot Type', ['Bar Chart', 'Polar Scatter Plot', 'Line Plot'])

    data_rag = {
        'context_precision': 0.8687,
        'faithfulness': 0.9375,
        'answer_relevancy': 0.9106,
        'context_recall': 1.0,
        'context_relevancy': 0.0464,
        'answer_correctness': 0.6676,
        'answer_similarity': 0.9532,
        'Inference_time': 1.0
    }

    data_vector_db_rag = {
        'context_precision': 0.8792,
        'faithfulness': 0.9242,
        'answer_relevancy': 0.9361,
        'context_recall': 1.0,
        'context_relevancy': 0.0445,
        'answer_correctness': 0.7614,
        'answer_similarity': 0.9525,
        'Inference_time': 0.4513
    }

    plot_comparison(data_rag, data_vector_db_rag, selected_metrics, plot_type)

if __name__ == "__main__":
    main()

import streamlit as st
import requests
from bs4 import BeautifulSoup
import base64
from groq import Groq
from googlesearch import search
from youtube_search import YoutubeSearch
import json

# Initialize Groq client
client = Groq(api_key=st.secrets.GROQ_API_KEY)

def chat_groq(query):
    """Query Groq's AI model for responses"""
    response = client.chat.completions.create(
        messages=[{"role": "user", "content": query}],
        model="mixtral-8x7b-32768",
        temperature=1.1,
        max_tokens=2048
    )
    return response.choices[0].message.content

def scrape_website(url):
    """Scrape website content and structure"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    paragraphs = soup.find_all('p')

    content = []
    for heading, paragraph in zip(headings, paragraphs):
        content.append(heading.text.strip())
        content.append(paragraph.text.strip())

    return {"content": content[:20]}  # Limit to first 20 elements

def create_prompt_template(text_from_website):
    """Create structured prompt for mind mapping"""
    structure_guide = """
    Create a hierarchical node structure in JSON format with:
    - Main headings
    - Sub-headings 
    - Keywords (1-7 word phrases)
    Include 5-20 headings each with multiple keywords.
    
    Format example:
    {
        "Main Topic": {
            "Sub-Topic 1": {"keyword1": {}, "keyword2": {}},
            "Sub-Topic 2": {"keyword1": {}, "keyword2": {}}
        }
    }"""
    
    return f"{text_from_website}\n\n{structure_guide}"

def create_mindmap(json_data):
    """Convert JSON structure to Mermaid syntax"""
    mindmaps = []
    for heading in json_data.keys():
        mermaid_code = "mindmap\n"
        clean_heading = heading.replace('(', '').replace(')', '')
        mermaid_code += f"  root({clean_heading})\n"
        
        for sub_heading, keywords in json_data[heading].items():
            mermaid_code += f"    {sub_heading}\n"
            for keyword in keywords.keys():
                mermaid_code += f"      {keyword}\n"
        
        mindmaps.append(mermaid_code)
    return mindmaps

def generate_kroki_diagram(code, diagram_type="mermaid"):
    """Generate SVG diagram using Kroki API"""
    response = requests.post(
        f"https://kroki.io/{diagram_type}/svg",
        json={"diagram_source": code}
    )
    return response.text if response.status_code == 200 else None

def create_mindmap_kroki(text):
    """Full mindmap generation pipeline"""
    truncated_text = str(text)[:2048]
    prompt = create_prompt_template(truncated_text)
    
    try:
        json_response = chat_groq(prompt)
        json_start = json_response.find('{')
        json_end = json_response.rfind('}') + 1
        parsed_data = json.loads(json_response[json_start:json_end])
        
        mermaid_diagrams = create_mindmap(parsed_data)
        svg_output = ""
        
        for diagram in mermaid_diagrams:
            svg = generate_kroki_diagram(diagram)
            if svg:
                svg_output += svg
                
        return svg_output
    
    except Exception as e:
        st.error(f"Error generating mindmap: {str(e)}")
        return None

def gen_links(query):
    """Generate relevant web and YouTube links"""
    web_links = list(search(query, num_results=4))
    
    youtube_results = YoutubeSearch(query, max_results=3).to_dict()
    youtube_links = [f"https://youtube.com{result['url_suffix']}" 
                     for result in youtube_results]
    
    return web_links, youtube_links

def render_svg(svg):
    """Display SVG in Streamlit"""
    b64 = base64.b64encode(svg.encode()).decode()
    html = f'<img src="data:image/svg+xml;base64,{b64}"/>'
    st.write(html, unsafe_allow_html=True)

def main():
    """Main application interface"""
    st.title("🧠 Brainzy - Instant Knowledge Organizer")
    st.markdown("Transform any content into structured mindmaps using Groq's AI!")
    
    input_method = st.radio("Input method:", 
                           ("Text Input", "Website URL"))
    
    user_input = ""
    if input_method == "Text Input":
        user_input = st.text_area("Enter your content:", height=200)
    else:
        url = st.text_input("Enter website URL:")
        if url:
            user_input = scrape_website(url)
    
    if st.button("Generate Mindmap"):
        with st.spinner("Creating knowledge structure..."):
            # Generate content
            web_links, youtube_links = gen_links(str(user_input)[:100])
            mindmap_svg = create_mindmap_kroki(user_input)
            
            # Generate summary
            summary = chat_groq(f"Create 3 bullet points summarizing this: {str(user_input)[:2000]}")
            
            # Display results
            st.subheader("Visual Mindmap")
            if mindmap_svg:
                render_svg(mindmap_svg)
            else:
                st.warning("Could not generate visual diagram")
            
            st.subheader("Key Points")
            st.write(summary)
            
            st.subheader("Recommended Resources")
            st.markdown("#### Web Links:")
            for link in web_links:
                st.markdown(f"- [{link}]({link})")
            
            st.markdown("#### YouTube Videos:")
            for vid in youtube_links:
                st.markdown(f"- [{vid}]({vid})")

if __name__ == "__main__":
    main()

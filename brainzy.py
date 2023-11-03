import streamlit as st
import requests
from bs4 import BeautifulSoup
import requests
import base64
import googlesearch 
from youtube_search import YoutubeSearch
import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": "Bearer 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"}

OPENAI_API_KEY = st.secrets.OPENAI_API_KEY

def chat_openai(query):
    llm = ChatOpenAI(temperature=1.1, openai_api_key = OPENAI_API_KEY)
    prompt = ChatPromptTemplate.from_template(
        "{query}"
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    return (chain.run(query=query))


def scrape_website(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
    paragraphs = soup.find_all('p')

    all_text_and_headings = []

    for heading, paragraph in zip(headings, paragraphs):
        all_text_and_headings.append(heading.text.strip())
        all_text_and_headings.append(paragraph.text.strip())

    scraped_text = ""

    text = {}

    for idx in range(0, len(all_text_and_headings), 2):
        heading = all_text_and_headings[idx]
        paragraph = all_text_and_headings[idx + 1]
        text[heading] = paragraph

    return text


def create_prompt_template(text_from_website):
    sub_p = """for the above text create a tree node hierarchy for the above content
        in this format
        heading
        sub headings
        keywords
        extract as many keywords and sub headings as possible
        there should be about 5 to 20 headings and each of them should have multiple keywords, keywords can be key phrases in the length of 1 word to 7 words
        , it should maintain a hierarchy
        should return in this json format

        example

        {"heading":
        {"sub-heading":
        {
        "keyword": {},
        },
        {"sub-heading 2":
        {
        "keyword": {},
        },

        }
        },
        }"""
    prompt = text_from_website + sub_p

    return prompt

def create_mindmap(json_file):
    headings = list(json_file.keys())
    # print(headings)
    mindmaps = []
    # mindmap = "mindmap"+"\n"
    for i in headings:
        mindmap = "mindmap"+"\n"
        nh = i.replace('(', '')
        nh = nh.replace(')', '')
        mindmap = mindmap + "  " + "root({})".format(nh) + "\n"
        sub_map = json_file[i]
        sub_headings = list(sub_map.keys())
        for j in sub_headings:
            mindmap = mindmap + "    " + j + '\n'
            items = list(sub_map[j].keys())
            for k in items:
                mindmap = mindmap + '      ' + k + '\n'
        mindmaps.append(mindmap)

    return mindmaps


def generate_kroki_diagram(diagram_code, diagram_type):
    kroki_api_url = "https://kroki.io"
    payload = {
        "diagram_source": diagram_code,
        "diagram_type": diagram_type,
    }
    response = requests.post(f"{kroki_api_url}/{diagram_type}/svg", json=payload)
    return response.text if response.status_code == 200 else None

def create_mindmap_kroki(text1):
    text1 = text1[:2048]
    prompt = create_prompt_template(text1)
    m = chat_openai(prompt)
    # m = chat_with_openai(prompt)
    newparse = m[m.find("{"):(len(m)-m[::-1].find('}'))]
    newparse = json.loads(newparse)
    # m = json.loads(m)
    m = create_mindmap(newparse)
    mermaid_svgs = ""
    try:
        for i in m:
            diagram_svg = generate_kroki_diagram(i, "mermaid")

            if diagram_svg:
                mermaid_svgs = mermaid_svgs + diagram_svg
            else:
                print("Diagram generation failed.")
        return mermaid_svgs
    except:
        print("error")
        return None

def generate_answer(data):
    pass

def gen_links(input_text):
    results = googlesearch.search(input_text)
    linklist = []
    for i in results:
      linklist.append(i)
    results = YoutubeSearch(input_text, max_results=3).to_dict()
    resultsfinal = ['https://youtube.com' + url['url_suffix'] for url in results]
    return linklist[:4], resultsfinal


def summarizer(data):
    payload = {"inputs":data}
    response = requests.post(API_URL, headers=headers, json=payload).json()
    return response[0]['summary_text']

        
def mindmapgen(data):
    #edit the svg data here
    svg_file_path = "sample.svg"
    with open(svg_file_path, "r") as svg_file:
        svg_content = svg_file.read()
    return svg_content

def headings(url):
    headings_content = scrape_website(url)
    headings = [heading for heading in headings_content.keys()]
    finalheading = ""
    for i in range(1,5):
        finalheading += headings[i] + " "
    return finalheading

def render_svg(svg):
    """Renders the given svg string."""
    b64 = base64.b64encode(svg.encode('utf-8')).decode("utf-8")
    html = r'<img src="data:image/svg+xml;base64,%s"/>' % b64
    st.write(html, unsafe_allow_html=True)

def main():
    st.title("Brainzy by Tl;DΣR")
    st.markdown("Generate Mindmaps and notes for any content!")

    # Input options: Text Input and URL Input
    option = st.radio("Choose an input option:", ("Direct Text Input", "URL Input"))

    if option == "Direct Text Input":
        mindmap_data = st.text_area("Enter your text:")

    else:
        url = st.text_input("Enter URL:")


    if st.button("Generate"):
        progress_bar = st.progress(0)
        if option == "URL Input":
            mindmap_data = scrape_website(url)
            glinks, ylinks = gen_links(headings(url))
            progress_bar.progress(30)
        else:
            glinks, ylinks = gen_links(mindmap_data[:10])
            progress_bar.progress(30)
        # mindmapvalue = mindmapgen(mindmap_data)
        mindmapvalue = create_mindmap_kroki(str(mindmap_data))
        progress_bar.progress(70)
        summarized_text = summarizer(str(mindmap_data))
        progress_bar.progress(100)
        st.write("Generated Mindmap:")
        render_svg(mindmapvalue)

        st.write("Summary:")
        st.write(summarized_text)

        st.write("Relevant Links")
        for i in glinks:
            st.write(i)

        st.write("Youtube Links")
        for i in ylinks:
            st.write(i)


        # question = st.text_input("Ask a question:")
        # if st.button("Ask"):
        #     st.text("Question: ")
        #     st.text("Answer: ")

        # # Answer the question (You will fill this logic)
        # if question:
        #     answer = generate_answer(question)
        #     st.text("Question: " + question)
        #     st.text("Answer: " + answer)

if __name__ == "__main__":
    main()

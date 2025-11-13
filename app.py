import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
import json
from dotenv import load_dotenv
from db import init_db, insert_text, last_five_runs
import os
load_dotenv()
init_db()
api_key=os.getenv("OPENAI_API_KEY")


st.title("Text summarizer")
st.write('Any text written can be summarized')
text=st.text_input("Enter text to summarize:")
summ=st.button("Summarize...")
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    openai_api_key=api_key,
    openai_api_base="https://openrouter.ai/api/v1"
)
def llm_summarize(text):
    prompt=ChatPromptTemplate.from_messages([('system',"You are a helpful assistant. Respond with JSON only."),('user',f'Summarize {text} and extract 3-5 keywords')])
    formatted_prompt=prompt.format()
    response=llm.invoke(formatted_prompt)
    raw_output = response.content.strip()
    if raw_output.startswith("```"):
        raw_output=raw_output.strip("`")
        raw_output=raw_output.replace("json", "", 1).strip()
    try:
        result=json.loads(raw_output)
    except:
        result = {"summary":raw_output, "keywords": []}
    return result

if summ and text.strip():
    with st.spinner("Generating summary..."):
        result = llm_summarize(text)
        st.subheader("Response:")
        st.json(result)
        insert_text(text, result)
else:
    st.info("Enter some text and click 'Summarize'")
with st.expander("Last 5 runs"):
    text=last_five_runs()
    for t in text:
        st.write("Input",t["input"])
        st.write("Output",t["output"])


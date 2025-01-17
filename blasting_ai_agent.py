# blasting_ai_agent.py
import openai
import pinecone
import json
import streamlit as st
import os

# Load API keys from Streamlit secrets or environment variables
openai.api_key = st.secrets["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"] if "OPENAI_API_KEY" in st.secrets else os.getenv("OPENAI_API_KEY")
pinecone_api_key = st.secrets["pcsk_4AD5o8_Aan16jdGUz2suKbfVLprdYxnc5x2ZTybempWVeAjoNUfQmRERkJGP1WPemnrThG"] if "PINECONE_API_KEY" in st.secrets else os.getenv("PINECONE_API_KEY")

if not openai.api_key or not pinecone_api_key:
    st.error("API keys missing! Set them in Streamlit secrets or environment variables.")
    st.stop()

# Initialize Pinecone client
pinecone.init(api_key=pinecone_api_key, environment="us-west1-gcp")

# Check if Pinecone index exists
index_name = "blasting-strategist"
if index_name not in pinecone.list_indexes():
    st.error(f"Pinecone index '{index_name}' not found. Available indexes: {pinecone.list_indexes()}")
    st.stop()

index = pinecone.Index(index_name)

# Function to load reports into the knowledge base
def load_reports(reports):
    for report in reports:
        response = openai.Embedding.create(input=report["content"], model="text-embedding-ada-002")
        vector = response["data"][0]["embedding"]
        index.upsert([(report["id"], vector, report)])

# Function to answer user queries
def ask_blasting_ai(query):
    query_embedding = openai.Embedding.create(input=query, model="text-embedding-ada-002")["data"][0]["embedding"]
    results = index.query(query_embedding, top_k=3, include_metadata=True)

    if not results.get("matches"):
        return "No relevant data found in the knowledge base."

    context = "\n\n".join([item["metadata"].get("content", "No content available") for item in results["matches"]])

    prompt = f"""
    You are a business strategist AI specialized in the mining and blasting industry.
    Based on the following knowledge base, provide a strategic answer to the question:
    
    Context:
    {context}
    
    Question: {query}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an expert in the mining and blasting industry."},
                  {"role": "user", "content": prompt}]
    )

    return response["choices"][0]["message"]["content"]

# Streamlit UI
def main():
    st.title("Blasting Business Strategist AI")
    st.write("Ask your AI agent about trends, competitors, and strategies in the mining & blasting industry.")
    
    query = st.text_input("Enter your question:")
    if st.button("Ask AI") and query:
        answer = ask_blasting_ai(query)
        st.write("## AI Response:")
        st.write(answer)

if __name__ == "__main__":
    main()

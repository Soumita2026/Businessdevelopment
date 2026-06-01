import streamlit as st
import os
from pathlib import Path
from dotenv import load_dotenv
import http.client
import json

# ==========================================
# 1. INITIALIZE ENVIRONMENT
# ==========================================
current_dir = Path(__file__).resolve().parent
env_path = current_dir / '.env'
load_dotenv(dotenv_path=env_path)

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")


# ==========================================
# 2. ROBUST CORE API FUNCTIONS
# ==========================================
def google_search(query):
    """Performs a direct API call to Serper securely."""
    if not SERPER_API_KEY:
        return "Serper API key missing from environment."
    try:
        conn = http.client.HTTPSConnection("google.serper.dev")
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': str(SERPER_API_KEY).strip(),
            'Content-Type': 'application/json'
        }
        conn.request("POST", "/search", payload, headers)
        res = conn.getresponse()
        data = res.read()
        results = json.loads(data.decode("utf-8"))

        snippets = [item.get('snippet', '') for item in results.get('organic', [])[:3]]
        return "\n".join(snippets) if snippets else "No search results returned."
    except Exception as e:
        return f"Could not fetch search data: {e}"


def query_groq(prompt):
    """Performs a direct API call to Groq with full fallback visibility."""
    if not GROQ_API_KEY:
        return "❌ Error: GROQ_API_KEY is missing or empty."
    try:
        conn = http.client.HTTPSConnection("api.groq.com")

        # Using the standard modern llama-3.3 model to ensure availability
        payload = json.dumps({
            "model": "llama-3.3-70b-versatile",
            "messages": [
                {"role": "system", "content": "You are a Senior Business Development & Product Analyst."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        })

        headers = {
            'Authorization': f'Bearer {str(GROQ_API_KEY).strip()}',
            'Content-Type': 'application/json'
        }

        conn.request("POST", "/openai/v1/chat/completions", payload, headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        result_json = json.loads(data)

        # Safe structural parsing check
        if 'choices' in result_json and len(result_json['choices']) > 0:
            return result_json['choices'][0]['message']['content']
        elif 'error' in result_json:
            error_msg = result_json['error'].get('message', 'Unknown API Error')
            return f"❌ Groq Server Error: {error_msg}"
        else:
            return f"❌ Unexpected response structure from Groq:\n```json\n{json.dumps(result_json, indent=2)}\n```"

    except Exception as e:
        return f"❌ Python Connection Error: {e}"


# ==========================================
# 3. STREAMLIT UI LAYOUT
# ==========================================
st.set_page_config(page_title="Product Analysis Tool", layout="wide")
st.title("🚀 Business Development: Product Analysis Dashboard")

# Show key status on screen cleanly to remove guesswork
with st.sidebar:
    st.header("🔑 API Connection Status")
    if GROQ_API_KEY:
        st.success("Groq Key Detected")
    else:
        st.error("Groq Key Missing")

    if SERPER_API_KEY:
        st.success("Serper Key Detected")
    else:
        st.error("Serper Key Missing")

product_name = st.text_input("Enter the product name or market niche to analyze:",
                             placeholder="e.g., AI-powered Customer Support Platforms")

if st.button("Run Market Analysis", type="primary"):
    if not product_name.strip():
        st.warning("Please enter a valid product name.")
    else:
        with st.spinner("Analyzing market data and generating reports..."):

            st.write("🔍 Running live web search across competitor contexts...")
            search_context = google_search(f"{product_name} competitors trends metrics")

            st.write("📊 Processing trends data via Groq Engine...")
            final_prompt = f"""
            Analyze the market landscape, competitive positioning, and core features associated with: '{product_name}'.

            Here is live web search data to help your analysis:
            {search_context}

            Provide a comprehensive Markdown report summarizing key competitors, a feature breakdown matrix, 
            identified market gaps, and strategic business development recommendations.
            """

            report = query_groq(final_prompt)

            st.success("🏁 Execution Complete!")
            st.markdown("### 📊 Market Analysis Output Report")
            st.markdown(report)
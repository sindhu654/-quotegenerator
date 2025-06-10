import streamlit as st
import google.generativeai as genai

# ========== 1. Setup Gemini API ========== #
genai.configure(api_key="AIzaSyB2UpptHwCOXJulgi579qgdce_aWI83BfM")  # Replace with your actual API key

# Use correct model name string
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

# ========== 2. Helper: Generate Quote Prompt ========== #
def build_prompt(keyword, category, tone):
    base = "Generate a meaningful quote"
    if keyword:
        base += f" about {keyword}"
    if category:
        base += f" in the category of {category}"
    if tone:
        base += f" with a {tone} tone"
    base += ". Include author name if known. Keep it short and profound."
    return base

# ========== 3. Generate Quote Using Gemini ========== #
def generate_quote(keyword, category, tone):
    prompt = build_prompt(keyword, category, tone)
    try:
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"Error: {e}"

# ========== 4. Streamlit App UI ========== #
st.set_page_config(page_title="Gemini Quote Generator", layout="centered")
st.title("✨ Random Quote Generator")
st.markdown("Get a customized quote using AI. Choose a theme, category, and tone.")

# --- Input Area --- #
keyword = st.text_input("Enter a theme/keyword (optional):", placeholder="e.g. motivation, happiness")

category = st.selectbox("Choose a category:", ["Inspirational", "Humorous", "Love", "Life", "Random"])

tone = st.radio("Select a tone/style:", ["Formal", "Casual", "Witty", "Philosophical"])

# --- Regenerate Trigger --- #
if 'quote_result' not in st.session_state:
    st.session_state.quote_result = ""

if st.button("🎯 Generate Quote"):
    st.session_state.quote_result = generate_quote(keyword, category, tone)

# --- Display Quote --- #
if st.session_state.quote_result:
    with st.container():
        st.markdown("---")
        st.subheader("📝 Your Quote")
        st.markdown(
            f"""<div style='
                    background-color: #f4f4f4;
                    padding: 20px;
                    border-radius: 15px;
                    box-shadow: 2px 2px 12px rgba(0,0,0,0.1);
                    font-style: italic;
                    font-size: 18px;'>{st.session_state.quote_result}</div>""",
            unsafe_allow_html=True
        )

    # --- Regenerate Button --- #
    if st.button("🔁 Regenerate"):
        st.session_state.quote_result = generate_quote(keyword, category, tone)

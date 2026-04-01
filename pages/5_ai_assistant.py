import streamlit as st
from utils.ai import summarize

st.set_page_config(page_title="AI Assistant", page_icon="🤖")

st.title("🤖 AI Assistant")
st.caption("Turn your messy notes into clean summaries ✨")

# 🔐 Auth check
if "user" not in st.session_state:
    st.warning("Login first")
    st.stop()

# 💎 Premium check
if not st.session_state.get("premium", 0):
    st.warning("🔒 Premium Feature. Upgrade to use AI.")
    st.stop()

# 📝 Input
text = st.text_area(
    "Paste your notes",
    height=200,
    placeholder="Type or paste lecture notes, PDFs, etc..."
)

# 🚀 Action
if st.button("✨ Summarize"):

    if not text.strip():
        st.warning("⚠️ Please enter some text.")
        st.stop()

    with st.spinner("Thinking..."):
        result = summarize(text)

    # 📌 Output
    st.subheader("📌 Summary")
    st.success(result)

    # 🔥 UX Upgrade: Download button
    st.download_button(
        label="⬇️ Download Summary",
        data=result,
        file_name="summary.txt",
        mime="text/plain"
    )

    # 💡 Subtle product hint (retention play)
    st.caption("Tip: Convert this into tasks to stay consistent 👀")
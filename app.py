import streamlit as st
from deep_translator import GoogleTranslator

st.set_page_config(
    page_title="Translation Tool",
    page_icon="🌐",
    layout="centered"
)

st.title("🌐 Translation Tool")
st.caption("Translate text quickly between multiple languages.")

languages = {
    "English": "en",
    "Hindi": "hi",
    "French": "fr",
    "Spanish": "es",
    "German": "de",
    "Italian": "it",
    "Japanese": "ja",
    "Chinese": "zh-CN",
    "Arabic": "ar",
    "Bengali": "bn"
}

# Text input
text = st.text_area(
    "Enter text to translate",
    placeholder="Type your text here...",
    height=150
)

# Language selection
col1, col2 = st.columns(2)

with col1:
    source_language = st.selectbox(
        "From",
        list(languages.keys())
    )

with col2:
    target_language = st.selectbox(
        "To",
        list(languages.keys()),
        index=1
    )

# Buttons
translate_col, clear_col = st.columns(2)

with translate_col:
    translate_clicked = st.button(
        "🌐 Translate",
        type="primary",
        use_container_width=True
    )

with clear_col:
    clear_clicked = st.button(
        "🧹 Clear",
        use_container_width=True
    )

# Clear button
if clear_clicked:
    st.rerun()

# Translation
if translate_clicked:

    if not text.strip():
        st.warning("⚠️ Please enter some text first.")

    elif source_language == target_language:
        st.info("Source and target languages are the same.")
        st.subheader("Translation")
        st.write(text)

    else:
        try:
            translator = GoogleTranslator(
                source=languages[source_language],
                target=languages[target_language]
            )

            translated_text = translator.translate(text)

            st.subheader("✨ Translation")

            st.success(translated_text)

            # Copyable translation
            st.text_area(
                "Copy translation",
                value=translated_text,
                height=100
            )

        except Exception as e:
            st.error("❌ Translation failed.")
            st.write("Please check your internet connection and try again.")
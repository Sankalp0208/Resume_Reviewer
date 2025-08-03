import language_tool_python
import streamlit as st
import spacy

@st.cache_resource
def load_nlp():
    return spacy.load("en_core_web_sm")

@st.cache_resource
def load_tool():
    # Connect to your local LanguageTool server
    return language_tool_python.LanguageTool(
        remote_server='http://localhost:8083',
        language='en-GB'  # Closest to Indian English
    )

def grammar_check(text):
    try:
        tool = load_tool()
        nlp = load_nlp()
        doc = nlp(text)

        # Collect character spans of all proper nouns (PROPN)
        ignore_spans = []
        for token in doc:
            if token.pos_ == "PROPN":
                start = token.idx
                end = token.idx + len(token.text)
                ignore_spans.append((start, end))

        matches = tool.check(text)
        suggestions = []

        for match in matches:
            match_start = match.offset
            match_end = match.offset + match.errorLength

            # Skip matches overlapping any PROPN span
            if any(start <= match_start < end or start < match_end <= end for start, end in ignore_spans):
                continue

            suggestions.append({
                "message": match.message,
                "suggestion": match.replacements,
                "error_text": text[match.offset:match.offset + match.errorLength],
                "offset": match.offset,
                "length": match.errorLength
            })

        return suggestions

    except Exception as e:
        st.warning(f"⚠️ Grammar check failed: {e}")
        return []


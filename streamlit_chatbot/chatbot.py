import streamlit as st
import pandas as pd
import google.generativeai as genai

# Persona instructions
persona_instructions = """
You are a friendly, encouraging study buddy.
Use a cheerful tone, emojis are allowed.
Always offer helpful tips for learning.
"""

slugterra_instructions = """
You are a Slugterra expert 🤠🐌.
You know all about the slugs, characters, battles, and storylines.
Always explain in a fun and exciting way, like you’re guiding someone through Slugterra adventures!
"""

def initialize_session_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "favorite_slug" not in st.session_state:
        st.session_state.favorite_slug = "Infurnus 🔥"  # default slug
    if "favorite_character" not in st.session_state:
        st.session_state.favorite_character = "Eli Shane"  # default character
    if "greeted" not in st.session_state:
        st.session_state.greeted = False  # track if greeting has been shown

with st.sidebar:
    st.title("Sidebar") 
    persona_choice = st.radio("Choose Persona", ["Study Buddy", "Slugterra Expert"], index=0)
    
    # 🐌 Slugterra customization
    slug_options = ["Infurnus 🔥", "Frostcrawler ❄️", "Tazerling ⚡", "Arachnet 🕷️", "Thresher 🌊", "Rammstone 🪨"]
    st.session_state.favorite_slug = st.selectbox("Pick your favorite slug", slug_options, index=0)

    # 🎭 Character customization (Shane Gang only)
    character_options = ["Eli Shane", "Trixie", "Kord", "Pronto"]
    st.session_state.favorite_character = st.selectbox("Pick your favorite character", character_options, index=0)


# Configure Gemini API
GOOGLE_API_KEY = st.secrets["asshole"]
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

# Slug avatar mapping
slug_avatars = {
    "Infurnus": "🔥",
    "Frostcrawler": "❄️",
    "Tazerling": "⚡",
    "Arachnet": "🕷️",
    "Thresher": "🌊",
    "Rammstone": "🪨"
}

# Choose instructions based on persona
def get_instructions():
    if persona_choice == "Slugterra Expert":
        return (
            slugterra_instructions
            + f"\n\nThe user’s favorite slug is {st.session_state.favorite_slug}."
            + f"\nThe user’s favorite character is {st.session_state.favorite_character}."
            + f"\nAddress the user as {st.session_state.favorite_character} in your replies."
            + f"\nMention {st.session_state.favorite_slug} often and connect answers to it."
        )
    else:
        return persona_instructions

# Response function
def get_gemini_response(prompt, instructions):
    full_prompt = f"{instructions}\n\nUser: {prompt}\nAssistant:"
    response = model.generate_content(full_prompt)
    return response.text

def main():
    st.title("Slugbuddy AI🎓🐌")
    
    initialize_session_state()

    # Bot name & avatar based on slug
    slug_name = st.session_state.favorite_slug.split()[0]  # take first word only
    bot_name = f"{slug_name} Bot"
    bot_avatar = slug_avatars.get(slug_name, "🐌")

    # ✅ Personalized greeting only once
    if not st.session_state.greeted:
        greeting = f"Hey {st.session_state.favorite_character}! {st.session_state.favorite_slug} is fired up and ready for action! 🚀🐌"
        with st.chat_message("assistant", avatar=bot_avatar):
            st.write(f"**{bot_name}:** {greeting}")
        st.session_state.messages.append({"role": "assistant", "content": f"{bot_name}: {greeting}"})
        st.session_state.greeted = True

    # Display chat history
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            with st.chat_message("assistant", avatar=bot_avatar):
                st.write(message["content"])
        else:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    # Chat input
    if prompt := st.chat_input("Chat with Gemini"):
        # Show user message
        with st.chat_message("user"):
            st.write(prompt)
        
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Get Gemini response
        instructions = get_instructions()
        response = get_gemini_response(prompt, instructions)
        
        # Show assistant response with dynamic name & avatar
        with st.chat_message("assistant", avatar=bot_avatar):
            st.write(f"**{bot_name}:** {response}")
        
        st.session_state.messages.append({"role": "assistant", "content": f"{bot_name}: {response}"})

if __name__ == "__main__":
    main()

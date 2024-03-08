import streamlit as st
import replicate
import os
from googletrans import Translator

# 🌟✨ StellarChat: Elevating Your Chatbot Experience! 🚀💬

# Setting up the page configuration
st.set_page_config(page_title="🌟✨ StellarChat")

# Authenticating with Replicate
with st.sidebar:
    st.title('🌟✨ StellarChat')
    st.write('Welcome to StellarChat! This futuristic chatbot is empowered by the incredible Llama 2 LLM model from Meta.')
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key provided! You are all set to blast off!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter your Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
            st.warning('Please enter valid credentials to unlock the chat galaxy!', icon='⚠️')
        else:
            st.success('Welcome aboard! Let us dive into the cosmos of conversation!', icon='👉')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    # Personalize your chat experience
    st.subheader('Spacecraft Configuration')
    selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B', 'Llama2-70B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    else:
        llm = 'replicate/llama70b-v2-chat:e951f18578850b652510200860fc4ea62b3b16fac280f83ff32282f87bbd2e48'
    
    # Set parameters for generating responses
    temperature = st.sidebar.slider('Temperature 🌡️', min_value=0.01, max_value=5.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('Top P 🔝', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('Max Length 📏', min_value=64, max_value=4096, value=512, step=8)

os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Initialize chat history
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm your llama friend. How can I assist you today?"}]

# Display or clear chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I'm your llama friend. How can I assist you today?"}]
st.sidebar.button('Clear Chat History', on_click=clear_chat_history)

# Generating responses using LLaMA2
def generate_llama2_response(prompt_input):
    dialogue_history = "You are a knowledgeable assistant. You always reply as 'Assistant' without impersonating 'User'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            dialogue_history += "User: " + dict_message["content"] + "\n\n"
        else:
            dialogue_history += "Assistant: " + dict_message["content"] + "\n\n"
    output = replicate.run(llm, 
                           input={"prompt": f"{dialogue_history} {prompt_input} Assistant: ",
                                  "temperature":temperature, "top_p":top_p, "max_length":max_length, "repetition_penalty":1})
    return output

# User-provided prompt
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate a new response if last message is not from assistant
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)

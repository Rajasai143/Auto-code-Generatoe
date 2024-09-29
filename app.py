import os
from dotenv import load_dotenv
import streamlit as st
import google.generativeai as genai

# This needs to be the first Streamlit command
st.set_page_config(page_title="Automated Code Generator & Enhancer")

# Load environment variables
load_dotenv()
api_key = os.getenv('GOOGLE_API_KEY')

# Configure the generative AI tool with the Gemini API key
genai.configure(api_key=api_key)

# Function to initialize the Gemini Pro model for code generation
model = genai.GenerativeModel("gemini-pro")
chat = model.start_chat(history=[])

# Function to generate code based on software requirements
def generate_required_code(requirements, language):
    prompt = f"""
    Based on the following user requirements, generate efficient and optimized {language} code:
    
    Requirements: {requirements}
    
    The generated code should:
    - Be optimized for performance and scalability.
    - Follow best practices and coding standards.
    - Ensure that the code is error-free and maintainable.
    
    Additionally, provide a brief description of the code functionality.
    """
    
    response = chat.send_message(prompt, stream=True)
    generated_code = ""
    for chunk in response:
        generated_code += chunk.text
    return generated_code

# Function to enhance an existing code snippet
def enhance_code(snippet, language):
    prompt = f"""
    Optimize the following {language} code for performance, readability, and error-free execution:
    
    Code: {snippet}
    
    The enhanced code should:
    - Be optimized for performance.
    - Be free from potential errors or bugs.
    - Follow best practices and coding standards.
    - Be more readable and maintainable.
    
    Provide a brief explanation of the improvements made to the code.
    """
    
    response = chat.send_message(prompt, stream=True)
    enhanced_code = ""
    for chunk in response:
        enhanced_code += chunk.text
    return enhanced_code





# Add custom CSS for background and element styling
st.markdown(
    """
    <style>
    
    /* Background image for the entire app */
    .stApp {
        background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfJr4dULiD0zFQui8VbCUvl_uUAyU5YflC5mm41TyVnfidPn_9vTngRxkbB3mcVjp-KM8&usqp=CAU");
background-size: cover;
        background-position: center;
    }
    
    /* Styling for text inputs and text areas */
    textarea, input {
        background-color: black !important;
        color: white !important;
        border: 2px solid #3498db !important;
        border-radius: 10px !important;
        font-size: 16px !important;
    }
    
    /* Styling for buttons */
    button {
        background-color: transperent !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 10px 20px !important;
        font-size: 16px !important;
        cursor: pointer;
    }
    
    button:hover {
        background-color: #2980b9 !important;
    }
    
    /* Styling for headers and text */
    h1, h2, h3, h4 {
        color: white !important;
        text-shadow: 1px 1px 5px black;
    }
    
    /* Styling for code display */
    pre {
        background-color: black !important;
        color: white !important;
        border-radius: 10px !important;
        padding: 10px !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize the Streamlit app
st.header("Automated Code Generator and Enhancer")

# Initialize session state for chat history if it doesn't exist
if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

# Language selection dropdown (common for both functions)
language = st.selectbox("Select programming language:", ["Python", "Java", "C++", "JavaScript", "Go"])

# Buttons for user choice between generating required code or enhancing code
action = st.radio("Choose an action:", ("Software Required Code", "Code Enhancing"))

# Handle user action: Software Required Code
if action == "Software Required Code":
    # Input for software requirements
    requirements = st.text_area("Enter your software requirements:", key="requirements")
    if st.button("Generate Code"):
        if requirements:
            # Generate the code based on the user requirements
            generated_code = generate_required_code(requirements, language)
            
            # Add user query and generated code to session chat history
            st.session_state["chat_history"].append(("You", requirements))
            
            # Display the generated code and description
            st.subheader(f"Generated {language} Code:")
            st.code(generated_code, language=language.lower())  # Proper code display
            st.session_state["chat_history"].append(("Bot", generated_code))

# Handle user action: Code Enhancing
if action == "Code Enhancing":
    # Input for existing code snippet to enhance
    code_snippet = st.text_area(f"Paste your {language} code to enhance:", key="snippet")
    if st.button("Enhance Code"):
        if code_snippet:
            # Enhance the existing code snippet
            enhanced_code = enhance_code(code_snippet, language)
            
            # Add user query and enhanced code to session chat history
            st.session_state["chat_history"].append(("You", code_snippet))
            
            # Display the enhanced code and explanation
            st.subheader(f"Enhanced {language} Code:")
            st.code(enhanced_code, language=language.lower())  # Proper code display
            st.session_state["chat_history"].append(("Bot", enhanced_code))

# Display the chat history
if st.button("Show Chat History"):
    st.subheader("Chat History")
    for role, text in st.session_state["chat_history"]:
        st.write(f"{role}: {text}")
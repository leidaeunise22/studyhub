# Importing required libraries
import streamlit as st                 # For creating the web app
import google.generativeai as genai     # For using Google’s generative AI models
import math                             # For performing mathematical operations in scientific calculator
import PyPDF2                           # For reading and extracting text from PDF files




# Configuring Google Generative AI with an API key and setting up the model
genai.configure(api_key='your-api-key-goes-here')  # API key to access Google generative AI
model = genai.GenerativeModel('gemini-pro')                        # Initializing the AI model 'gemini-pro'



# Function to extract text content from a PDF file
def extract_text_from_pdf(pdf_file):
    """Extracts text content from each page of the uploaded PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)   # Initialize PDF reader with uploaded file
    num_pages = len(pdf_reader.pages)         # Count the number of pages in the PDF
    text = ""                                 # Placeholder for extracted text

    # Loop through each page and add its text to the text variable
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]     # Access each page
        text += page.extract_text()           # Extract and append text from each page

    return text                               # Return combined text from all pages




# Display a welcome message with custom font and styling
st.markdown("<p class='cursive-text'>Welcome to Aleida's Study Hub!</p>", unsafe_allow_html=True)




# --- Scientific Calculator Section ---
st.subheader("Scientific Calculator")                     # Display a subheading for calculator section
expression = st.text_input("Enter an expression (e.g., math.sin(math.pi/2))")  # Input field for math expressions
if st.button("Calculate"):                                # Button to trigger calculation
    if expression:
        try:
            result = eval(expression, {}, {"math": math})  # Evaluate expression in a secure way with math functions
            st.write(f"Result: {result}")                 # Display the result
        except Exception as e:
            st.write(f"Error: {e}")                       # Handle and display any errors in evaluation




# --- AI Assistant Section ---
st.subheader("AI Assistant")                              # Display a subheading for the AI assistant
user_input = st.text_input("How can I help you today?", "")  # Input field for user queries

if st.button("Generate Response"):                        # Button to trigger AI response generation
    if user_input:
        response = model.generate_content(user_input)     # Use the AI model to generate a response to user input
        if response:
            st.write("Gemini says:", response.text)       # Display the AI-generated response





# --- AI PDF Reader Section ---
st.subheader("AI PDF Reader")                             # Display a subheading for the PDF reader section

# Upload and process a PDF file
uploaded_file = st.file_uploader("Choose a PDF file to upload", type=["pdf"])  # PDF upload option
user_prompt = st.selectbox(                                               # Dropdown for choosing processing options
    'How may I assist you?',
    ('Create study cards', 'Summarize', 'Create study guide', 'Additional Material')
)

# If a PDF file is uploaded, process it based on user prompt
if uploaded_file is not None:
    # Extract text from the PDF using the helper function
    pdf_text = extract_text_from_pdf(uploaded_file)

    if st.button("Process PDF"):                      # Button to trigger PDF processing
        if user_prompt:
            # Prepare the AI input by combining the extracted PDF text and user prompt
            combined_input = f"Here's the content of the uploaded PDF:\n\n{pdf_text}\n\nNow, {user_prompt}"
            response = model.generate_content(combined_input)  # Generate AI response
            st.write("AI Response:", response.text)            # Display the AI-generated response
        else:
            st.warning("Please enter a prompt.")               # Warning if no prompt is provided





st.caption("Pssst... scroll for examples of text styling :)")

# --- Text Styling Examples Section ---
# Examples of using HTML/CSS styling with Streamlit's markdown support
st.subheader("Check out these CSS text styling that you can include in your app !")

# Display sample headings and text with different styles
st.markdown("<h1>This is a Main Heading</h1>", unsafe_allow_html=True)
st.markdown("<h2>This is a Subheading</h2>", unsafe_allow_html=True)
st.markdown("<h3>This is a Smaller Heading</h3>", unsafe_allow_html=True)
st.markdown("<p>This is a regular paragraph demonstrating the font styling.</p>", unsafe_allow_html=True)

# Display highlighted and green-styled text
st.markdown("<p><span class='highlight'>This text is highlighted.</span></p>", unsafe_allow_html=True)
st.markdown("<p><span class='Green-text'>This text is Green.</span></p>", unsafe_allow_html=True)

# Combined styles example: highlighted and cursive
st.markdown("<p><span class='highlight cursive-text'>This text is both highlighted and cursive.</span></p>", unsafe_allow_html=True)

# Custom CSS for additional styling (e.g., fonts, colors, alignment) in the app
st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=Alex+Brush&display=swap" rel="stylesheet">
<style>
    body {
        font-family: 'Helvetica Neue', sans-serif;
        background-color: #f0f0f0; /* Light gray background */
        padding: 20px;
        line-height: 1.6; /* Better readability */
    }
    h1 {
        font-size: 2.5em; 
        color: #333; 
        text-align: center; 
        text-transform: uppercase; 
        text-decoration: underline; 
        font-weight: bold; 
    }
    h2 {
        font-size: 2em; 
        color: #444; 
        text-align: left; 
        text-transform: capitalize; 
    }
    h3 {
        font-size: 1.75em; 
        color: #555; 
        text-align: left; 
        font-weight: normal; 
    }
    p {
        font-size: 1em; 
        color: #666; 
        text-align: justify; 
        margin-bottom: 15px; 
    }
    .highlight {
        background-color: yellow; 
        font-weight: bold; 
    }
    .Green-text {
        color: #00ff00; 
        font-weight: bold; 
        text-align: center; 
        text-decoration: underline; 
    }
    .cursive-text {
        font-family: 'Alex Brush', cursive;
        color: #FF69B4; /* Hot pink color */
        font-size: 3em;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

import streamlit as st
import google.generativeai as genai
import requests
import base64
import math
import PyPDF2
import time

#streamlit run demogwc.py --server.enableCORS=false



st.markdown("""

<style>
    @import url('https://fonts.googleapis.com/css2?family=Alex+Brush&display=swap');
    .cursive-pink-text {
        font-family: 'Alex Brush', cursive;
        color: #ff69b4; /* Hot pink */
        font-size: 2.5em; /* Adjust size as desired */
        text-align: center;
    }
</style>

    body {
        font-family: 'Helvetica Neue', sans-serif;
    }

    
    .white-text {
        color: white;   /* Set color to white */
    }

    .highlight-text {
        background-color: yellow;
        font-weight: bold;
    }
    <link href="https://fonts.googleapis.com/css2?family=Alex+Brush&display=swap" rel="stylesheet">
    <style>
        .cursive-text {
            font-family: 'Alex Brush', cursive; 
        }
</style>
""", unsafe_allow_html=True)
st.markdown("""
<h1 class='cursive-pink-text'>Welcome to Aleida's Study Hub!</h1>
""", unsafe_allow_html=True)

st.title("My Styled App")
st.write("This is some regular text.")
st.markdown("<span class='highlight-text'>This text is highlighted.</span>", unsafe_allow_html=True)
st.markdown("<span class='cursive-text'>This text is cursive.</span>", unsafe_allow_html=True)
st.markdown("""
<h1 class='cursive-text'>
    <span class='white-text'>Welcome to Aleida's Study Hub! </span> 
</h1>
""", unsafe_allow_html=True)





# Configure the Google Generative AI API
genai.configure(api_key='AIzaSyAbmzbfcfcAxKGwc3hQtC4rduGBJQq0uRQ')
model = genai.GenerativeModel('gemini-pro')

st.header("Welcome to Aleida's Study Hub!")
col1, col2 = st.columns([2, 1])

# Weather API Key (Replace with your actual API key)
weather_api_key = "c19884e791b473ab65b34be6c92dbca7"

def get_weather_forecast(city):
    """Fetches and returns today's weather forecast for a given city in Fahrenheit."""
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + weather_api_key + "&q=" + city
    response = requests.get(complete_url)
    
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        # Convert from Kelvin to Fahrenheit
        temperature = round((main['temp'] - 273.15) * 9/5 + 32, 2)  
        description = data['weather'][0]['description']
        return f"Today's forecast for {city}: {temperature}°F, {description}"
    else:
        return "Error fetching weather data."

# Initialize todo list in session state
if 'todos' not in st.session_state:
    st.session_state.todos = []

st.sidebar.header("To-Do List")

# Function to add a new todo item
def add_todo():
    new_todo = st.session_state.new_todo_input
    if new_todo:  # Only add if not empty
        st.session_state.todos.append({"task": new_todo, "completed": False})
        st.session_state.new_todo_input = ""  # Clear input field

# Input field for new todo items
st.sidebar.text_input("Enter a new to-do item:", key="new_todo_input", on_change=add_todo)

# Display and manage todo items
for index, todo in enumerate(st.session_state.todos):
    col1, col2, col3 = st.sidebar.columns([.3, 1, 1])  # Create three columns
    with col1:
        # Checkbox to mark as completed
        completed = st.checkbox(f"", key=f"checkbox_{index}", value=todo["completed"])
        if completed:
            st.session_state.todos[index]["completed"] = True
        else:
            st.session_state.todos[index]["completed"] = False
    with col2:
        # Display the todo item
        if todo["completed"]:
            st.markdown(f"<strike>{todo['task']}</strike>", unsafe_allow_html=True)
        else:
            st.write(todo["task"])
    with col3:
        # Delete button
        if st.button("Delete", key=f"delete_{index}"):
            del st.session_state.todos[index]
            st.rerun()  # Rerun to refresh the list

# Weather section in sidebar
st.sidebar.header("Today's Weather")
city_name = st.sidebar.text_input("Enter City Name", "London")
if st.sidebar.button("Get Forecast"):
    forecast = get_weather_forecast(city_name)
    st.sidebar.write(forecast)

# Theme section
themes = {
    "Light": "",
    "Dark": """
        <style>
        .stApp {
            background-color: #333333;
        }
        </style>
    """,
    "Gradient": """
        <style>
        .stApp {
            background: linear-gradient(315deg, #4f2991 3%, #7dc4ff 38%, #36cfcc 68%, #a92ed3 98%);
            animation: gradient 15s ease infinite;
            background-size: 400% 400%;
            background-attachment: fixed;
        }
        </style>
    """,
}

# Create a selectbox for theme selection
selected_theme = st.sidebar.selectbox("Select a theme", list(themes.keys()))

# Apply the selected theme
st.markdown(themes[selected_theme], unsafe_allow_html=True)

def encode_image(image_file):
    """Encodes an image file to base64 format."""
    if image_file is not None:
        return base64.b64encode(image_file.read()).decode()
    else:
        return None

st.sidebar.subheader("Upload Background Image")
uploaded_image = st.sidebar.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Encode the uploaded image
encoded_image = encode_image(uploaded_image)

# Apply the uploaded image as background
if encoded_image:
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_image});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Scientific Calculator section
st.text("Scientific Calculator")

expression = st.text_input("Enter an expression (e.g., math.sin(math.pi/2))")
if st.button("Calculate"):
    if expression:
        try:
            result = eval(expression, {}, {"math": math})
            st.write(f"Result: {result}")
        except Exception as e:
            st.write(f"Error: {e}")

# AI Assistant section
st.text("AI Assistant")

user_input = st.text_input("How can I help you today?", "")
if st.button("Generate Response"):
    if user_input:
        response = model.generate_content(user_input)
        if response:
            st.write("Brainiac says:", response.text)

# AI PDF Reader section
st.text("AI PDF Reader")

def extract_text_from_pdf(pdf_file):
    """Extracts text content from a PDF file."""
    pdf_reader = PyPDF2.PdfReader(pdf_file)
    num_pages = len(pdf_reader.pages)
    text = ""
    for page_num in range(num_pages):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    return text

uploaded_file = st.file_uploader("Choose a PDF file to upload", type=["pdf"])
user_prompt = st.text_input("Enter your prompt:")

if uploaded_file is not None:
    # Extract text from the PDF
    pdf_text = extract_text_from_pdf(uploaded_file)

    if st.button("Process PDF"):
        if user_prompt:
            # Combine PDF text and prompt for the AI
            combined_input = f"Here's the content of the uploaded PDF:\n\n{pdf_text}\n\nNow, {user_prompt}"
            response = model.generate_content(combined_input)
            st.write("AI Response:", response.text)
        else:
            st.warning("Please enter a prompt.")

#ask me anything !!
#pdf options, summarize, generate flashcards, create a quiz

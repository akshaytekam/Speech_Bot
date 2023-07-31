from flask import Flask, render_template, request, redirect, send_file
from flask_socketio import SocketIO, emit
import time
import speech_recognition as sr
import pyttsx3
from bs4 import BeautifulSoup
from header import generate_empty_html

app = Flask(__name__)

def text_to_speech(text):
    # Initialize the TTS engine
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


file_path = "generated.html"

@app.route('/download')
def download_html():
	return send_file(file_path, as_attachment=True)

def save_html_to_file(html_content, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_content)
    print(f"HTML file '{file_path}' generated successfully.")

def write_to_file(file_path, html_content):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html_content)

    print(f"HTML file '{file_path}' generated successfully.")

def update_html_code(existing_file, new_content, new_element):
    # Read the content of the existing HTML file
    with open(existing_file, 'r') as f:
        html_content = f.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Create a new <p> tag with the new paragraph content
    new_p_tag = soup.new_tag(new_element)
    new_p_tag.string = new_content

    new_p_tag.attrs['style'] = "display: flex; justify-content: center; align-items: center;"

    # Create a new <div> tag
    new_div_tag = soup.new_tag('div')

    # Append the new <h2> tag to the <div> tag
    new_div_tag.append(new_p_tag)

    # Find the <body> tag and append the new <p> tag to it
    body_tag = soup.body
    body_tag.append(new_p_tag)

    # Create a new HTML file with the updated content
    updated_file = 'generated.html'
    with open(updated_file, 'w') as f:
        f.write(soup.prettify())

def add_menu_bar_to_html(existing_file):
    # Read the content of the existing HTML file
    with open(existing_file, 'r') as f:
        html_content = f.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Create a new menu bar using an unordered list (<ul>) with list items (<li>)
    new_menu_items = ['Home', 'About', 'Contact']
    new_menu_list = soup.new_tag('ul', **{'class': 'menu-bar'})
    for item in new_menu_items:
        new_li_tag = soup.new_tag('li')
        new_li_tag.string = item
        new_menu_list.append(new_li_tag)

    # Find the <body> tag and insert the new menu bar at the beginning of the body
    body_tag = soup.body
    body_tag.insert(0, new_menu_list)

    # Add CSS styles to the menu bar using a <style> tag
    style_tag = soup.new_tag('style')
    style_tag.string = """
        .menu-bar {
            list-style: none;
            display: flex;
            justify-content: space-around;
            background-color: #f2f2f2;
            padding: 10px 0;
        }

        .menu-bar li {
            padding: 5px 10px;
            border: 1px solid #ccc;
            border-radius: 5px;
        }
    """
    head_tag = soup.head
    head_tag.append(style_tag)

    # Create a new HTML file with the updated content
    updated_file = 'generated.html'
    with open(updated_file, 'w') as f:
        f.write(soup.prettify())

def speech():
    transcript = ""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        # Adjust the background noise
        recognizer.adjust_for_ambient_noise(source)
        # Listen for audio input
        audio = recognizer.listen(source)

        try:
            # Use Google's Web Speech API to recognize the speech
            transcript = recognizer.recognize_google(audio)

        except Exception as e:
            print("Error : "+ str(e))
        return transcript

@app.route("/", methods=["GET","POST"])
def index():
    html_content = generate_empty_html()
    save_html_to_file(html_content, file_path)
    
    return render_template('index.html')

@app.route('/button_clicked', methods=['POST'])
def handle_button_click():
    data = request.get_json()
    if data and data.get('buttonClicked', False):

        transcript = ""
        say_something = "Say something."
        print(say_something)
        text_to_speech(say_something)
        
        transcript = speech()
        if transcript == 'heading':
            heading_value = "What is heading value?"
            print(heading_value)
            text_to_speech(heading_value)
            input_value_heading = speech()
            new_element = 'h2'

            update_html_code(file_path, input_value_heading, new_element)
            print("html code updated with", transcript)
        
        if transcript == 'paragraph':
            paragraph_value = "What is paragraph value?"
            print(paragraph_value)
            text_to_speech(paragraph_value)
            input_value_paragraph = speech()
            new_element = 'p'

            update_html_code(file_path, input_value_paragraph, new_element)
            print("html code updated with", transcript)
        
        if transcript == 'button':
            button_value = "What is button value?"
            print(button_value)
            text_to_speech(button_value)
            input_value_button = speech()
            new_element = 'button'

            update_html_code(file_path, input_value_button, new_element)
            print("html code updated with", transcript)

        if transcript == 'menu':
            add_menu_bar_to_html(file_path)
            print("html code updated with", transcript)

    return "Button click not detected."

if __name__ == "__main__":
    app.run(debug=True, threaded=True)
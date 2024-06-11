from flask import Flask, request, render_template
from openai import OpenAI

# Point to the local server
client = OpenAI(base_url="http://localhost:1234/v1", api_key="not-needed")

app = Flask(__name__)

# Function to read contents of a text file
def read_text_file(file_path):
    with open(file_path, 'r') as file:
        contents = file.read()
    return contents

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for handling form submission
@app.route('/get_response', methods=['POST'])
def get_response():
    user_prompt = request.form['prompt']
    file_contents = read_text_file("vault.txt")

    # Get response from OpenAI based on user prompt
    completion = client.chat.completions.create(
        model="local-model", # this field is currently unused
        messages=[
            {"role": "system", "content": file_contents},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7,
    )

    # Extract response from OpenAI completion
    response = completion.choices[0].message.content

    return render_template('index.html', prompt=user_prompt, response=response)

if __name__ == '__main__':
    app.run(debug=True)




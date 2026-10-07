import re
import os

def remove_emojis_and_fluff(text):
    # Emojis to remove
    emojis = ['🧠', '🎯', '🏗️', '☁️', '👉', '🧹', '📊', '🔬', '📈', '🌍', '💡', '⚖️', '🚀', '✅', '❌', '🔥', '✨']
    for emoji in emojis:
        text = text.replace(emoji + " ", "")
        text = text.replace(emoji, "")
        
    # Replace fluff/filler words with academic equivalents
    replacements = {
        "mic-drop finding": "primary finding",
        "beautiful": "comprehensive",
        "amazing": "significant",
        "incredible": "robust",
        "perfectly": "effectively",
        "insanely high": "statistically anomalous",
        "The cardinal sin of many hackathon submissions": "A common methodological error",
        "This section forms the computational core of the engine.": "",
        "The heavy lifting of the": "The",
        "drastically reducing compute time.": "optimizing computational efficiency.",
        "which replaces the need for Streamlit/Dash!": "",
        "brilliant move": "strategic decision",
        "fake humans": "synthetic artifacts",
        "torturing the data until it confesses": "overfitting exploratory noise",
        "fake data": "synthetic data",
        "massive": "substantial",
        "hoard almost 100%": "account for the vast majority",
        "hoover up": "capture",
        "script kiddies": "amateur implementations"
    }
    
    # Case-insensitive replacements
    for old, new in replacements.items():
        pattern = re.compile(re.escape(old), re.IGNORECASE)
        text = pattern.sub(new, text)
        
    # Extra trailing spaces fix
    text = re.sub(r' +$', '', text, flags=re.MULTILINE)
    
    return text

files_to_clean = [
    'README.md',
    'docs/METHODOLOGY.md',
    'docs/ADVANCED_EDA.md',
    'docs/ARCHITECTURE.md',
    'docs/SAS_VFL_INTEGRATION.md'
]

project_root = os.path.dirname(os.path.abspath(__file__))

for file_path in files_to_clean:
    full_path = os.path.join(project_root, file_path)
    if os.path.exists(full_path):
        with open(full_path, 'r') as f:
            content = f.read()
            
        cleaned_content = remove_emojis_and_fluff(content)
        
        with open(full_path, 'w') as f:
            f.write(cleaned_content)
        print(f"Cleaned {file_path}")


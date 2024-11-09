from flask import Flask, render_template_string, request, jsonify
import sqlite3
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from scipy.special import softmax

app = Flask(__name__)

# Constants
EMOJIS_PER_PAGE = 50  # Number of emojis per page for lazy loading

# Load the emotion classification model and tokenizer
tokenizer = AutoTokenizer.from_pretrained("j-hartmann/emotion-english-distilroberta-base")
model = AutoModelForSequenceClassification.from_pretrained("j-hartmann/emotion-english-distilroberta-base")

# Define id to label mapping
id2label = {
    "0": "anger",
    "1": "disgust",
    "2": "fear",
    "3": "joy",
    "4": "neutral",
    "5": "sadness",
    "6": "surprise"
}

# Initialize SQLite and load the emojis if not already loaded
def init_db():
    conn = sqlite3.connect('emojis.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emojis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emoji TEXT,
            name TEXT,
            "group" TEXT,
            sub_group TEXT,
            codepoints TEXT
        )
    ''')

    # Only load emojis if the table is empty
    cursor.execute('SELECT COUNT(*) FROM emojis')
    if cursor.fetchone()[0] == 0:
        # Load the emoji dataset from the uploaded CSV
        df = pd.read_csv('/mnt/data/emoji_df.csv')  # Path to your uploaded file
        df.to_sql('emojis', conn, if_exists='replace', index=False)

    conn.commit()
    conn.close()

# Function to analyze emotions
def analyze_emotions(text):
    inputs = tokenizer(text, return_tensors="pt", max_length=512, truncation=True, padding="max_length")
    outputs = model(**inputs)
    scores = outputs.logits[0].detach().numpy()
    scores = softmax(scores)
    emotions = {
        'anger': float(scores[0]),
        'disgust': float(scores[1]),
        'fear': float(scores[2]),
        'joy': float(scores[3]),
        'neutral': float(scores[4]),
        'sadness': float(scores[5]),
        'surprise': float(scores[6])
    }
    return emotions

# Get emojis with pagination and optional search filter
def get_emojis(category=None, search_query="", page=1, per_page=EMOJIS_PER_PAGE):
    conn = sqlite3.connect('emojis.db')
    cursor = conn.cursor()
    offset = (page - 1) * per_page

    if category:
        query = "SELECT emoji, name FROM emojis WHERE \"group\" = ? AND name LIKE ? ORDER BY name LIMIT ? OFFSET ?"
        cursor.execute(query, (category, f'%{search_query}%', per_page, offset))
    else:
        query = "SELECT emoji, name FROM emojis WHERE name LIKE ? ORDER BY name LIMIT ? OFFSET ?"
        cursor.execute(query, (f'%{search_query}%', per_page, offset))

    emojis = cursor.fetchall()
    conn.close()

    return emojis

@app.route('/')
def index():
    category = request.args.get('category', None)
    search_query = request.args.get('search', "")

    # Define emoji categories with Font Awesome
    categories = [
        ("Smileys & Emotion", "fa-solid fa-face-smile"),
        ("People & Body", "fa-solid fa-users"),
        ("Animals & Nature", "fa-solid fa-leaf"),
        ("Food & Drink", "fa-solid fa-mug-hot"),
        ("Activities", "fa-solid fa-futbol"),
        ("Travel & Places", "fa-solid fa-location-dot"),
        ("Objects", "fa-solid fa-lightbulb"),
        ("Symbols", "fa-solid fa-heart"),
        ("Flags", "fa-solid fa-flag")
    ]

    return render_template_string('''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <!-- Existing head content remains unchanged -->
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Emoji Picker with Emotion Analysis</title>
        <!-- Font Awesome for Category Icons -->
        <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
        <!-- Animate.css for Animations -->
        <link href="https://cdnjs.cloudflare.com/ajax/libs/animate.css/4.1.1/animate.min.css" rel="stylesheet">
        <!-- Hover.css for Hover Effects -->
        <link href="https://cdnjs.cloudflare.com/ajax/libs/hover.css/2.3.1/css/hover-min.css" rel="stylesheet">
        <!-- AOS (Animate On Scroll) -->
        <link href="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.css" rel="stylesheet">
        <style>
            /* Color Palette */
            :root {
                --primary-color: #689e4b; /* Green */
                --dark-color: #0e2326;    /* Dark Teal */
                --light-color: #ffffff;    /* White */
                --border-color: #ddd;
                --hover-bg-color: #e5e7eb;
            }

            /* Reset & Base Styles */
            * {
                box-sizing: border-box;
                margin: 0;
                padding: 0;
            }

            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background-color: var(--light-color);
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                position: relative;
            }

            /* Toggle Button */
            .toggle-button {
                position: fixed;
                bottom: 20px;
                right: 20px;
                background-color: var(--primary-color);
                color: var(--light-color);
                border: none;
                border-radius: 50%;
                width: 60px;
                height: 60px;
                font-size: 24px;
                cursor: pointer;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                transition: background-color 0.3s, transform 0.3s;
                z-index: 1001;
                display: flex;
                justify-content: center;
                align-items: center;
            }

            .toggle-button:hover {
                background-color: #5a8a3e;
                transform: scale(1.1);
            }

            /* Modal Styles */
            .modal {
                display: none; /* Hidden by default */
                position: fixed; /* Stay in place */
                z-index: 1000; /* Sit on top */
                left: 0;
                top: 0;
                width: 100%; /* Full width */
                height: 100%; /* Full height */
                overflow: auto; /* Enable scroll if needed */
                background-color: rgba(0,0,0,0.4); /* Black w/ opacity */
            }

            .modal-content {
                background-color: var(--light-color);
                margin: 5% auto; /* 5% from the top and centered */
                padding: 20px;
                border: 1px solid var(--border-color);
                width: 90%; /* Could be more or less, depending on screen size */
                max-width: 600px;
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                position: relative;
                animation: fadeIn 0.5s ease-in-out;
            }

            .close-btn {
                color: var(--dark-color);
                position: absolute;
                top: 10px;
                right: 20px;
                font-size: 28px;
                font-weight: bold;
                cursor: pointer;
                transition: color 0.3s;
            }

            .close-btn:hover,
            .close-btn:focus {
                color: var(--primary-color);
                text-decoration: none;
                cursor: pointer;
            }

            /* Emoji Picker Styles */
            .emoji-picker {
                width: 100%;
                display: flex;
                flex-direction: column;
                align-items: center;
            }

            /* Search Bar */
            .search-bar {
                width: 100%;
                padding: 10px 12px;
                border-radius: 8px;
                border: 1px solid var(--border-color);
                margin-bottom: 15px;
                font-size: 16px;
                transition: border 0.3s;
            }

            .search-bar:focus {
                border-color: var(--primary-color);
                outline: none;
                box-shadow: 0 0 5px rgba(104, 158, 75, 0.5);
            }

            /* Category Icons */
            .category-icons {
                display: flex;
                justify-content: space-between;
                margin-bottom: 15px;
                overflow-x: auto;
                width: 100%;
            }

            .category-icons a {
                flex: 1;
                text-align: center;
                padding: 8px 0;
                margin: 0 4px;
                border-radius: 6px;
                color: var(--dark-color);
                background-color: var(--light-color);
                transition: color 0.3s, transform 0.3s;
                text-decoration: none;
                font-size: 20px;
                position: relative;
            }

            .category-icons a.active i,
            .category-icons a:hover i {
                color: var(--primary-color);
            }

            /* Remove background color changes on hover and active */
            .category-icons a.active,
            .category-icons a:hover {
                background-color: var(--light-color);
            }

            /* Emoji Grid */
            .emoji-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(40px, 1fr));
                gap: 10px;
                overflow-y: auto;
                max-height: 250px;
                padding-right: 5px;
                width: 100%;
            }

            .emoji {
                font-size: 24px;
                cursor: pointer;
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 8px;
                border-radius: 8px;
                transition: background-color 0.3s, transform 0.3s;
                /* Hover.css class for effect */
                /* AOS animation */
                data-aos="zoom-in"
            }

            .emoji:hover {
                background-color: var(--hover-bg-color);
                /* Scale handled by Hover.css */
            }

            .emoji:active {
                transform: scale(0.95);
            }

            /* Scrollbar Styling */
            .emoji-grid::-webkit-scrollbar {
                width: 6px;
            }

            .emoji-grid::-webkit-scrollbar-track {
                background: var(--light-color);
                border-radius: 10px;
            }

            .emoji-grid::-webkit-scrollbar-thumb {
                background-color: var(--primary-color);
                border-radius: 10px;
            }

            /* Responsive Design */
            @media (max-width: 600px) {
                .modal-content {
                    width: 95%;
                }

                .category-icons a {
                    font-size: 18px;
                }

                .emoji {
                    font-size: 20px;
                }
            }

            /* Additional Animations */
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(-20px); }
                to { opacity: 1; transform: translateY(0); }
            }

            /* Emotion Distribution Progress Bars */
            .emotion-distribution {
                width: 100%;
                margin-top: 20px;
            }

            .emotion-bar {
                margin-bottom: 10px;
            }

            .emotion-label {
                margin-bottom: 5px;
                font-weight: bold;
                display: flex;
                justify-content: space-between;
            }

            .progress {
                width: 100%;
                background-color: var(--hover-bg-color);
                border-radius: 10px;
                overflow: hidden;
            }

            .progress-bar {
                height: 20px;
                background-color: var(--primary-color);
                width: 0%;
                transition: width 0.5s;
            }

            /* Notification Styles */
            .notification {
                position: fixed;
                bottom: 100px;
                right: 20px;
                background-color: rgba(0,0,0,0.8);
                color: #fff;
                padding: 10px 20px;
                border-radius: 5px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
                z-index: 1002;
                display: flex;
                align-items: center;
                opacity: 0;
                transition: opacity 0.5s;
            }

            .notification span:first-child {
                font-size: 24px;
                margin-right: 10px;
            }
        </style>
    </head>
    <body>
        <!-- Toggle Button -->
        <button class="toggle-button" id="open-modal" aria-label="Open Emoji Picker">
            <i class="fa-solid fa-smile"></i>
        </button>

        <!-- Modal for Emoji Picker and Emotion Distribution -->
        <div id="emoji-modal" class="modal" aria-hidden="true" role="dialog" aria-labelledby="modal-title">
            <div class="modal-content">
                <span class="close-btn" onclick="closeModal()" aria-label="Close">&times;</span>
                <div class="emoji-picker animate__animated animate__fadeIn">
                    <!-- Search Bar -->
                    <input type="text" class="search-bar" placeholder="Search emojis..." 
                           oninput="searchEmojis(this.value)" value="{{ request.args.get('search', '') }}" aria-label="Search Emojis">
                    
                    <!-- Category Icons -->
                    <div class="category-icons">
                        {% for cat, icon in categories %}
                            <a href="javascript:void(0);" onclick="changeCategory('{{ cat }}')" class="{{ 'active' if category == cat else '' }}" title="{{ cat }}" aria-label="{{ cat }}">
                                <i class="{{ icon }}" aria-hidden="true"></i>
                            </a>
                        {% endfor %}
                    </div>
                    
                    <!-- Emoji Grid with Lazy Loading -->
                    <div class="emoji-grid" id="emoji-grid" aria-label="Emoji List" data-aos="fade-up">
                        <!-- Emojis will be loaded here dynamically -->
                    </div>
                </div>

                <!-- Emotion Distribution Progress Bars -->
                <div class="emotion-distribution" id="emotion-distribution" aria-label="Emotion Distribution">
                    {% for emotion in ['anger', 'disgust', 'fear', 'joy', 'neutral', 'sadness', 'surprise'] %}
                        <div class="emotion-bar">
                            <div class="emotion-label">
                                <span>{{ emotion.capitalize() }}</span>
                                <span id="{{ emotion }}-percentage">0%</span>
                            </div>
                            <div class="progress">
                                <div class="progress-bar" id="{{ emotion }}-bar"></div>
                            </div>
                        </div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <!-- JavaScript Libraries -->
        <!-- AOS (Animate On Scroll) -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/aos/2.3.4/aos.js"></script>
        <!-- GSAP for advanced animations (optional) -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.11.4/gsap.min.js"></script>
        <script>
            // Initialize AOS
            AOS.init({
                duration: 800,
                easing: 'slide',
                once: true
            });

            // Modal Elements
            const modal = document.getElementById("emoji-modal");
            const openModalBtn = document.getElementById("open-modal");
            const closeModalBtn = document.querySelector(".close-btn");

            // Function to update progress bars with percentages
            function updateProgressBars(emotions) {
                for (const [emotion, percentage] of Object.entries(emotions)) {
                    const capEmotion = emotion.charAt(0).toUpperCase() + emotion.slice(1);
                    const percentageElement = document.getElementById(`${emotion}-percentage`);
                    const progressBar = document.getElementById(`${emotion}-bar`);
                    
                    percentageElement.innerText = `${(percentage * 100).toFixed(2)}%`;
                    progressBar.style.width = `${(percentage * 100).toFixed(2)}%`;
                }
            }

            // Open Modal
            openModalBtn.onclick = function() {
                modal.style.display = "block";
                modal.setAttribute('aria-hidden', 'false');
                // Load emojis when modal is opened
                loadEmojis();
            }

            // Close Modal
            closeModalBtn.onclick = function() {
                modal.style.display = "none";
                modal.setAttribute('aria-hidden', 'true');
            }

            // Close Modal when clicking outside of the modal content
            window.onclick = function(event) {
                if (event.target == modal) {
                    modal.style.display = "none";
                    modal.setAttribute('aria-hidden', 'true');
                }
            }

            let page = 1;
            let isLoading = false;
            let currentCategory = "{{ category or '' }}";
            let searchQuery = "{{ search_query or '' }}";

            function searchEmojis(query) {
                searchQuery = query;
                page = 1;
                document.getElementById("emoji-grid").innerHTML = "";
                loadEmojis();
            }

            function changeCategory(category) {
                if (currentCategory === category) return; // Prevent reloading same category
                currentCategory = category;
                page = 1;
                document.getElementById("emoji-grid").innerHTML = "";
                setActiveCategory(category);
                loadEmojis();
            }

            function setActiveCategory(category) {
                const categoryLinks = document.querySelectorAll('.category-icons a');
                categoryLinks.forEach(link => {
                    if (link.getAttribute('onclick').includes(`'${category}'`)) {
                        link.classList.add('active');
                    } else {
                        link.classList.remove('active');
                    }
                });
            }

            function loadEmojis() {
                if (isLoading) return;
                isLoading = true;
                
                fetch(`/load_emojis?page=${page}&category=${encodeURIComponent(currentCategory)}&search=${encodeURIComponent(searchQuery)}`)
                    .then(response => response.json())
                    .then(data => {
                        const emojiGrid = document.getElementById("emoji-grid");
                        data.emojis.forEach(item => {
                            const emojiSpan = document.createElement("span");
                            emojiSpan.classList.add("emoji");
                            emojiSpan.setAttribute("data-aos", "zoom-in");
                            emojiSpan.title = item.name;
                            emojiSpan.innerText = item.emoji;
                            emojiSpan.onclick = () => selectEmoji(item.emoji, item.name);
                            emojiGrid.appendChild(emojiSpan);
                        });
                        // Refresh AOS to recognize new elements
                        AOS.refresh();
                        isLoading = false;
                        if (data.has_more) {
                            page++;
                        }
                    })
                    .catch(error => {
                        console.error('Error loading emojis:', error);
                        isLoading = false;
                    });
            }

            function selectEmoji(emoji, name) {
                // Send the emoji name to the server for classification
                fetch(`/classify`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ "name": name })
                })
                .then(response => response.json())
                .then(data => {
                    if(data.emotions){
                        updateProgressBars(data.emotions);
                        displayEmotionNotification(emoji, data.primary_emotion);
                    } else {
                        console.error('No emotion data received.');
                    }
                })
                .catch(error => {
                    console.error('Error classifying emoji:', error);
                });
            }

            // Function to display a brief notification upon selecting an emoji
            function displayEmotionNotification(emoji, emotion) {
                // Create notification element
                const notification = document.createElement("div");
                notification.classList.add("notification");
                
                notification.innerHTML = `<span>${emoji}</span><span><strong>${emotion.charAt(0).toUpperCase() + emotion.slice(1)}</strong></span>`;

                document.body.appendChild(notification);

                // Fade in
                setTimeout(() => {
                    notification.style.opacity = "1";
                }, 100);

                // Fade out after 2 seconds
                setTimeout(() => {
                    notification.style.opacity = "0";
                    // Remove from DOM after transition
                    setTimeout(() => {
                        notification.remove();
                    }, 500);
                }, 2000);
            }
        </script>
    </body>
    </html>
    ''', categories=categories, category=category, search_query=search_query)

@app.route('/load_emojis')
def load_emojis_route():
    category = request.args.get('category', None)
    search_query = request.args.get('search', "")
    page = int(request.args.get('page', 1))

    emojis = get_emojis(category, search_query, page)
    has_more = len(emojis) == EMOJIS_PER_PAGE  # Check if there are more emojis to load

    return jsonify({
        "emojis": [{"emoji": emoji, "name": name} for emoji, name in emojis],
        "has_more": has_more
    })

@app.route('/classify', methods=['POST'])
def classify():
    data = request.get_json()
    name = data.get('name', '')
    
    if not name:
        return jsonify({"error": "No emoji name provided."}), 400
    
    emotions = analyze_emotions(name)
    
    # Determine primary emotion
    primary_emotion = max(emotions, key=emotions.get)
    
    return jsonify({
        "emotions": emotions,
        "primary_emotion": primary_emotion
    })

if __name__ == '__main__':
    init_db()  # Initialize the database and load emojis
    app.run(debug=True)
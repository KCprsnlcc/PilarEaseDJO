from flask import Flask, render_template_string, request, jsonify
import sqlite3
import pandas as pd

app = Flask(__name__)

# Constants
EMOJIS_PER_PAGE = 50  # Number of emojis per page for lazy loading

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
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Emoji Picker</title>
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
            }

            .emoji-picker {
                width: 320px;
                border: 1px solid var(--border-color);
                border-radius: 10px;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                background-color: var(--light-color);
                padding: 15px;
                display: flex;
                flex-direction: column;
                animation: fadeIn 0.5s ease-in-out;
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
                /* Hover.css class for effect */
                class="hvr-underline-from-center"
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
                class="hvr-grow"
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
            @media (max-width: 400px) {
                .emoji-picker {
                    width: 90%;
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
        </style>
    </head>
    <body>
        <div class="emoji-picker animate__animated animate__fadeIn">
            <!-- Search Bar -->
            <input type="text" class="search-bar" placeholder="Search emojis..." 
                   oninput="searchEmojis(this.value)" value="{{ request.args.get('search', '') }}" aria-label="Search Emojis">
            
            <!-- Category Icons -->
            <div class="category-icons">
                {% for cat, icon in categories %}
                    <a href="javascript:void(0);" onclick="changeCategory('{{ cat }}')" class="{{ 'active' if category == cat else '' }}" title="{{ cat }}">
                        <i class="{{ icon }}" aria-hidden="true"></i>
                    </a>
                {% endfor %}
            </div>
            
            <!-- Emoji Grid with Lazy Loading -->
            <div class="emoji-grid" id="emoji-grid" aria-label="Emoji List" data-aos="fade-up">
                <!-- Emojis will be loaded here dynamically -->
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
                            emojiSpan.classList.add("emoji", "hvr-grow"); // Hover.css class
                            emojiSpan.setAttribute("data-aos", "zoom-in"); // AOS attribute
                            emojiSpan.title = item.name;
                            emojiSpan.innerText = item.emoji;
                            emojiSpan.onclick = () => selectEmoji(item.emoji);
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

            function selectEmoji(emoji) {
                // You can customize this function to handle the selected emoji as needed
                // Example: Insert emoji into a text input or textarea
                alert("Selected Emoji: " + emoji);
            }

            // Load initial emojis
            loadEmojis();

            // Lazy load on scroll
            document.getElementById("emoji-grid").addEventListener("scroll", function() {
                const grid = document.getElementById("emoji-grid");
                if (grid.scrollTop + grid.clientHeight >= grid.scrollHeight - 10) {
                    loadEmojis();
                }
            });
        </script>
    </body>
    </html>
    ''', categories=categories, category=category, search_query=search_query)

@app.route('/load_emojis')
def load_emojis():
    category = request.args.get('category', None)
    search_query = request.args.get('search', "")
    page = int(request.args.get('page', 1))

    emojis = get_emojis(category, search_query, page)
    has_more = len(emojis) == EMOJIS_PER_PAGE  # Check if there are more emojis to load

    return jsonify({
        "emojis": [{"emoji": emoji, "name": name} for emoji, name in emojis],
        "has_more": has_more
    })

if __name__ == '__main__':
    init_db()  # Initialize the database and load emojis
    app.run(debug=True)

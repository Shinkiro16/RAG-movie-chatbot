# 🎬 Movie Research Assistant - Python Chatbot

📖 Overview

The Movie Research Assistant is a Python-based chatbot that allows users to search for movies, get IMDb details, and find trailers using DuckDuckGo. It features a modern UI with chat bubbles and supports franchise detection.

## 📌 Features

- 🎥 Search movies & get **IMDb details** (Title, Rating, Plot)
- 📽️ Find **YouTube trailers** using **DuckDuckGo Search**
- 🎞️ Detect **movie franchises** & suggest full lists
- 💾 **Caches searches** using SQLite for faster results
- 🎨 **Modern UI with rounded chat bubbles**
- 🗑️ **Clear Chat button to reset the conversation**

## ⚙️ Installation

1. **Clone the repository** (if using GitHub):
   ```sh
   git clone https://github.com/yourusername/movie-chatbot.git
   cd movie-chatbot

2. Install dependencies:

   pip requirements.txt

3.Run the chatbot:

    python main.py

💡 How to Use

    Enter a movie name in the chat box and press Enter.
    The bot fetches movie details & trailers.
    If it's part of a franchise, the bot asks if you want a full list.
    Type "yes" to see all movies in the franchise.
    Use Clear Chat as needed.

🎬 Example Usage

    User:

        star wars

    Bot:

        🎬 Star Wars: Episode IV - A New Hope (1977)
        ⭐ IMDb Rating: 8.6
        📖 Plot: Luke Skywalker joins forces with a Jedi Knight...
        🎞️ Trailer: https://youtube.com/watch?v=example
        There are multiple movies with this title. Showing the first one made.
        Would you like a list of all movies in this franchise? (yes/no)

🛠️ Tech Stack

    Python 3.9+
    Tkinter (UI)
    IMDbPY (Movie data)
    DuckDuckGo Search (Trailer links)
    SQLite (Caching)

🚀 Approach & Challenges

    🔹 How We Approached the Project

    I aimed to build an interactive chatbot that seamlessly fetches movie details & trailers while maintaining a clean, user-friendly interface.
    Key steps in our approach:

        Used IMDbPY for accurate movie data retrieval.
        Implemented DuckDuckGo Search to fetch YouTube trailer links.
        Optimized with SQLite to prevent redundant API calls.
        Designed a sleek UI with separate chat bubbles for an improved experience.

    🔹 Hurdles We Encountered

    1️⃣ Handling Movie Franchises:

        Initially, the chatbot asked for franchise lists too early before displaying movie details.
        Fixed by ensuring IMDb details load first, then detecting franchises.

    2️⃣ DuckDuckGo Search Rate Limits:

        Sometimes failed to fetch trailers due to search limits.
        Implemented caching in SQLite to reduce unnecessary searches.

    If I had more time I would improved how the bot chats and the UI.

📝 License

    MIT License

🚀 Built with Python for movie lovers! 🎥🍿

    ---

    ### **✅ What’s Updated in This Version?**
    ---
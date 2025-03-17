import tkinter as tk
from tkinter import scrolledtext
import asyncio
import sqlite3
from imdb import IMDb
import threading
from duckduckgo_search import DDGS

awaiting_response = None  # Tracks if bot is waiting for a "yes/no" response

# SQLite Database Setup for Caching
conn = sqlite3.connect("movie_cache.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS movies (title TEXT PRIMARY KEY, year TEXT, rating TEXT, plot TEXT, trailer TEXT)""")
conn.commit()

# IMDb API Setup
ia = IMDb()

# ✅ Function to Update Chat with Separate Rounded Bubbles
def update_chat(role, messages):
    chat_display.config(state="normal")

    if isinstance(messages, str):
        messages = [messages]  # Ensure separate bubbles

    for message in messages:
        chat_bg = "#007BFF" if role == "You" else "#E9ECEF"
        chat_fg = "white" if role == "You" else "black"
        align = "right" if role == "You" else "left"
        tag = "user" if role == "You" else "bot"

        chat_display.insert(tk.END, "\n", tag)
        chat_display.insert(tk.END, f" {message} ", tag)
        chat_display.insert(tk.END, "\n", tag)

        chat_display.tag_config(tag, background=chat_bg, foreground=chat_fg, font=("Arial", 12), 
                                lmargin1=20, lmargin2=20, rmargin=20, spacing1=8, spacing3=8, wrap="word")
        chat_display.tag_configure(tag, justify=align)

    chat_display.config(state="disabled")
    chat_display.yview(tk.END)

# ✅ Function to Clear Chat
def clear_chat():
    chat_display.config(state="normal")
    chat_display.delete("1.0", tk.END)
    chat_display.config(state="disabled")

# ✅ Function to Fetch Movie Details from IMDb
async def search_imdb(movie_name):
    cursor.execute("SELECT * FROM movies WHERE title=?", (movie_name,))
    cached_movie = cursor.fetchone()

    if cached_movie:
        return {
            "title": cached_movie[0],
            "year": cached_movie[1],
            "rating": cached_movie[2],
            "plot": cached_movie[3],
            "trailer": cached_movie[4]
        }

    loop = asyncio.get_running_loop()
    results = await loop.run_in_executor(None, ia.search_movie, movie_name)
    
    if not results:
        return None

    movie = sorted(results, key=lambda m: m.get('year', 9999))[0]
    ia.update(movie)
    
    trailer_link = await search_youtube_trailer(movie.get('title'))

    movie_data = {
        "title": movie.get('title'),
        "year": str(movie.get('year', "N/A")),
        "rating": str(movie.get('rating', "N/A")),
        "plot": movie.get('plot', ["No plot available"])[0],
        "trailer": trailer_link
    }
    
    cursor.execute("INSERT OR REPLACE INTO movies VALUES (?, ?, ?, ?, ?)", 
                   (movie_data["title"], movie_data["year"], movie_data["rating"], movie_data["plot"], movie_data["trailer"]))
    conn.commit()
    
    return movie_data

# ✅ Function to Fetch Trailer using DuckDuckGo
async def search_youtube_trailer(movie_name):
    query = f"{movie_name} official trailer site:youtube.com"
    
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=5)

    for result in results:
        if "youtube.com/watch" in result["href"]:
            return result["href"]

    return "No trailer found."

# ✅ Function to Handle User Input
def search_movie():
    user_input = entry.get().strip()
    entry.delete(0, tk.END)
    
    if not user_input:
        return

    update_chat("You", user_input)
    threading.Thread(target=asyncio.run, args=(search_movie_async(user_input),), daemon=True).start()

# ✅ Async Function for Searching Movies
async def search_movie_async(user_input):
    global awaiting_response

    update_chat("Bot", "...typing...")

    if awaiting_response and user_input.lower() in ["yes", "no"]:
        if user_input.lower() == "yes":
            await list_movies(awaiting_response)  
        awaiting_response = None  
        return

    movie_info = await search_imdb(user_input)

    if not movie_info:
        update_chat("Bot", "Sorry, I couldn't find any movie with that title.")
        return

    update_chat("Bot", f"🎬 **{movie_info['title']}** ({movie_info['year']})")
    update_chat("Bot", f"⭐ IMDb Rating: {movie_info['rating']}")
    update_chat("Bot", f"📖 Plot: {movie_info['plot']}")
    
    trailer_link = await search_youtube_trailer(user_input)
    update_chat("Bot", f"🎞️ Trailer: {trailer_link}")

    search_results = ia.search_movie(user_input)
    if len(search_results) > 1:
        update_chat("Bot", "There are multiple movies with this title. Showing the first one made.")
        update_chat("Bot", "Would you like a list of all movies in this franchise? (yes/no)")
        awaiting_response = user_input

async def list_movies(movie_name):
    search_results = ia.search_movie(movie_name)
    movie_list = sorted(search_results, key=lambda m: m.get('year', 9999))

    update_chat("Bot", "Here is the full list of movies in the franchise:")

    for movie in movie_list:
        update_chat("Bot", f"- {movie.get('title', 'Unknown')} ({movie.get('year', 'N/A')})")

# 🎨 GUI Setup - Modern UI
root = tk.Tk()
root.title("Movie Research Assistant")
root.geometry("900x650")
root.configure(bg="#F4F6F9") 

root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# 📌 Title Bar
tk.Label(root, text="Movie Research Assistant", font=("Arial", 16, "bold"), bg="#3A7CA5", fg="white", pady=8).pack(fill="x")

# 📝 Chat Display - Modernized
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=25, width=80, state="disabled",
                                         bg="white", fg="black", font=("Arial", 12), relief="flat", bd=0, padx=10, pady=5)
chat_display.pack(expand=True, fill="both", padx=10, pady=5)
chat_display.tag_config("user", foreground="#007BFF", font=("Arial", 12, "bold"))
chat_display.tag_config("bot", foreground="#28A745", font=("Arial", 12, "italic"))

# ✏️ Input Box
entry_frame = tk.Frame(root, bg="white", bd=2, relief="sunken")
entry_frame.pack(fill="x", padx=10, pady=5)

entry = tk.Entry(entry_frame, width=80, bg="white", fg="black", font=("Arial", 12), insertbackground="black", relief="flat")
entry.pack(side="left", expand=True, fill="x", padx=10, pady=5)
entry.bind("<Return>", lambda event: search_movie())

# 🚀 Send, Clear, and Dark Mode Buttons
button_frame = tk.Frame(root, bg="white")
button_frame.pack(fill="x", padx=10, pady=5)

send_button = tk.Button(button_frame, text="Send", command=search_movie, font=("Arial", 12, "bold"),
                        bg="#007BFF", fg="white", relief="flat", padx=15, pady=5)
send_button.pack(side="left", padx=5, pady=5)

clear_button = tk.Button(button_frame, text="Clear Chat", command=clear_chat, font=("Arial", 12),
                         bg="#DC3545", fg="white", relief="flat", padx=10, pady=5)
clear_button.pack(side="left", padx=5, pady=5)

root.mainloop()
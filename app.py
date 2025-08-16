from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# ========== set up API keys ==========
# giphy
GIPHY_KEY = "***REMOVED***"
R_CAT_KEY = "https://www.reddit.com/r/cats"
# for reddit, just use subreddit api public json

# ========== indexing ==========
@app.route("/", methods=["GET", "POST"])
def index():
    query = ""
    results = []

    if request.method == "POST":
        query = request.form["query"]

        # === giphy ===
        giphy_limit = 5
        giphy_url = f"https://api.giphy.com/v1/gifs/search?api_key={GIPHY_KEY}&q={query}&limit={giphy_limit}"
        try:
            giphy_res = requests.get(giphy_url).json()
            gifs = [gif["images"]["downsized_medium"]["url"] for gif in giphy_res.get("data", [])]
            results.extend(gifs)
        except Exception as e:
            print("Giphy error:", e)

        # === reddit ===
        reddit_limit = 10
        reddit_url = f"{R_CAT_KEY}/search.json?q={query}&restrict_sr=1&limit={reddit_limit}"
        try:
            reddit_res = requests.get(reddit_url, headers={"User-agent": "conical-cat/0.1"}).json()
            posts = [post["data"]["url"] for post in reddit_res["data"]["children"]]
            results.extend(posts)
        except Exception as e:
            print("Reddit error:", e)

    return render_template("index.html", query=query, results=results)

if __name__ == "__main__":
    app.run(debug=True)

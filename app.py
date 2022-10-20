import os

from update_summarizer import app

if __name__ == "__main__":
    app.run(debug=True, port=os.getenv("PORT") or 8080)
from flask import Flask, request, redirect, url_for, render_template_string

app = Flask(__name__)

books = [
    {"id": 1, "title": "The Alchemist", "author": "Paulo Coelho", "owner": "Ananya", "status": "Available"},
    {"id": 2, "title": "Wings of Fire", "author": "A. P. J. Abdul Kalam", "owner": "Rahul", "status": "Available"},
    {"id": 3, "title": "Atomic Habits", "author": "James Clear", "owner": "Meera", "status": "Requested"},
]
next_id = 4

PAGE = """
<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>BookLoop | Book Exchange Portal</title>
<style>
*{box-sizing:border-box}body{margin:0;font-family:Arial,sans-serif;background:#f3f6fb;color:#172033}
header{background:#243b70;color:white;padding:24px max(5%,calc((100% - 1050px)/2))}
header h1{margin:0 0 7px;font-size:30px}header p{margin:0;color:#dce6ff}
main{max-width:1050px;margin:28px auto;padding:0 18px}.intro{background:white;padding:20px;border-radius:14px;box-shadow:0 4px 18px #1d355710}
h2{margin-top:0}.layout{display:grid;grid-template-columns:2fr 1fr;gap:18px;margin-top:18px}
.panel{background:white;padding:20px;border-radius:14px;box-shadow:0 4px 18px #1d355710}
.book{border:1px solid #e3e8f1;border-radius:10px;padding:14px;margin:12px 0}
.book h3{margin:0 0 7px}.muted{color:#63708a;font-size:14px}.status{display:inline-block;background:#e8f7ef;color:#187245;padding:5px 9px;border-radius:20px;font-size:12px}
label{display:block;font-size:14px;margin:12px 0 5px}input{width:100%;padding:10px;border:1px solid #cbd4e2;border-radius:8px}
button{margin-top:14px;border:0;border-radius:8px;padding:11px 14px;background:#3159a6;color:white;cursor:pointer;font-weight:bold}
.notice{background:#e8f7ef;padding:10px;border-radius:8px;color:#187245;margin:12px 0}
footer{text-align:center;color:#69758b;padding:22px;font-size:13px}
@media(max-width:700px){.layout{grid-template-columns:1fr}header h1{font-size:25px}}
</style></head>
<body>
<header><h1>📚 BookLoop</h1><p>A simple community book exchange portal</p></header>
<main>
<section class="intro"><h2>Share a book. Discover your next read.</h2>
<p>List books you can exchange with other readers. Browse the community collection and add your own book below.</p>
<strong>{{ books|length }} books listed</strong>
{% if message %}<div class="notice">{{ message }}</div>{% endif %}
</section>
<div class="layout">
<section class="panel"><h2>Community bookshelf</h2>
{% for book in books %}
<div class="book"><h3>{{ book.title }}</h3><div class="muted">By {{ book.author }} · Listed by {{ book.owner }}</div>
<p><span class="status">{{ book.status }}</span></p></div>
{% endfor %}
</section>
<section class="panel"><h2>List a book</h2><p class="muted">Add a book to the exchange list.</p>
<form method="post" action="{{ url_for('add_book') }}">
<label for="title">Book title</label><input id="title" name="title" required maxlength="80" placeholder="e.g. The Hobbit">
<label for="author">Author</label><input id="author" name="author" required maxlength="80" placeholder="Author name">
<label for="owner">Your name</label><input id="owner" name="owner" required maxlength="50" placeholder="Your name">
<button type="submit">Add book</button></form>
</section></div></main><footer>BookLoop · DevOps case study · Flask + Docker + Kubernetes + Jenkins</footer>
</body></html>
"""

@app.get("/")
def home():
    return render_template_string(PAGE, books=books, message=request.args.get("message", ""))

@app.post("/add")
def add_book():
    global next_id
    title = request.form.get("title", "").strip()
    author = request.form.get("author", "").strip()
    owner = request.form.get("owner", "").strip()
    if not (title and author and owner):
        return redirect(url_for("home", message="Please complete all fields."))
    books.append({"id": next_id, "title": title, "author": author, "owner": owner, "status": "Available"})
    next_id += 1
    return redirect(url_for("home", message="Your book was added to the community bookshelf!"))

@app.get("/health")
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

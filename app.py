from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def index():
    """Render the index page and display all blog posts."""
    with open('blog_posts.json') as file:
        blog_posts = json.load(file)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    """Handle adding a new blog post."""
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        with open('blog_posts.json') as file:
            blog_posts = json.load(file)
        if blog_posts:
            new_id = blog_posts[-1]['id'] + 1
        else:
            new_id = 1
        new_post = {
            "id": new_id,
            "author": author,
            "title": title,
            "content": content,
            "likes": 0
        }
        blog_posts.append(new_post)
        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    """Handle deleting a blog post by its ID."""
    with open('blog_posts.json') as file:
        blog_posts = json.load(file)
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    with open('blog_posts.json', 'w') as file:
        json.dump(blog_posts, file)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    """Handle updating a blog post by its ID."""
    if request.method == 'POST':
        author = request.form.get('author')
        title = request.form.get('title')
        content = request.form.get('content')
        with open('blog_posts.json', 'r') as file:
            blog_posts = json.load(file)
        for post in blog_posts:
            if post['id'] == post_id:
                post['author'] = author
                post['title'] = title
                post['content'] = content
                break
        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file)
        return redirect(url_for('index'))
    else:
        with open('blog_posts.json', 'r') as file:
            blog_posts = json.load(file)
        for post in blog_posts:
            if post['id'] == post_id:
                current_post = post
                break
        else:
            return 'Post not found', 404
        return render_template('update.html', post=current_post)


@app.route('/like/<int:post_id>')
def like(post_id):
    """Handle implementing the likes count of a blog post by its ID."""
    with open('blog_posts.json') as file:
        blog_posts = json.load(file)
    for post in blog_posts:
        if post['id'] == post_id:
            post['likes'] += 1
            break
    with open('blog_posts.json', 'w') as file:
        json.dump(blog_posts, file)
    return redirect(url_for('index'))


if __name__ == "__main__":
    """Start the Flask application."""
    app.run(host="0.0.0.0", port=5000)

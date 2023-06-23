from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)


@app.route('/')
def index():
    with open('blog_posts.json') as file:
        blog_posts = json.load(file)
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
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
        blog_posts.append({"id": new_id, "author": author, "title": title, "content": content})
        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/delete/<int:post_id>')
def delete(post_id):
    with open('blog_posts.json') as file:
        blog_posts = json.load(file)
    blog_posts = [post for post in blog_posts if post['id'] != post_id]
    with open('blog_posts.json', 'w') as file:
        json.dump(blog_posts, file)
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    with open('blog_posts.json') as file:
        blog_posts = json.load(file)
    post = next((post for post in blog_posts if post['id'] == post_id), None)
    if post is None:
        return "Post not found", 404
    if request.method == 'POST':
        post['author'] = request.form.get('author')
        post['title'] = request.form.get('title')
        post['content'] = request.form.get('content')
        with open('blog_posts.json', 'w') as file:
            json.dump(blog_posts, file)
        return redirect(url_for('index'))
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)

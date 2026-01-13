from flask import Flask, render_template, url_for

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/gene')
def gene():
    test: list = ["hello", "IM", " testing", " my", "app", " testing", " my", "app", " testing", " my", "app"]
    test1: list = []
    for i in test:
        test1.append(f"<div class=\"container\">{i}</div>")

    return render_template('gene.html', item=test1)



        


if __name__ == "__main__":
    app.run(debug=True)

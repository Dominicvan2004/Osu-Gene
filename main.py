from flask import (
Flask, 
render_template, 
request
)
from Osu_gene.main import osu_gene
import asyncio as a 

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/projects')
def projects():
    return render_template('projects.html')

@app.route('/gene', methods=["GET", "POST"])
def gene():
    # test: list = ["hello", "IM", " testing", " my", "app", " testing", " my", "app", " testing", " my", "app"]
    # test1: list = []
    # for i in test:
    #     test1.append(f"<div class=\"container\">{i}</div>")\

    item0: list = []
    item1: list = []

    if request.method == "POST":
        item1 = a.run(osu_gene(request.form['id']))
        return render_template('gene.html', item=item1)
    else:
        return render_template('gene.html', item=item0)
    



        


if __name__ == "__main__":
    app.run(debug=True)

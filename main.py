from flask import (
Flask, 
render_template, 
request
)
from Osu_gene.osu_gene import osu_gene
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

    empty_list: list = []
    filled_list: list = []

    if request.method == "POST":
        filled_list = a.run(osu_gene(request.form['id']))
        return render_template('gene.html', item=filled_list)
    else:
        return render_template('gene.html', item=empty_list)
    


        


if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, send_file
from sof import get_jobs as get_sof_jobs
from wwr import get_jobs as get_wwr_jobs
from rok import get_jobs as get_rok_jobs
from save import save_to_file

app = Flask(__name__)

fakeDB = {}


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/report')
def report():
    word = request.args.get('word')

    if word:
        word = word.lower()
        fromDB = fakeDB.get(word)

        if fromDB:
            jobs = fromDB
        else:
            sof_jobs = get_sof_jobs(word)
            wwr_jobs = get_wwr_jobs(word)
            rok_jobs = get_rok_jobs(word)
            jobs = sof_jobs + wwr_jobs + rok_jobs
            
            fakeDB[word] = jobs

    else:
        return redirect('/')

    return render_template('home.html',
                           searchingBy=word,
                           resultsNumber=len(jobs),
                           jobs=jobs)


@app.route('/export')
def export():
    try:
        word = request.args.get('word')

        if not word:
            raise Exception()
        word = word.lower()
        jobs = fakeDB.get(word)

        if not jobs:
            raise Exception()

        save_to_file(jobs)

        return send_file('jobs.csv')

    except:
        return redirect('/')


if __name__=="__main__":
    app.run(host="127.0.0.1", port="5000", debug=True)

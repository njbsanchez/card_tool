from flask import render_template, request, flash, redirect, url_for
from app import app
from flask_wtf import form
import time
import datetime


import roadmap_card_scraper as rm
import analyze as az


@app.route("/", methods=['GET', 'POST'])
def go_home():
    
    enviro = ['author', 'proof', 'truth', 'production']
    roadmap_type = ['data-center', 'cloud']
    
    if request.method == "POST":
        # print(request.form['enviro'])
        # print(request.form['roadmap_type'])
        env = request.form['enviro']
        type = request.form['roadmap_type']
        rm.parse_roadmap(type, env)
        # return render_template('done.html', env, type)
        return render_template('done.html', environment=env, type=type, filename=filename)
    
    enviro = ['author', 'proof', 'truth', 'production']
    roadmap_type = ['data-center', 'cloud']
    
    if request.method == "POST":

        path = request.form['path']
        enviroment = request.form['enviro']
        type = request.form['roadmap_type']
        filename = az.analyze_scrape(path, type, enviroment)
        
        return redirect(url_for("go_qa", environment=enviro, type=type, filename=filename, **request.args))
    
    return render_template('homepage.html',
                           enviro=enviro, 
                           roadmap_type=roadmap_type)

# @app.route("/card-scraper", methods=['GET', 'POST'])
# def go_scrape():
#     enviro = ['author', 'proof', 'truth', 'production']
#     roadmap_type = ['data-center', 'cloud']
    
#     if request.method == "POST":
#         # print(request.form['enviro'])
#         # print(request.form['roadmap_type'])
#         env = request.form['enviro']
#         type = request.form['roadmap_type']
#         filename = rm.parse_roadmap(type, env)
#         # return render_template('done.html', env, type)
#         return render_template('done.html', environment=env, type=type, filename=filename)
    
#     return render_template('scraper.html', 
#                            enviro=enviro, 
#                            roadmap_type=roadmap_type)

@app.route("/card-qa/<enviro>/<path>/<roadmap_type>", methods=['GET', 'POST'])

def go_qa(enviro, path, roadmap_type):

    filename = az.analyze_scrape(path, type, enviro)
    
    return render_template('done.html')
    
    # return render_template('analyze.html', 
    #                        enviro=enviro, 
    #                        roadmap_type=roadmap_type)



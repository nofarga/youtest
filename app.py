from datetime import date
from pyexpat import model
from flask import Flask,url_for,render_template,request,url_for,redirect,flash,send_from_directory
from werkzeug.utils import secure_filename
import pandas as pd
from sklearn.model_selection import train_test_split # Import train_test_split function
# import pickle
import openpyxl
from sklearn.datasets import load_iris
from sklearn.metrics import accuracy_score
import numpy
import datetime
import os
# import Orange

app = Flask(__name__,template_folder='./templates',static_folder='./static')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='images/favicon.png')

# @app.route('youtest1.herokuapp.com', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def details_processing():
    arr=[]
    if request.method == 'POST':
        artist_Year = request.form.get('artist_Year')
        if artist_Year=='on':
            arr.append(1)
        else:
            arr.append(0)
        song_Year = request.form.get('song_Year')
        if song_Year=='on':
            arr.append(1)
        else:
            arr.append(0)
        seniority = request.form.get('seniority')
        arr.append(int(seniority))
        date_song = request.form.get('data')
        date=datetime.datetime.strptime(date_song, '%Y-%m-%d')
        arr.append(int(date.year))

        style = request.form.get('style')
        arr_style=[0,0,0,0,0,0]
        if style=='pop':
            arr_style[0]=1
        elif style=='dance':
            arr_style[1]=1
        elif style=='rap':
            arr_style[2]=1
        elif style=='middlee':
            arr_style[3]=1
        elif style=='balada':
            arr_style[4]=1
        elif style=='latin':
            arr_style[5]=1
        arr+=arr_style

        language_heb = request.form.get('language_heb')
        if language_heb=='on':
            arr.append(1)
        else:
            arr.append(0)
        duration = request.form.get('duration')
        arr.append(int(duration))

        author = request.form.get('author') #כותב
        arr_author=[0,0,0,0,0,0,0,0]
        if author=='staticbenal':
            arr_author[0]=1
        elif author=='stavbeger':
            arr_author[1]=1
        elif author=='tamardyonatank':
            arr_author[2]=1
        elif author=='aviohion':
            arr_author[3]=1
        elif author=='dolevrpenh':
            arr_author[4]=1
        elif author=='edenhason':
            arr_author[5]=1
        elif author=='dodornmadali':
            arr_author[6]=1
        elif author=='gil':
            arr_author[7]=1
        arr+=arr_author

        composer = request.form.get('composer') #מלחין
        arr_composer=[0,0,0,0,0,0,0,0]
        if composer=='staticbenal':
            arr_composer[0]=1
        elif composer=='stavbeger':
            arr_composer[1]=1
        elif composer=='tamardyonatank':
            arr_composer[2]=1
        elif composer=='aviohion':
            arr_composer[3]=1
        elif composer=='dolevrpenh':
            arr_composer[4]=1
        elif composer=='edenhason':
            arr_composer[5]=1
        elif composer=='dodornmadali':
            arr_composer[6]=1
        elif composer=='gil':
            arr_composer[7]=1
        arr+=arr_composer

        producer = request.form.get('producer') #מפיק
        arr_producer=[0,0,0,0]
        if producer=='stavbeger':
            arr_producer[0]=1
        elif producer=='yardenj':
            arr_producer[1]=1
        elif producer=='yakovlimai':
            arr_producer[2]=1
        elif producer=='yanonyahal':
            arr_producer[3]=1
        arr+=arr_producer

        records = request.form.get('records') #תקליטים
        arr_records=[0,0,0,0,0]
        if records=='NMC':
            arr_records[0]=1
        elif records=='tedi':
            arr_records[1]=1
        elif records=='liam':
            arr_records[2]=1
        elif records=='unicel':
            arr_records[3]=1
        elif records=='Mobile1music':
            arr_records[4]=1
        arr+=arr_records

        word_y = request.form.get('word_y')
        if word_y=='on':
            arr.append(1)
        else:
            arr.append(0)
        video = request.form.get('video')
        if video=='on':
            arr.append(1)
        else:
            arr.append(0)
            
        add_row(arr)
        arr_result=pick()
        res=int(arr_result[0][0])
        if res==1:
            str_res='לצערנו השיר שלך לא יצליח, אולי בפעם הבאה...'
        if res==0:
            str_res='! השיר שלך יהיה הצלחה'
        return render_template("total.html",result=str_res) 
    
    return render_template("hello.html", name=None) 


if __name__ == "__main__":
    app.run()

def add_row(arr):

    filename = './FINAL.xlsx'
    wb = openpyxl.load_workbook(filename=filename)
    sheet = wb['Sheet1']
    sheet.append(arr)
    wb.save(filename)

def pick():
    
    database = pd.read_excel('./FINAL.xlsx', dtype=float).to_numpy()
    file=open('./random_forest.pkcls', "rb")
    pkl = pd.read_pickle(file)

    dict_bin_a={0:[0,0],1:[1,0]}
    arr=[]
    for x in range(len(database[-1])):
        if x==2 or x==3 or x==11:
            arr.append(database[-1][x])
        elif x==2:
            arr.append(0)
        else:
            arr+=dict_bin_a.get(database[-1][x])
    row= numpy.array(arr)
    res=pkl.predict(row.reshape(1,-1))
    return res
from flask import Flask, render_template, request, redirect
import csv
from password_checker import *
from hackernews_project import *
from bs4 import BeautifulSoup
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')



@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

def write_to_csv(data):


    with open('./records/database.csv', mode='a', newline='') as database:
        email = data['e-mail']
        subject = data['subject']
        message = data['message']
        csv_writer = csv.writer(database, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([email,subject,message])



@app.route('/submit_email', methods=['POST', 'GET'])
def submit_email():
    if request.method =='POST' :
        data = request.form.to_dict()
        print(data)
        write_to_csv(data)
        return redirect('/thankyou.html')
    else :
        print('OOPS ! SOMETHING WENT WRONG, Try Again !!!')


@app.route('/password_checker_demo', methods=['POST', 'GET'])
def password_checker_demo():
    if request.method =='POST' :
        data = request.form.to_dict()
        result = main(list(data.values()))
    else :
        print('OOPS ! SOMETHING WENT WRONG, Try Again !!!')
    return '''
                <html>
                    <body>
                        <p>Your password is {result} times hacked.</p>
                        <p><a href="/work.html">Click here to check again</a>
                        <p><a href="/index.html">Click here to go homepage</a>
                    </body>
                </html>
            '''.format(result=result)

@app.route('/hackernews_demo', methods=['POST', 'GET'])
def hackernews_project_demo():
    if request.method =='POST' :
        res = requests.get('https://news.ycombinator.com/newest')
        soup = BeautifulSoup(res.text, 'html.parser')
        links = soup.select('.storylink')
        subtext = soup.select('.subtext')
        data = create_custom_hn(links,subtext)
    else :
        print('OOPS ! SOMETHING WENT WRONG, Try Again !!!')
    return '''
                <html>
                    <body>
                        <h1>current news related to programming world are :</h1><br><br><p>{data}</p><br>
                        <p><a href="/work2.html">Click here to go back.</a>
                        <p><a href="/index.html">Click here to go homepage.</a>
                    </body>
                </html>
            '''.format(data=data)
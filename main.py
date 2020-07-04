from flask import Flask, redirect, render_template, request
import os
import database
import requests

app = Flask(__name__)

"""

:route: index
:use: to create new URL shorts

"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Check that the website actually is accessible - no point putting a null site in the db
        full_url = request.form.get('newUrl')
        url_request = requests.get(full_url)
        if url_request.status_code == 200:
            ## Then they have entered an accessible site URL
            data = database.insert_into(full_url)
            code_url = f"{request.host}/{data['url_code']}"
            return render_template('new_url.html', full_url=full_url, code=data['url_code'], expiry=data['expiry_date'], code_url=code_url)
    return render_template('index.html')

"""

:route: rerouter
:use: to redirect the URL shorts

"""

@app.route('/<code>')
def rerouter(code):
    url = database.get_url_from_code(code)

    if url is not None:
        return redirect(url)
    
    return f'URL code: {code} does not exist :('


if __name__ == '__main__':
    try:
        os.system('clear')
    except:
        print('*' * 25)
    app.run(debug = True)
    
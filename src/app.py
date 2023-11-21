from flask import Flask, render_template, request, redirect, send_file, abort


from handlers.handler_form import handlerForm
from handlers.handler_xlsx import handlerJsonForXlsx
from view.views import showData
from config import get_token




app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        handler = handlerForm(request.form)
        handler()
        return redirect('/')
    return render_template('index.html')



@app.route('/views', methods=['POST', 'GET'])
def templates_url():
    showdata = showData()
    template = showdata.show_template
    filters = showdata.show_filter
    stop_word = showdata.show_stop_word
    if request.method == 'POST':
        handler = handlerForm(request.form)
        handler()
        return redirect('/views')
    return render_template('template.html', templates = template, filters = filters, stop_word = stop_word)



@app.route('/views/response', methods = ['POST', 'GET'])
def response_url():
    showdata = showData()
    response = showdata.show_response()
    return render_template('response.html', response = response)



@app.route('/getxlsx', methods=['POST', 'GET'])
def get_xlsx():
        handlerXlsx = handlerJsonForXlsx('feedbacks.xlsx')
        file_name = handlerXlsx.handler_feedback(get_token(), data_from=request.form['data_from'], data_to=request.form['data_to'], take=5000, skip=0)
        return send_file(file_name, as_attachment=True)


@app.route('/setstarttime', methods=['POST', 'GET'])
def set_time():
    if request.method == 'POST':
        print(request.form)
    return render_template('settings-time.html')


if __name__=='__main__':
    app.run(debug=True)
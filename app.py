from flask import Flask, render_template, request, redirect, url_for
import requests
import pandas
from bokeh.plotting import figure, output_file, save
from datetime import datetime
from dateutil.relativedelta import relativedelta

#some helper functions
def determineStartDate():
  current_time = datetime.today()
  earlier_time = current_time + relativedelta(months=-int(app.vars['timespan']))
  
  return earlier_time.strftime('%Y-%m-%d'), current_time.strftime('%Y-%m-%d')
  

def checkRequest():
  urlname = 'https://www.quandl.com/api/v3/datasets/WIKI/'
  urlname = urlname + app.vars['name_stock'] + '.json'
  urlname = urlname + '?order=asc&exclude_headers=true&column_index='+app.vars['button']

  if app.vars['timespan'] != '-1':
    starttime, endtime = determineStartDate()
    urlname = urlname + '&start_date=' + starttime + '&end_date=' + endtime

  urlname = urlname + '&collapse=' + app.vars['timeres'] + '&transformation=rdiff'
  urlname = urlname + '?api_key=8zAwUeJsnmGaDrJgEHrr'
  
  print urlname

  r = requests.get(urlname)

  return urlname, r.status_code

def requestData(urlname):

  
  df = pandas.read_json(urlname)
  df = df['dataset']

  return df

def plotData(df):
  
  dates = list(zip(*df['data'])[0])
  for i in range(0,len(dates)):
    dates[i] = datetime.strptime(dates[i],'%Y-%m-%d')
  values = list(zip(*df['data'])[1])

  output_file("templates/datetime.html")

  p = figure(width=800, height=250, x_axis_type="datetime", title="Stock Ticker Information")
  p.xaxis.axis_label = 'date'
  p.yaxis.axis_label = app.vars[app.vars['button']]
  p.line(dates, values, color='navy', alpha=0.5)
  p.circle(dates, values, color='navy', alpha=0.5, legend=app.vars['name_stock'])

  save(p)


# now the flask app
app = Flask(__name__)
app.vars = {}
app.vars['4'] = 'closing price'
app.vars['5'] = 'volume'
app.vars['11'] = 'adjusted closing price'

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():

  if request.method == 'GET':
    return render_template('index.html')
  else:
    app.vars['name_stock'] = request.form['name_stock']
    app.vars['button'] = request.form['button']
    app.vars['timespan'] = request.form['timespan']
    app.vars['timeres'] = request.form['timeres']

    urlname, status = checkRequest()

    print status

    if status == 200:
      df = requestData(urlname)
      plotData(df)

      return render_template('datetime.html')

    else:
      return render_template('error.html')

#@app.errorhandler(404)
#def page_not_found(e):
#  return render_template('404.html'), 404

#@app.errorhandler(500)
#def page_not_found(e):
#  return render_template('500.html'), 500

if __name__ == '__main__':
  app.run(port=33507)

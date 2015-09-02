from flask import Flask, render_template, request, redirect, url_for
import pandas
from bokeh.plotting import figure, output_file, save
from datetime import datetime

#some helper functions
def requestData(stockName, option='4'):
  urlname = 'https://www.quandl.com/api/v3/datasets/WIKI/'
  urlname = urlname + stockName + '.json'
  urlname = urlname + '?order=asc&exclude_headers=true&column_index='+option
  urlname = urlname + '&collapse=weekly&transformation=rdiff'
  
  print urlname
  
  df = pandas.read_json(urlname)
  df = df['dataset']

  return df

def plotData(df):
  
  dates = list(zip(*df['data'])[0])
  for i in range(0,len(dates)):
    dates[i] = datetime.strptime(dates[i],'%Y-%m-%d')
  values = list(zip(*df['data'])[1])

  output_file("templates/datetime.html")

  p = figure(width=800, height=250, x_axis_type="datetime")
  p.line(dates, values, color='navy', alpha=0.5)

  save(p)

# now the flask app
app = Flask(__name__)

@app.route('/')
def main():
  return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():

  if request.method == 'GET':
    return render_template('index.html')
  else:
    data_name = request.form['name_stock']
    print data_name
    data_button = request.form['button']
    print request.form['button']

    df = requestData(data_name,data_button)
    plotData(df)

    return render_template('back.html')


if __name__ == '__main__':
  app.run(port=33507)

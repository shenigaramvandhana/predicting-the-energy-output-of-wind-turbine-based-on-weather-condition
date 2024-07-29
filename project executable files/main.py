import pickle
from flask import Flask, render_template, request, url_for
from sklearn.ensemble import GradientBoostingRegressor

app = Flask(__name__)
model = pickle.load(open('Flask\\Scaler.pkl', 'rb'))


# model1 = pickle.load(open('model.pkl'),'rb')

@app.route('/',)
def home():
     
    return render_template("index.html")


@app.route('/predict_city',methods=["POST","GET"])
def predict_city():
    import requests
    apikey1='07437e2b01edda05f7f9ff0660c2517a'
    apikey='b6b9fef20bacb311bc34f6512cbd1585'
    # userinput = input("Enter city name: ")

    userinput = request.form.get('cityname')
    weather_data = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={userinput}&appid={apikey1}')
    # print(weather_data.json())
    data = weather_data.json()
    # print(f'temperature in {userinput} is {data["main"]["temp"]}')
    # print(f'max temperature in {userinput} is {data["main"]["temp_max"]}')
    # print(f'pressure in {userinput} is {data["main"]["pressure"]}')
    # print(f'humidity in {userinput} is {data["main"]["humidity"]}')
    # print(f'wind speed in {userinput} is {data["wind"]["speed"]}')
    
    windsp = data["wind"]["speed"]
    winddir = data["wind"]["deg"]
    maxtemp = data["main"]["temp_max"]
    hum = data["main"]["humidity"]
    press= data["main"]["pressure"]
    pred = model.predict([[windsp,winddir,maxtemp,hum,press]])
    
    
    return render_template('output1.html',predicted_energy=pred,userinput=userinput, windsp=windsp,winddir=winddir, maxtemp=maxtemp,hum=hum, press=press)




@app.route('/submit',methods=["POST","GET"])
def submit():
     if request.method == 'POST':
         windspeed = int(float(request.form.get('ws')))
         winddirection = int(float(request.form.get('wd')))
         maxtemp = int(float(request.form.get('mt')))
        #  windgust = int(float(request.form.get('wg')))
         humidity = int(float(request.form.get('h')))
         pressure = int(float(request.form.get('p')))
        #  print(f'wind speed is {windspeed}')
        #  print(f'Wind direction is {winddirection}')
        #  print(f'Max temp is {maxtemp}')
         pred1 = model.best_estimator_.predict([[windspeed, winddirection,maxtemp,humidity,pressure]])

         
     return render_template('output.html',predicted_energy=pred1)


if __name__ == '__main__':
    app.run(debug=True)


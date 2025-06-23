from flask import Flask, render_template, request
from fuzzy import predict_weather

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    suhu = float(request.form['suhu'])
    kelembaban = float(request.form['kelembaban'])
    angin = float(request.form['angin'])
    penyinaran = float(request.form['penyinaran'])

    result, score = predict_weather(suhu, kelembaban, angin, penyinaran)
    parameters = {
        'suhu': suhu,
        'kelembaban': kelembaban,
        'angin': angin,
        'penyinaran': penyinaran
    }

    return render_template('result.html', result=result, parameters=parameters, score=round(score, 2))



if __name__ == '__main__':
    app.run(debug=True, port=8080)


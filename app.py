from flask import Flask, request, render_template
import pickle

app = Flask(__name__)

# Memuat model dari file
with open('fuzzy_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

@app.route('/')
def index():
    return render_template('index.html', output='')

@app.route('/predict', methods=['POST'])
def predict():
    '''
    Predict based on user inputs
    and render the result to the html page
    '''
    d1, d2, d3, d4, d5, q3, q4, q10, q11, q12 = [x for x in request.form.values()]

    loaded_model.input['harga'] = (100 / 7) * float(q4)
    loaded_model.input['cuaca'] = (100 / 7) * float(q11)
    loaded_model.input['promosi'] = (100 / 7) * float(q12)
    loaded_model.compute()
    predicted_sales_loaded = loaded_model.output['penjualan']

    # Menampilkan output kategorikal dari model yang telah dimuat
    kategori_penjualan_loaded = None

    if predicted_sales_loaded <= 50:
        kategori_penjualan_loaded = "Rendah"
    elif predicted_sales_loaded <= 70:
        kategori_penjualan_loaded = "Sedang"
    else:
        kategori_penjualan_loaded = "Tinggi"

    return render_template('index.html', d1=d1, d2=d2, d3=d3, d4=d4, d5=d5, q3=konversi(int(q3)), q4=konversi(int(q4), q=1), q10=konversi(int(q10)), q11=konversi(int(q11), q=2), q12=konversi(int(q12), q=2), output=kategori_penjualan_loaded)


def konversi(nilai, q = 0):
    if nilai == 1:
        if q == 0:
            return 'Sangat Tidak Puas'
        elif q == 1:
            return 'Sangat Murah'
        else:
            return 'Sangat Tidak Sering'
    elif nilai == 2:
        if q == 0:
            return 'Tidak Puas'
        elif q == 1:
            return 'Murah'
        else:
            return 'Tidak Sering'
    elif nilai == 3:
        if q == 0:
            return 'Agak Tidak Puas'
        elif q == 1:
            return 'Agak Murah'
        else:
            return 'Tidak Sering'
    elif nilai == 4:
        if q == 0:
            return 'Netral'
        elif q == 1:
            return 'Sedang'
        else:
            return 'Sedang'
    elif nilai == 5:
        if q == 0:
            return 'Agak Puas'
        elif q == 1:
            return 'Agak Mahal'
        else:
            return 'Agak Sering'
    elif nilai == 6:
        if q == 0:
            return 'Puas'
        elif q == 1:
            return 'Mahal'
        else:
            return 'Sering'
    else:
        if q == 0:
            return 'Sangat Puas'
        elif q == 1:
            return 'Sangat Mahal'
        else:
            return 'Sangat Sering'


if __name__ == '__main__':
    app.run(debug=True)
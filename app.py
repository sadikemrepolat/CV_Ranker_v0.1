from flask import Flask, render_template, request, redirect, url_for
import os
import readPdf


app = Flask(__name__)

def my_function():
    return "BU BIR DENEME MESAJIDIR!"

# CV dosyalarının yükleneceği klasör
CV_UPLOAD_FOLDER = os.path.join(os.getcwd(), 'cv')
if not os.path.exists(CV_UPLOAD_FOLDER):
    os.makedirs(CV_UPLOAD_FOLDER)

# İlan dosyalarının yükleneceği klasör
ILAN_UPLOAD_FOLDER = os.path.join(os.getcwd(), 'ilan')
if not os.path.exists(ILAN_UPLOAD_FOLDER):
    os.makedirs(ILAN_UPLOAD_FOLDER)

app.config['CV_UPLOAD_FOLDER'] = CV_UPLOAD_FOLDER
app.config['ILAN_UPLOAD_FOLDER'] = ILAN_UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_files():
    # Gelen dosyaların ve hangi input alanından geldiklerinin kontrolü
    for input_name in request.files:
        files = request.files.getlist(input_name)

        for file in files:
            if file and (file.filename.endswith('.pdf') or file.filename.endswith('.docx')):
                # Hangi input alanından geldiğine göre dosyayı kaydet
                if input_name == 'ilanfile':
                    file.save(os.path.join(app.config['ILAN_UPLOAD_FOLDER'], file.filename))
                elif input_name == 'cvfile':
                    file.save(os.path.join(app.config['CV_UPLOAD_FOLDER'], file.filename))

    return redirect(url_for('index'))

@app.route('/display_result', methods=['POST'])
def display_result():
    try:
        sonuc = readPdf.start()
        print("Terminal: ", sonuc)  # Terminale yazdır
        sonuc = str(sonuc)
        sonuc.replace("\n","<br>")
        return sonuc  # Sonucu geri döndür
    except Exception as e:
        return str(e), 500  # Hata mesajını ve 500 kodunu döndür

if __name__ == '__main__':
    app.run(debug=True)
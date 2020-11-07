import os
from flask import Flask,render_template,request,send_file
from PyPDF2 import PdfFileMerger

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/", methods = ["POST"])
def pdfMerge():
    merger = PdfFileMerger()
    files = request.files.getlist("file")
    fileName = request.form.get("fileName")+'.pdf'
    for file in files:
            merger.append(file)
    merger.write(f'./output/{fileName}')
    merger.close()
    files = os.listdir('output')
    files = [file for file in files]
    return render_template('index.html', files=files)

@app.route('/output/<filename>')
def read_json(filename, static_folder="output"):
    pdfFileObj = os.path.join(static_folder, filename)
    return send_file(pdfFileObj)

if __name__ == "__main__":
    app.run(debug = True)
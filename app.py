import os
from flask import Flask,render_template,request,send_file,redirect,url_for
from PyPDF2 import PdfFileMerger
from pdf2image import convert_from_path
from PIL import Image

currentPath = os.getcwd()
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = currentPath

@app.route("/")
def index():
    files = os.listdir('output')
    files = [file for file in files]
    return render_template("index.html", files= files)

@app.route("/", methods = ["POST"])
def pdfMerge():
    merger = PdfFileMerger()
    files = request.files.getlist("file")
    fileName = request.form.get("fileName")+'.pdf'
    for file in files:
            merger.append(file)
    merger.write(f'./output/{fileName}')
    merger.close()
    return redirect(url_for('index'))

@app.route("/pdfToImage", methods=["POST"] )
def pdfToImage():
    file = request.files.get("pdfFile")
    pdfName = request.form.get("pdfName")+'.jpg'
    pathUrl = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    image = convert_from_path(pathUrl)
    image.save(f'output/{pdfName}', 'JPEG')
    return redirect(url_for('index'))

@app.route("/imageToPdf", methods=["POST"] )
def imageToPdf():
    file = request.files.get("imageFile")
    imgName = request.form.get("imageName")+'.pdf'
    image = Image.open(file)
    img = image.convert('RGB')
    img.save(f'output/{imgName}')
    return redirect(url_for('index'))

@app.route('/output/<filename>')
def read_json(filename, static_folder="output"):
    pdfFileObj = os.path.join(static_folder, filename)
    return send_file(pdfFileObj)

if __name__ == "__main__":
    app.run(debug = True)
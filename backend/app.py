from flask import Flask, jsonify, request
from sklearn.externals import joblib
import cv2
import os
import pytesseract
import io
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage

from flask_cors import CORS, cross_origin

pytesseract.pytesseract.tesseract_cmd = r'/usr/local/Cellar/tesseract/4.0.0/bin/tesseract'

app = Flask(__name__)
CORS(app)

@app.route('/image/<img_path>')
def summariseimage(img_path):
    # Read image using opencv
   
    img = cv2.imread(img_path)
    

    # Extract the file name without the file extension
    file_name = os.path.basename(img_path).split('.')[0]
    file_name = file_name.split()[0]

    # Create a directory for outputs
    output_path = os.path.join('Save1', file_name)
    if not os.path.exists(output_path):
        os.makedirs(output_path)
      # Save the filtered image in the output directory
   # save_path = os.path.join(output_path, file_name + "_filter_" + str(method) + ".jpg")
   # cv2.imwrite(save_path, img)

    # Recognize text with tesseract for python
    result = pytesseract.image_to_string(img, lang="eng")
    r=[
        {
            'text':result
        }]
    return  jsonify({'emp':r})

@app.route('/pdf/<path>')
def summarisepdf(path):
    # Read image using opencv
   
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    r=[
        {
            'text':text
        }]
    return  jsonify({'emp':r})

if __name__ == '__main__':
   app.run(debug = True)
import os

from flask import render_template, redirect, request, \
    url_for, flash, current_app, make_response
from werkzeug.utils import secure_filename

from . import o2sc
from converter import Converter
from zip import Zip

ALLOWED_EXTENSIONS = set(['txt', 'csv', 'zip'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@o2sc.route('/o2sc', methods=['GET', 'POST'])
def o2sc():
    app = current_app._get_current_object()
    if request.method == 'POST':
        # get the form data
        file = request.files['file']
        delimiter = str(request.form['delimiter'])
        quote_char = str(request.form['quote-char'])
        doc_type = str(request.form['doc-type'])
        file_path_field = str(request.form['file-path-field'])
        unique_id = str(request.form['unique-id'])
        omit = str(request.form['omit'])
        header_mapping = str(request.form['header-mapping'])

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            c = Converter()

            if '.zip' in filename:
                z = Zip()
                extracted_list = z.unzip(app.config['UPLOAD_FOLDER'], filename)

                for filename in extracted_list:
                    c.convert_file(app.config['UPLOAD_FOLDER'],
                                   app.config['DOWNLOAD_FOLDER'],
                                   filename,
                                   delimiter,
                                   quote_char,
                                   doc_type,
                                   file_path_field,
                                   unique_id,
                                   omit,
                                   header_mapping)

                zip_archive = z.zip(app.config['DOWNLOAD_FOLDER'], extracted_list)
                response = make_response(zip_archive)
                response.headers["Content-Disposition"] = "attachment; filename=_converted_zip_archive.zip"
                return response

            else:
                converted_file = c.convert_file(app.config['UPLOAD_FOLDER'],
                                                app.config['DOWNLOAD_FOLDER'],
                                                filename,
                                                delimiter,
                                                quote_char,
                                                doc_type,
                                                file_path_field,
                                                unique_id,
                                                omit,
                                                header_mapping)
                response = make_response(converted_file)
                response.headers["Content-Disposition"] = "attachment; filename=_converted_" + filename
                return response
    return render_template('o2sc/upload.html')

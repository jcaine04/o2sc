import csv
import sys
import ast

import config
from app.o2sc.utilities import Utilities

class Converter(object):

    def __init__(self):
        self.u = Utilities()

    def convert_file(self, input_file_path, output_file_path, filename, delimiter, quotechar, doc_type,
                     file_name_field, omit, header_mapping):

        if len(quotechar) == 0:
            quotechar = None

        # Turn the omitted field into a list
        omit_list = omit.split(',')
        omit_list = [i.strip() for i in omit_list]

        if len(omit_list[0]) == 0:
            omit_list = None

        # Turn the header mapping into a dictionary
        header_mapping_dict = ast.literal_eval('{' + header_mapping + '}')

        try:
            f = open(input_file_path + filename, 'rb')
        except IOError:
            print "Couldn't open source file"
            sys.exit()

        if quotechar:
            d = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        else:
            d = csv.DictReader(f, delimiter=delimiter)

        try:
            out_file = open(output_file_path + filename, 'wb')
        except IOError:
            print "Couldn't open out file"
            sys.exit()

        out_file.write('>>>>Self Configuring Tagged DIP<<<<' + '\n')
        for r in d:
            out_file.write('BEGIN:' + '\n')

            # write out mapped values first
            if header_mapping_dict:
                for i in header_mapping_dict:
                    out_file.write(header_mapping_dict[i] + ': ' + r[i] + '\n')

            # write out the file type num
            out_file.write('>>FileTypeNum: ' + self.u.get_file_type_num(r[file_name_field]) + '\n')

            # write out doc type name, if needed
            if doc_type:
                out_file.write('>>DocType: ' + doc_type)

            # remove omitted values
            if omit_list:
                for i in omit_list:
                    del r[i]

            # write out the rest of the values
            for key, value in r.iteritems():
                if value:
                    out_file.write(str(key) + ': ' + str(value) + '\n')
        out_file.write('END:' + '\n')
        out_file.close()
        completed_file = open(output_file_path + filename, 'rb').read()
        return completed_file
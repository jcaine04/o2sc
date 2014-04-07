import csv
import sys
import ast

from .utilities import Utilities


class Converter(object):

    def __init__(self):
        self.u = Utilities()

    def convert_file(self, input_file_path, output_file_path, filename, delimiter, quotechar, doc_type,
                     file_path_field, unique_id, omit, header_mapping, return_file=True):
        """Convert ordered dip filed to self-configured

        Keyword arguments:
        input_file_path -- The path to the input file (excluding filename)
        output_file_path -- The path to the output file (excluding filename)
        filename -- Input and output filename
        delimiter -- Delimiter in the input file
        quotechar -- Quote Character used in the input file
        doc_type -- Doc Type used for all documents
        file_path_field -- The header name in the input file that contains the full path to the file
        unique_id -- The header that contains the unique identifier for a document
        omit -- List of headers to omit from the input file
        header_mapping -- Dictionary mapping header name to value to write out in the output file
        """

        # set the csv field size limit to max to handle large fields
        csv.field_size_limit(sys.maxsize)

        # If quotechar isn't set, set to None
        if len(quotechar) == 0:
            quotechar = None

        # Turn the omitted field into a list and strip whitespace from the ends
        omit_list = omit.split(',')
        omit_list = [i.strip() for i in omit_list]

        # If the list is empty, set to None
        if len(omit_list[0]) == 0:
            omit_list = []

        # Turn the header mapping into a dictionary
        header_mapping_dict = ast.literal_eval('{' + header_mapping + '}')

        # Open the input file
        try:
            f = open(input_file_path + filename, 'rb')
        except IOError:
            print "Couldn't open source file"
            sys.exit()

        # Build a dictionary from the csv
        if quotechar:
            d = csv.DictReader(f, delimiter=delimiter, quotechar=quotechar)
        else:
            d = csv.DictReader(f, delimiter=delimiter)

        # Open the output file
        try:
            out_file = open(output_file_path + filename, 'wb')
        except IOError:
            print "Couldn't open out file"
            sys.exit()

        # Write out the output file
        out_file.write('>>>>Self Configuring Tagged DIP<<<<' + '\n')

        # placeholder for unique id
        last_unique_id = ''
        current_unique_id = ''
        for r in d:
            # get the current unique id
            current_unique_id = r[unique_id]

            # if the current unique id equals the last, continue the document
            if current_unique_id == last_unique_id:

                out_file.write('>>FullPath: ' + r[file_path_field] + '\n')
                last_unique_id = current_unique_id

            else:  # else, begin a new document

                out_file.write('BEGIN:' + '\n')

                # write out mapped values
                if header_mapping_dict:
                    for i in header_mapping_dict:
                        out_file.write(header_mapping_dict[i] + ': ' + r[i] + '\n')

                # write out the file type num
                out_file.write('>>FileTypeNum: ' + self.u.get_file_type_num(r[file_path_field]) + '\n')

                # write out doc type name, if needed
                if doc_type:
                    out_file.write('>>DocType: ' + doc_type)

                # remove omitted values
                if omit_list:
                    for i in omit_list:
                        del r[i]

                # write out the rest of the values
                for key, value in r.iteritems():
                    if value and key != file_path_field:
                        out_file.write(str(key) + ': ' + str(value) + '\n')

                # write out the full path
                if r[file_path_field]:
                    out_file.write('>>FullPath: ' + r[file_path_field] + '\n')

                # set the last unique id
                last_unique_id = r[unique_id]

        out_file.write('END:' + '\n')

        # Close out the output file
        out_file.close()
        if return_file:
            # Read in the output file and return it
            completed_file = open(output_file_path + filename, 'rb').read()
            return completed_file


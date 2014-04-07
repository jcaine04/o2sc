import zipfile
import sys
import os


class Zip(object):

    def __init__(self):
        pass

    def unzip(self, zip_file_path, zip_file_name):

        try:
            z = zipfile.ZipFile(zip_file_path + zip_file_name)
        except zipfile.BadZipfile:
            print "File is not a valid ZIP archive."
            sys.exit()

        names = z.namelist()
        for n in names:
            try:
                z.extract(n, zip_file_path)
            except:
                print "Could not extract file: %s" % n

        return names

    def zip(self, file_path, filename_list):

        f = zipfile.ZipFile(os.path.join(file_path, '_converted_zip_archive.zip'), 'w')
        for filename in filename_list:
            f.write(file_path + filename)

        f.close()

        return open(file_path + '_converted_zip_archive.zip').read()

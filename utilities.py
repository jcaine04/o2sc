class Utilities(object):

    def __init__(self):
        self.file_type_num_dict = {
            'pdf': '16',
            'tif': '2',
            'jpg': '2',
            'png': '2',
            'doc': '12',
            'txt': '1',
            'xls': '13',
            'ppt': '14',
            'rtf': '15',
            'htm': '17',
            'avi': '18',
            'mov': '19',
            'wav': '20',
            'xml': '32',
            'msg': '36',
        }

    def get_file_type_num(self, file_path):

        try:
            file_extension = file_path.lower().rsplit('.', 1)[1]
        except IndexError:
            return 'Unknown File Format - No File Extension'

        file_type_num = self.file_type_num_dict.get(file_extension)

        if not file_type_num:
            return 'Unknown File Format - %s ' % file_extension
        else:
            return file_type_num
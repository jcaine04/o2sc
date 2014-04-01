class Utilities(object):

    def get_file_type_num(self, string):
        lc = string.lower()
        if '.pdf' in lc:
            return '16'
        elif '.tif' in lc:
            return '2'
        elif '.doc' in lc:
            return '12'
        elif '.txt' in lc:
            return '1'
        else:
            return 'Unknown File Format'
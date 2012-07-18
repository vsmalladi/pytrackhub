from collections import OrderedDict 

class Track(object):
    """ Base class for a track object. """

    def __init__(self,track_name=None,big_data_url=None,short_label=None,long_label=None,track_type=None):
        self.track_name = track_name
        self.big_data_url = big_data_url
        self.short_label = short_label
        self.long_label = long_label
        self.track_type = track_type
        self.ordered_attributes = OrderedDict()

    def order(self):
        """Order 5 basic attributes that should be set to match style of trackHubs"""
        self.ordered_attributes['trackName'] = self.track_name
        self.ordered_attributes['bigDataUrl'] = self.big_data_url
        self.ordered_attributes['shortLabel'] = self.short_label
        self.ordered_attributes['longLabel'] = self.long_label
        self.ordered_attributes['trackType'] =self.track_type

    def __str__(self):
        str = ''
        self.order()
        for var,val in self.ordered_attributes.items():
            str += var + ' ' + val + '\n'

        return str


    def write(self, fh):
        """Write track object into a file"""
        fh.write(str(self))
        fh.write('\n')

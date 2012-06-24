class Track(object):
    """ Base class for a track object. """

    def __init__(self,track_name=None,big_data_url=None,short_label=None,long_label=None,track_type=None):
        self.track_name = track_name
        self.big_data_url = big_data_url
        self.short_label = short_label
        self.long_label = long_label
        self.track_type = track_type

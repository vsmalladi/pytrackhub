from collections import OrderedDict
import os.path
import os


class Hub(object):
    """ Base class for a hub object. """

    def __init__(self, hub_name=None, short_label=None, long_label=None, email=None):
        self.hub_name = hub_name
        self.short_label = short_label
        self.long_label = long_label
        self.genomes_object = None
        self.email = email
        self.ordered_attributes = OrderedDict()

    def __order(self):
        """Order 5 basic attributes that should be set """
        self.ordered_attributes['hub'] = self.hub_name
        self.ordered_attributes['shortLabel'] = self.short_label
        self.ordered_attributes['longLabel'] = self.long_label
        self.ordered_attributes['genomesFile'] = self.genomes_object.genome_file
        self.ordered_attributes['email'] = self.email

    def __str__(self):
        str = ''
        self.__order()
        for var, val in self.ordered_attributes.items():
            str += var + ' ' + val + '\n'

        return str

    def add_genomes_object(self, genomes_object):
        """Add genome object to hub"""
        self.genomes_object = genomes_object

    def add_genome(self, genome_object):
        self.genomes_object.add_genome(genome_object)

    def __hub_directory(self, hub_dir):
        """Determines the path for where the hub will live"""
        if hub_dir is None:
            hub_path = os.getcwd()
        else:
            hub_path = hub_dir

        hub_object_path = os.path.join(hub_path, self.hub_name)

        if not os.path.exists(hub_object_path):
            os.mkdir(hub_object_path)

        return hub_object_path

    def write_hub_file(self, hub_file_place):
        """Write hub object into a file under directory named after the hub"""

        hub_file_path = os.path.join(hub_file_place, 'hub.txt')

        hub_file = open(hub_file_path, 'w')
        hub_file.write(str(self))
        hub_file.write('\n')
        hub_file.close()

    def write_hub_tree(self, hub_dir=None):
        """Write entire hub hierarchy"""

        hub_place = self.__hub_directory(hub_dir)

        self.write_hub_file(hub_place)
        self.genomes_object.write_genome_dir(hub_place)

import os
import os.path
import track

class GenomeStanza(object):
    """ Base class for genome stanza. """

    def __init__(self, genome=None, track_file="trackDb.txt"):
        self.genome = genome
        self.track_file = track_file #File Name only, no direcotry
        self.track_list = []

    def __str__(self):
        str = ''
        str += 'genome ' + self.genome + '\n'
        str += 'trackDb ' + self.genome + '/' + self.track_file + '\n'
        
        return str


    def add_track(self, track_object):
        """ Adds another track object into the list of tracks for a given genome"""
        self.track_list.append(track_object)

    def write_track(self, track_object):
        """Write out each track stanza in its own file"""
        track_object_path = os.path.join(self.genome,track_object.track_name)
        track_object_file = open(track_object_path + '.txt','w')
        track_object.write(track_object_file)
        track_object_file.close()

    def write_track_file(self):
        """Write the include file and loop through and write each tack object """
        if not os.path.exists(self.genome):
            os.mkdir(self.genome)
        
        track_file_path = os.path.join(self.genome,self.track_file)
        track_file = open(track_file_path,'w')
        
        for track in self.track_list:
            track_file.write('include ' + track.track_name + '.txt' + '\n')
            self.write_track(track)

        track_file.close()

    def write(self, fh):
        """Write genome listi into a file"""
        fh.write(str(self))
        fh.write('\n')
    

class GenomeFile(object):
    """" Class for holding all the genome stanza's. """

    def __init__(self,genome_file=None):
        self.genome_list = []
        self.genome_file = genome_file

    def __str__(self):
        str = ''
        for genome in self.genome_list:
            str += genome.__str__() + '\n'

        return str

    def add_genome(self, genome_object):
        """Adds another genome object into the list of genomes for a given trackHub """
        self.genome_list.append(genome_object)

    def write(self):
        """Write list of genomes out to a genome file."""
        genome_file = open(self.genome_file,'w')
        genome_file.write(str(self))
        genome_file.close()

    def write_genome_dir(self):
        """Write the files associated for a track in appropiate directory"""
        for genome in self.genome_list:
            genome.write_track_file()
    

    def add_track(self,genome_object,track_object):
        """Adds another track object into the list for a given genome_object"""
        try:
            genome_object.add_track(track_object)
        except:
            raise LookupError("Genome not known " + genome_object)


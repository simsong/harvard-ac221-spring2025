"""
experiment_runner.py: reads the templatedb.tsv and probes.tsv files and runs the experiment
"""

import csv
import os
from os.path import join,splitext,basename
import click
from deepface import DeepFace

# The template database:
templates = []

class Face:
    """This class reads a face for a given name from a file and
    creates the representation 9embedding) used by deepface."""
    def __init__(self, name, fname):
        """
        :param name: the person's name
        :param fname: the file name in which the jpeg is located.
        Note: .dfr will be an array of *all* the faces found
        """
        self.name  = name
        self.fname = fname
        self.dfr   = DeepFace.represent(fname)

    def verify(self, f2, **kwargs):
        """Compare this face to another.
        :param f2: A Face object for what we are comparing to.
        :param **kwargs: The other keyword args used by DeepFace.py's verify
        :return dict: Deepface's verify return.
              - 'verified' a bool for the same persion,
              - 'distance' the distance metric.
        Note - We could use self.dfr[0]['embeddings'] to grab the embeddings of the first image.
               that would be more efficient, but the code would be harder to understand
        """
        return DeepFace.verify(self.fname, f2.fname, **kwargs)

def search_templates( face ):
    """Search the database and find the best match"""
    closest_face = None
    closest_face_match = None
    for t in templates:
        match = t.verify( face )
        if match and match['verified']:
            if (closest_face is None) or (match['distance'] < closest_fact_match['distance']):
                closest_face = face
                closest_face_match = match
    return (closest_face, closest_face_match)


@click.command(context_settings={"show_default": True})
@click.option("--templatedb", type=click.Path(), help="Template DB output filename", default='templatedb.tsv')
@click.option("--probes", type=click.Path(), help="Probe DB output filename", default='probes.tsv')
@click.option("--output", type=click.Path(), help="Experiment output", default='experiment_output.tsv')
# pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals,too-many-branches
def experiment_runner(templatedb, probes, output):
    """Run the experiments"""

    # First build the template database
    click.echo("Loading database...")
    with open(templatedb,'r',encoding='utf-8') as f:
        tsv_reader = csv.DictReader(f, delimiter='\t')
        for row in tsv_reader:
            print(row['name'])
            templates.append(Face(name=row['name'], fname=row['fname']))

    click.echo("Verification starting...")
    # Now read each of the probes and print the results
    with open(probes, 'r', encoding='utf-8') as f:
        with open(output, 'w', encoding='utf-8') as o:
            tsv_reader = csv.DictReader(f, delimiter='\t')
            print(f"probe name\tprobe fname\tclosest db name\tclosest db fname\tdistance\tstatus")
            print(f"probe name\tprobe fname\tclosest db name\tclosest db fname\tdistance\tstatus",file=o)
            for row in tsv_reader:
                f = Face(name=row['name'], fname=row['fname'])
                (c,m) = search_templates( f )
                if c:
                    closest_name  = c.name
                    closest_fname = c.fname
                    distance      = m['distance']
                else:
                    closest_name  = 'None'
                    closest_fname  = 'None'
                    distance       = 'None'
                print(f"{row['name']}\t{basename(row['fname'])}\t{closest_name}\t{basename(closest_fname)}\t{distance:2.5}\t{row['status']}")
                print(f"{row['name']}\t{basename(row['fname'])}\t{closest_name}\t{basename(closest_fname)}\t{distance:2.5}\t{row['status']}",file=o)



if __name__ == "__main__":
    experiment_runner()          # pylint: disable=no-value-for-parameter

"""
experiment_maker.py: Create template-il and experiment-il files.
"""

import statistics
import os
import random
from os.path import join,splitext
import click


DEFAULT_FACE_DATA_DIR = join(os.getenv("HOME"),"facedata")
JPEG_EXTENSIONS = set(['.jpeg','.jpg'])
def is_jpeg(fname):
    """Return true if fname is a JPEG based on extension, not content"""
    return splitext(fname)[1].lower() in JPEG_EXTENSIONS

# Where we will collect the photos
photos = {}                     # name:[fname1,fname2,...] mapping
photo_counts = {}               # name:count mapping

def people_with_at_least(n):
    """Return the number of people who have at least n photos"""
    return sum(1 for ct in photo_counts.values() if ct>=n)

def draw_person(count):
    """Draw a person with at least count photos. Once the person is
    drawn, remove them from the photos database. Raise an error if we
    run out of people"""

    remaining_people = list( photos.keys())
    random.shuffle(remaining_people)
    for name in remaining_people:
        if len(photos[name]) >= count:
            # save return values, but only take 'count' of the photos.
            # Then randomize the photos
            ret = (name, random.choices(photos[name], k=count))
            del photos[name]            # remove from list
            return ret
    raise RuntimeError(f"Could not find a person who has {count} photos remaining. Please change experimental parameters.")

@click.command(context_settings={"show_default": True})
@click.option("--photodir", type=click.Path(exists=True),
              default=DEFAULT_FACE_DATA_DIR,
              help="Location of your people photos")
@click.option("--tcount", default=3, help="Number of randomly chosen people to use for templates")
@click.option("--tphotos", default=1, help="Number of randomly chosen photos to use for each template")
@click.option("--ocount", default=1, help="Number of probe people to use who are not in the template database")
@click.option("--ccount", default=1, help="Number of probe people to use who are in the template database")
@click.option("--pphotos", default=1, help="Number of probes to used for each probe person")
@click.option("--templatedb", type=click.Path(), help="Template DB output filename", default='templatedb.tsv')
@click.option("--probedb", type=click.Path(), help="Probe DB output filename", default='probedb.tsv')
# pylint: disable=too-many-arguments,too-many-positional-arguments,too-many-locals,too-many-branches
def experiment_maker(photodir,tcount,tphotos,ocount,ccount,pphotos,templatedb,probedb):
    """Make the experiment files"""
    click.echo(f"Scanning {photodir}")

    # For each directory in photodir, count the number of photos it has
    for name in os.listdir(photodir):
        pdir = join(photodir,name)
        if os.path.isdir(pdir):
            photos[name] = [ join(pdir,name) for name in os.listdir(pdir) if is_jpeg(name) ]
            if photos[name]:
                photo_counts[name] = len(photos[name])
            else:
                # no photos!
                del photos[name]
                continue

    # Print some statistics about these photos:
    click.echo(f"Number of individuals: {len(photos)}")
    click.echo(f"Minimum number of photos per individual: {min(photo_counts.values())}")
    click.echo(f"Median number of photos per individual: {statistics.median(photo_counts.values())}")
    click.echo(f"Number of individuals with at least 2 photos: {people_with_at_least(2)}")
    click.echo(f"Number of individuals with at least 3 photos: {people_with_at_least(3)}")
    click.echo(f"Maximum number of photos per individual: {max(photo_counts.values())}")
    click.echo("")
    click.echo("Now generating output files...")
    click.echo("")
    # Make sure that we can satisfy the request
    if ccount > tcount:
        raise ValueError(f"More probe photos requested for the closed world assumption "
                         f"probes ({ccount}) than are in the template database ({tcount})")

    if people_with_at_least(tphotos) < tcount:
        raise ValueError(f"There are only {people_with_at_least(tphotos)} people who have {tphotos} but {tcount} were requested")

    if people_with_at_least(min(tphotos,pphotos)) < (tcount+ccount+ocount):
        raise ValueError(f"More photos are requested ({tcount+ccount+ocount}) for the experiment than are present in the dataset")


    # Collections of (name,photos) that we will create
    template_db = {}
    closed_probes = {}
    open_probes = {}

    # Find people who have sufficient photos to be both in the template database and in the closed probe photos
    # Note that the ordering assumes that tphotos > pphotos
    for _ in range(ccount):
        (name, fnames) = draw_person(tphotos+pphotos)
        template_db[name]   = fnames[0:tphotos]
        closed_probes[name] = fnames[tphotos:tphotos+pphotos]

    # Find additional people for the template database
    for _ in range(tcount - ccount):
        (name, fnames) = draw_person(tphotos)
        assert name not in template_db
        template_db[name]   = fnames

    # Find additional people for the open probep hotos
    for _ in range(ocount):
        (name, fnames) = draw_person(pphotos)
        assert name not in template_db
        open_probes[name]   = fnames

    # Now create the template db. Sort to make it attractive and to increase the usability of the output files.
    with open(templatedb,"w",encoding='utf-8') as f:
        f.write("name\tfname\n")
        for (name,fnames) in sorted(template_db.items()):
            for photo in sorted(fnames):
                f.write(f"{name}\t{photo}\n")

    # Now create the probe db
    with open(probedb,"w",encoding='utf-8') as f:
        f.write("name\tfname\tstatus\n")
        for (name,fnames) in sorted(closed_probes.items()):
            for fname in fnames:
                f.write(f"{name}\t{fname}\tpresent\n")
        for (name,fnames) in sorted(open_probes.items()):
            for fname in sorted(fnames):
                f.write(f"{name}\t{fname}\tabsent\n")

    click.echo("Done.")

if __name__ == "__main__":
    experiment_maker()          # pylint: disable=no-value-for-parameter

# Project 1: Prototyping a Face Recognition System

Here is some sample code for Project 1 which you may find useful.

This code assumes you have an AWS account and that you are running at
the MacOS command line. This code should also work on Windows or
Linux, but we haven't tested there.

If you clone this repo, be sure to create your Python virtual environment by typing:

```make venv```

Once you've done that, activate it with:

```source venv/bin/activate```

This directory provides two executables:

* `experiment_maker.py` - creates the `templatedb.tsv` for the template database and the `probedb.tsv` for the probe database.

* `experiment_runner.py` - Runs an experiment with the files created by `experiment_maker.py.` Currently only runs on Amazon Rekognition.

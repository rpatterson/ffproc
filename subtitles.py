from MediaParser import Parser
from util import Log
from task import Task,TaskTypes
"""
    subtitles:
        - keep yes/no - yes will require the external utilities to be installed for some files.
"""

"""
    Returns an array of incomplete Tasks. Infile and outfile must still be populated.
"""

def subs_transform(parser, options):
    subopts = options["subtitles"]
    if subopts["keep"] == False or len(parser.sub_streams) == 0:
        return []

    #Find the "best" subtitle stream. This will *usually* be the one which is in the right language, has has the highest number of frames. We're not checking for FD subtitles yet.
    bestsub={"language":"eng","numframes":0}
    for sub in parser.sub_streams:
        if sub["language"] == "eng" or sub["language"] == "und":
            if sub["numframes"] > bestsub["numframes"]:
                bestsub = sub
    return [Task(tasktype=TaskTypes.SUBTITLE, command=filenameFromType(bestsub["codec"]), arguments=[bestsub["index"]])]

#returns the subtitle script to use in order to extract everything. There's usually a fair number of steps involved for each one, so they are implemented as shell scripts.
def filenameFromType(type):
    if type == "srt":
        return "subs/extractsrt.sh"
    elif type == "pgssub":
        return "subs/tosrt.sh"
    elif type == "ass" or type == "ssa":
        return "subs/ssa-to-srt.sh"
    elif type == "vobsub" or type == "dvdsub":
        return "subs/tosrt_vobsub.sh"

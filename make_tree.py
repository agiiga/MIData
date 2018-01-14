#!/usr/bin/env python
#


import os
import sys
import uuid
import time
from shutil import copyfile

ROOT = "."

SESSION_TYPES = [ "eeg", "miq" ]
DATA_TYPES = [ "loreta", "roi", "raw" ]
EEG_TYPES = [ "control", "feedback" ]
FEEDBACK_TYPES = [ [ "baseline", 4 ], [ "baseline_ec", 2 ], [ "mi_w_fb", 10 ], [ "mi_wo_fb", 8 ], [ "rm", 4 ] ]
CONTROL_TYPES = [ [ "baseline", 4 ], [ "baseline_ec", 2 ], [ "mi_woo_fb", 10 ], [ "mi_wo_fb", 8 ], [ "rm", 4 ] ]

def main(argv):
    arg_len = len(argv)
    if (arg_len == 2):
        subject = argv[0]
        date = argv[1]
        print("Creating folder tree for subject {:s} with trial dates of {:s}").format(subject, date)
        subjectPath = os.path.join(ROOT, subject) 
        sessionFolders = createFolders(subjectPath, SESSION_TYPES)
        for f in sessionFolders:
            if f == os.path.join(subjectPath, SESSION_TYPES[0]):
                dataTypeFolders = createFolders(f, DATA_TYPES)
                for dt in dataTypeFolders:
                    eegTypeFolders = createFolders(dt, EEG_TYPES)
                    controlFolder = os.path.join(dt, EEG_TYPES[0])
                    for ft in eegTypeFolders:
                        dateFolders = createFolders(ft, [ date ])
                        for d in dateFolders:
                            if d.startswith(controlFolder):
                                createTrialFolders(d, FEEDBACK_TYPES)
                            else: 
                                createTrialFolders(d, CONTROL_TYPES)
    else:
        print("Please specify subject NAME and session DATE in DDMMYYYY format") 


def createFolders(root, arr):
    created = []
    for e in arr:
        path = os.path.join(root, e)
        created.append(path)
        createFolder(path)
                
    return created

def createTrialFolders(root, arr):
    created = []
    for e in arr:
        path = os.path.join(root, e[0])
        created.append(path)
        createFolder(path)
        start = 1
        while start <= e[1]:
            p = os.path.join(path, str(start))
            created.append(p)
            createFolder(p)
            start += 1

    return created


def createFolder(path):
    print("{:s}").format(path)
    

if __name__ == "__main__":
    main(sys.argv[1:])



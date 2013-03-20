import os, sys
from collections import Counter

"""
License: WTFPL http://www.wtfpl.net
Copyright: Gabriel Synnaeve 2013
"""

doc = """
Usage:
    python substitute_phones.py [$folder_path] [--sentences]

Substitutes phones found in .lab files (in-place) by using the foldings dict.

The optional --sentences argument will replace starting and ending pauses 
respectively by <s> and </s>.
"""

foldings = {'ux': 'uw', 
            'axr': 'er', 
            'em': 'm',
            'nx': 'n',
            'eng': 'ng',
            'hv': 'hh',
            'pcl': 'sil',
            'tcl': 'sil',
            'kcl': 'sil',
            'qcl': 'sil',
            'bcl': 'sil',
            'dcl': 'sil',
            'gcl': 'sil',
            'h#': 'sil',
            '#h': 'sil',
            'pau': 'sil',
            'el': 'l',
            'en': 'n',
            'sh': 'zh',
            'ao': 'aa',
            'ih': 'ix',
            'ah': 'ax'}

def process(folder, sentences=False):
    c_before = Counter()
    c_after = Counter()
    for d, ds, fs in os.walk(folder):
        for fname in fs:
            if fname[-4:] != '.lab':
                continue
            fullname = d.rstrip('/') + '/' + fname
            phones_before = []
            phones_after = []
            os.rename(fullname, fullname+'~')
            fr = open(fullname+'~', 'r')
            fw = open(fullname, 'w')
            saw_pause = 0
            for line in fr:
                phones_before.append(line.split()[2])
                tmpline = line
                if sentences:
                    if not saw_pause:
                        tmpline = tmpline.replace('h#', '<s>')
                    else:
                        tmpline = tmpline.replace('h#', '</s>')
                tmpline = tmpline.replace('-', '')
                for k, v in foldings.iteritems():
                    tmpline = tmpline.replace(k, v)
                fw.write(tmpline)
                phones_after.append(tmpline.split()[2])
                if 'h#' in line:
                    saw_pause += 1
            if saw_pause > 2:
                print "this file has more than 2 pauses", fname
            fw.close()
            os.remove(fullname+'~')
            c_before.update(phones_before)
            c_after.update(phones_after)
            print "dealt with", fullname 
    print "Counts before substitution", c_before
    print "Counts after substitution", c_after


if __name__ == '__main__':
    if len(sys.argv) > 1:
        if '--help' in sys.argv:
            print doc
            sys.exit(0)
        sentences = False
        if '--sentences' in sys.argv:
            sentences = True
        l = filter(lambda x: not '--' in x[0:2], sys.argv)
        foldername = '.'
        if len(l) > 1:
            foldername = l[1]
        process(foldername, sentences)
    else:
        process('.') # default

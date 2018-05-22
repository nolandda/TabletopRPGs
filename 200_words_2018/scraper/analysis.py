#!/usr/bin/python

import pprint

def load_vids():
    unique_vids = {}
    with open('video_ids.txt') as vidfile:
        vid_set = set(vidfile.read().split())
        for curvid in vid_set:
            unique_vids[curvid] = unique_vids.get(curvid, 0) + 1
    return unique_vids

#def analyse_chars( strmap ):
#    char_map = {}
#    for curstr,curcount in strmap.iteritems():
#        lst = list(curstr)
#        for cc in lst:
#            char_map[cc] = char_map.get(cc, 0) + 1            
#    return char_map

def repeating_ngrams( strmap ):
    counts = [0,0,0,0]
    odds = [0,0,0,0]
    for curstr,curary in strmap.iteritems():
        for i in range(len(curary)):
            if curary[i] > 0:
                counts[i] += 1
    n = len( strmap )
    print( str(counts) )
    for i in range(len(counts)):
        odds[i] = ((counts[i] * 1.0) / (n * 1.0)) * 100.0
    print('--- Case Sensitive ---')
    print('  Doubles = ' + str(counts[0]) + '/' + str(n) + ' = ' + str(odds[0]))
    print('  Tripples = ' + str(counts[1]) + '/' + str(n) + ' = ' + str(odds[1]))
    print('--- Case Insensitive ---')
    print('  Doubles = ' + str(counts[2]) + '/' + str(n) + ' = ' + str(odds[2]))
    print('  Tripples = ' + str(counts[3]) + '/' + str(n) + ' = ' + str(odds[3]))
    print( str(counts) )


def analyse_chars( strmap ):
    char_map = {}
    prev = '~'
    prevprev = '~'
    for curstr,curcount in strmap.iteritems():
        strmap[curstr] = [0,0,0,0]
        lst = list(curstr)
        for cc in lst:
            char_map[cc] = char_map.get(cc, 0) + 1            
            if prev == cc:
                strmap[curstr][0] += 1;
            if prevprev == prev and prev == cc:
                strmap[curstr][1] += 1;
                print('Tripple = ' + curstr)
            if prev.lower() == cc.lower():
                strmap[curstr][2] += 1;
            if prevprev.lower() == prev.lower() and prev.lower() == cc.lower():
                strmap[curstr][3] += 1;            
            prevprev = prev
            prev = cc
    return char_map

if __name__ == '__main__':
    # Do the stuff
    vidmap = load_vids()
    pp = pprint.PrettyPrinter(indent=2)
    charmap = analyse_chars( vidmap )
    #pp.pprint( vidmap )
    print('Num Entries = ' + str(len(vidmap.keys())))
    charmap = analyse_chars( vidmap )
    pp.pprint( charmap )
    print('Num Unique Chars = ' + str(len(charmap.keys())))
    repeating_ngrams( vidmap )

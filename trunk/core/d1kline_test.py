# -*- coding: utf-8 -*-
#所有kline算法的测试

import re
import unittest
from wolfox.fengine.core.d1kline import *

class ModuleTest(unittest.TestCase):
    def testKsign(self):
        topen = np.array([100,201,299,405])
        tclose = np.array([100,200,300,400])
        self.assertEquals('cbab',ksign(topen,tclose))

    def testKsize(self):
        topen = np.array([1000,1000,1000,1000,1000,1000,1000,1000,1000,1000])
        tclose = np.array([1000,1041,1023,1009,1002,998,991,987,959,1036])
        self.assertEquals('dabcddcbaa',ksize(topen,tclose))
        self.assertEquals('dbbcddcbbb',ksize(topen,tclose,tbig=50))
        self.assertEquals('dbccddccbc',ksize(topen,tclose,tmiddle=40,tbig=60))
        self.assertEquals('dbddddddbc',ksize(topen,tclose,tsmall=30,tmiddle=40,tbig=60))

    def testKsized(self):
        topen = np.array([1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000])
        tclose = np.array([1000,1040,1030,1076,1030,1006,932,950,970,994,1024])
        self.assertEquals('uubacdabcdb',ksized(topen,tclose,2))
        self.assertEquals('uubbcdabcdb',ksized(topen,tclose,2,tbig=3000))
        self.assertEquals('uucbcdaccdc',ksized(topen,tclose,2,tmiddle=2000,tbig=3000))
        self.assertEquals('uucbddacddc',ksized(topen,tclose,2,tsmall=1000,tmiddle=2000,tbig=3000))

    def testKscmp(self):
        topen = np.array([1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000])
        tclose = np.array([1000,1010,1010,1010,1010,1010,990,990,990,990,990])
        tf1 = np.array([1000,1000,1000,1000,1000,1000,1000,1000,1000,1000,1000])
        tf2 = np.array([1020,1050,1042,1025,1010,1003,965,985,920,997,1000])
        self.assertEquals('acccccccccc',kscmp(topen,tclose,topen,tclose))
        self.assertEquals('abbbbbbbbbb',kscmp(topen,tclose,topen,tclose,tmiddle=1000,tbig=2500))
        self.assertEquals('aaabcdbcadd',kscmp(topen,tclose,tf1,tf2))
        self.assertEquals('aabbcdbcadd',kscmp(topen,tclose,tf1,tf2,tbig=5000))
        self.assertEquals('aaabcdacadd',kscmp(topen,tclose,tf1,tf2,tbig=3000))
        self.assertEquals('aaabbdabadd',kscmp(topen,tclose,tf1,tf2,tmiddle=1000,tbig=3000))
        self.assertEquals('aaabcdacadd',kscmp(topen,tclose,tf1,tf2,tmiddle=2000,tbig=3000))
        self.assertEquals('aaabccacacd',kscmp(topen,tclose,tf1,tf2,tsmall=200,tmiddle=2000,tbig=3000))

    def testKrelation(self): #顺带测试ksrelation
        topen = np.array([1000,1011,1019,1016,1010,1028,1027,1000,1010,990,988])
        tclose = np.array([1010,1016,1015,1025,1030,1021,1022,1026,1002,1004,960])
        self.assertEquals('uabcdefghij',krelation(topen,tclose))

    def testKmatch(self):
        pat = re.compile('ab')
        self.assertEquals([0,1,0,0,0,1,0],kmatch('abcdabc',pat).tolist())
        self.assertEquals([0,1,0,0,0,1],kmatch('abcdab',pat).tolist())
        pat2 = re.compile('ab|bcd')
        self.assertEquals([0,1,0,0,0,1,0,0,0,1,0],kmatch('abcdabcbcda',pat2).tolist())
        self.assertEquals([0,1,0,0,0,1,0,0,0,1],kmatch('abcdabcbcd',pat2).tolist())

if __name__ == "__main__":
    import logging
    logging.basicConfig(filename="test.log",level=logging.DEBUG,format='%(name)s:%(funcName)s:%(lineno)d:%(asctime)s %(levelname)s %(message)s')
    
    unittest.main()

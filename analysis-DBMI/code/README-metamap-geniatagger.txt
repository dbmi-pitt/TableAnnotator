Extract Concepts by MetaMap 
===========================
(use MetaMap JAVA API)

1. Start MetaMap (details are listed on localhost:80 page)
$ cd /home/rdb20/UMLS/MetaMap/public_mm/
$ ./bin/skrmedpostctl start
$ ./bin/wsdserverctl start
$ cd /home/rdb20/UMLS/MetaMap/public_mm
$ ./bin/mmserver

2. Run java application
GitHub: analysis-DBMI/code/ExtractConceptByMetaMap.java
Input: a text file which list all headings
Output: a csv file which contains "Heading,CUI,Semantic Type,Preferred Name"

Extract tags by GENIA Tagger
===========================

1. Download GENIA Tagger
http://www.nactem.ac.uk/GENIA/tagger/

2. Run python application
GitHub: analysis-DBMI/code/extractTagByGenia.py
Input: a text file which list all headings
Output: a csv file which contains "headings,words,POStags"


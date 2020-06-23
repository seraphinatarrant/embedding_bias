gg = open('tweets2.tsv','w')
i = 0
for fil in ['01_clean.tsv','02_clean.tsv','03_clean.tsv','04_clean.tsv']:
	ff = open(fil,'r').readlines()
	for line in ff[1:]:	
		tweet = line.split('\t')
		if len(tweet)<4:
			continue
		text = tweet[3]
		gg.write(text)
		i = i + 1
		print (i)
	#ff.close()
gg.close()

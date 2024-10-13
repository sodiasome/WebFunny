import os

for root,dirs,files in os.walk("./linux"):
	i = 1
	for file in files:
		name = ""
		for ch in file:
			if not ch.isdigit():
				name += ch
				
		newName = str(i) + "." + name
		os.rename("./linux/"+file,newName)
		i += 1
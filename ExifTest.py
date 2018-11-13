import exifread
import glob


def process(filename):

    f = open(filename, 'rb')
    tags = exifread.process_file(f)
    #f = open('csvfile.csv','w')
    for tag in tags.keys():
    	if 'GPSLatitude' in tag:
    		print "%s, %s" % (tag, tags[tag])
    		f.write("%s, %s" % (tag, tags[tag]))
    	if 'GPSLongitude' in tag:
    		print "%s, %s" % (tag, tags[tag])
    		f.write("%s, %s" % (tag, tags[tag]))
   	

for (i,image_file) in enumerate(glob.iglob('gphoto/*.jpg')):
        process(image_file)

        
f.close()
 #Give your csv text here.
## Python will convert \n to os.linesep


# Open image file for reading (binary mode)
#path_name = "gphoto\ss.jpg"
#f = open(path_name, 'rb')

# Return Exif tags
#tags = exifread.process_file(f)

#for tag in tags.keys():
#	if 'GPSLatitude' in tag:
#		print "%s, %s" % (tag, tags[tag])


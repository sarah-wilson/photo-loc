import glob
import os

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
#import whatimage
#import pyheif

from sarahphotos.functions import count_my_photos

# def decodeImage(bytesIo):
#     fmt = whatimage.identify_image(bytesIo)
#     if fmt in ['heic', 'avif']:
#         i = pyheif.read_heif(bytesIo)
#
#         # Convert to other file format like jpeg
#         s = os.io.BytesIO()
#         pi = Image.frombytes(
#             mode=i.mode, size=i.size, data=i.data)
#
#         pi.save(s, format="jpeg")

def get_exif_data(image):
    """Returns a dictionary from the exif data of an PIL Image item. Also converts the GPS Tags"""
    exif_data = {}
    info = image._getexif()
    if info:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]

                exif_data[decoded] = gps_data
            else:
                exif_data[decoded] = value

    return exif_data


def _get_if_exist(data, key):
    if key in data:
        return data[key]

    return None


def _convert_to_degress(value):
    """Helper function to convert the GPS coordinates stored in the EXIF to degress in float format"""
    d0 = value[0][0]
    d1 = value[0][1]
    d = float(d0) / float(d1)

    m0 = value[1][0]
    m1 = value[1][1]
    m = float(m0) / float(m1)

    s0 = value[2][0]
    s1 = value[2][1]
    s = float(s0) / float(s1)

    return d + (m / 60.0) + (s / 3600.0)


def get_lat_lon(exif_data: object) -> object:
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    lat = None
    lon = None

    if "GPSInfo" in exif_data:
        gps_info = exif_data["GPSInfo"]

        gps_latitude = _get_if_exist(gps_info, "GPSLatitude")
        gps_latitude_ref = _get_if_exist(gps_info, 'GPSLatitudeRef')
        gps_longitude = _get_if_exist(gps_info, 'GPSLongitude')
        gps_longitude_ref = _get_if_exist(gps_info, 'GPSLongitudeRef')

        if gps_latitude and gps_latitude_ref and gps_longitude and gps_longitude_ref:
            lat = _convert_to_degress(gps_latitude)
            if gps_latitude_ref != "N":
                lat = 0 - lat

            lon = _convert_to_degress(gps_longitude)
            if gps_longitude_ref != "E":
                lon = 0 - lon

    return lat, lon

def get_datetime(exif_data: object) -> object:
    """Returns the latitude and longitude, if available, from the provided exif_data (obtained through get_exif_data above)"""
    datetime = None
    time_info = None

    if "DateTime" in exif_data:
        time_info = exif_data["DateTime"]

        datetime = _get_if_exist(time_info, "DateTime")

    return time_info


################
# Example ######
################
if __name__ == "__main__":
    myfile = open('update24.txt', 'w')
    for infile in glob.glob("update24/*"):

        im = Image.open(infile)
        exif_data = get_exif_data(im)
        results = get_lat_lon(exif_data)
        DT = get_datetime(exif_data)
        print(results, " DateTime: ", DT, " FileName: ", im.filename)
        myfile.write(str(results) + " DateTime: " + str(DT) + " FileName: " + im.filename + "\n")
    myfile.close()
    # text_file.close()

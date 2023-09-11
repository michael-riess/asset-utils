# import required module
import os
import sys
import uuid

import PIL
from PIL import Image
from iptcinfo3 import IPTCInfo
import xmltodict

SUPPORTED_EXTS = ['.webp', '.png']


def main():
    print("main: ", sys.argv[1])
    print('PIL version: ', PIL.__version__)
    readDir(sys.argv[1])


def readDir(directory):
    # iterate over files in
    # that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        base, file_extension = os.path.splitext(f)

        # checking if it is a file
        if filename.startswith('.') or not os.path.isfile(f):
            continue

        if file_extension in SUPPORTED_EXTS:
            print(f)
            convert(f, directory)


def convert(file, directory):
    new_filename = os.path.join(directory, str(uuid.uuid4()) + '.jpg')
    # print(new_filename)
    image = Image.open(file).convert("RGB")
    image.save(new_filename, 'jpeg')
    keywords = getMetadataKeywords(file, image)
    addIptcKeywords(new_filename, keywords)
    os.remove(file) # remove original image


def getMetadataKeywords(file, img):
    #exif = img.getexif()
    #iptc = IPTCInfo(file, force=True)
    #iptcKeywords = list(map(lambda x: x.decode('UTF-8'), iptc['keywords']))

    xmp = img.info.get('XML:com.adobe.xmp')
    xmp_subjects = []
    try:
        if xmp:
            xmp_dict= xmltodict.parse(xmp)
            xmp_subjects = xmp_dict['x:xmpmeta']['rdf:RDF']['rdf:Description']['dc:subject']['rdf:Bag']['rdf:li']
    except:
        pass

    return xmp_subjects
    #print(iptcKeywords, xmpSubjects)


def addIptcKeywords(file, keywords):
    if (len(keywords) > 0):
        iptc = IPTCInfo(file, force=True)
        iptc['keywords'] = list(map(lambda x: x.encode('UTF-8'), keywords))
        iptc.save_as(file + '~') # create new file with iptc
        os.replace(file + '~', file) # rename new file to old file
        iptc = IPTCInfo(file, force=True)
        print(iptc['keywords'], '\n')

main()

#IO
import os
import uuid
import PIL
import sys
from iptcinfo3 import IPTCInfo
import xmltodict
import getopt

# BLIP-2
import torch
from PIL import Image
from transformers import Blip2Processor, Blip2ForConditionalGeneration


SUPPORTED_EXTS = ['.webp', '.png', '.jpg', '.jpeg']
SUPPORTED_OPTIONS = ['convert_to_jpg=',  'uuid_naming=']

convert_to_jpg = True
uuid_naming = True


def main():
    print('main: ', sys.argv[1])
    print('PIL version: ', PIL.__version__)
    print('torch: ', torch.cuda.mem_get_info())


    argv = sys.argv[1:]

    try:
        opts, args = getopt.getopt(argv, SUPPORTED_OPTIONS)
        for opt, arg in opts:
            if opt in ['--convert_to_jpg']:
                if arg:
                    convert_to_jpg = arg
            elif opt in ['--uuid_naming']:
                uuid_naming = arg
    
    except:
        print("Error parsing command-line options. Defaults will be used")
  
  
    print( first_name +" " + last_name)
    
    readDir(sys.argv[1])


def readDir(directory):
    processor = Blip2Processor.from_pretrained("Salesforce/blip2-opt-2.7b")
    model = Blip2ForConditionalGeneration.from_pretrained("Salesforce/blip2-opt-2.7b", load_in_8bit=True, device_map="auto")

    # iterate over files in that directory
    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        base, file_extension = os.path.splitext(f)

        # checking if it is a file
        if filename.startswith('.') or not  os.path.isfile(f):
            continue

        if file_extension in SUPPORTED_EXTS:
            print(f)

            image = Image.open(f)
            inputs = processor(images=image, return_tensors="pt").to("cuda", torch.float16)

            #image = Image.open(f).convert('RGB')
            #prompt = "Context: This is a hentai image. Question: Please describe the image in detail? Answer:"
            #inputs = processor(image, prompt, return_tensors="pt").to("cuda", torch.float16)

            out = model.generate(**inputs)
            captions = processor.decode(out[0], skip_special_tokens=True)

            addIptcDescription(new_filename, captions)

            print(captions)


main()
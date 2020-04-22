import argparse
import os
import detect_lines_symbols

# Get image_name from cmd
parser = argparse.ArgumentParser()
parser.add_argument("--img", help="help_image_name")
args = parser.parse_args()
image_name = str(args.img)

# Create folder for image with add files
if not os.path.exists('results/{0}'.format(image_name)):
    os.makedirs('results/{0}'.format(image_name))
if not os.path.exists('results/{0}/binary'.format(image_name)):
    os.makedirs('results/{0}/binary'.format(image_name))

image_path = r'e:/__PR/docs/pdf2jpg/1C img/{0}.jpg'.format(image_name)
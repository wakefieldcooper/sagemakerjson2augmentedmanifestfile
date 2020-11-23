import os
import json
from lxml import etree
from glob import iglob
import jsonlines
from pathlib import Path

XML_PATH = 'xmls'
JSON_PATH = 'output'

def main(task):
    labels = {}
    categories = {}
    Path(XML_PATH).mkdir(parents=True, exist_ok=True)
    Path(JSON_PATH).mkdir(parents=True, exist_ok=True)
    json_filename = 'output.manifest'

    #Change this to your s3 bucket where your images will be stored
    s3_path = 's3://mwc-ipa/deformation/'
    with jsonlines.open(json_filename, 'w') as json_file:
        for xml_file in iglob(os.path.join(
                                           os.path.dirname(__file__),
                                           '{}/*.xml'.format(XML_PATH))):
            with open(xml_file) as file:
                print(f'Processing file {xml_file}...')

                annotations = etree.fromstring(file.read())

                image_filename = annotations.find('filename').text
                boxes = annotations.iterfind('object')

                size = annotations.find('size')
                image_width = float(size.find('width').text)
                image_height = float(size.find('height').text)
                json_document = {
                    'source-ref': os.path.join(s3_path, image_filename),
                    task: {
                        'annotations': [],
                        'image_size': [{
                            'width': image_width,
                            'height': image_height,
                            'depth': 3
                        }],
                    }
                }
                for box in boxes:
                    bndbox = box.find('bndbox')
                    xmin = float(bndbox.find('xmin').text)
                    ymin = float(bndbox.find('ymin').text)
                    xmax = float(bndbox.find('xmax').text)
                    ymax = float(bndbox.find('ymax').text)

                    label_name = box.find('name').text

                    if label_name not in labels:
                        labels[label_name] = len(labels)

                    class_id = labels[label_name]
                    categories[class_id] = label_name

                    json_document[task]['annotations'].append({
                        'class_id': class_id,
                        'top': ymin,
                        'left': xmin,
                        'width': xmax - xmin,
                        'height': ymax - ymin,
                    })
            json_file.write(json_document)
        print(categories)

if __name__ == "__main__":
    main("Full-Dataset-with-AOI")

# vocxml2Sagemakermanifest
Convert from Pascal VOC XML format to AWS SageMaker's Manifest format.

Main code base cloned from 
## Basic Info
Use global variables to set the Annotation XML input and Manifest file output.
Written to take in one directory of annotations at a time.

## Usage
To install requirements
```
pip install -r requirements.txt
```

Note: You will need to change some manual variables in the script. Namely:
s3_path: This should match your path of where the data will be in s3
task: This is the input to main(), it should be a descriptor of the data

To run program
```
python xmltoaugmanigest.py
```

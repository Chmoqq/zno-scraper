from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfpage import PDFTextExtractionNotAllowed
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams
from pdfminer.converter import PDFPageAggregator
import pdfminer
import re
import sys

sys.path.insert(1, "/Users/home/ivandaniyelyan/pdfminer")

# Open a PDF file.
fp = open('/Users/ivandaniyelyan/PycharmProjects/zno-scraper/Ukr-mova_lit-ZNO_2018-Klyuchi.pdf', 'rb')

# Create a PDF parser object associated with the file object.
parser = PDFParser(fp)

# Create a PDF document object that stores the document structure.
# Password for initialization as 2nd parameter
document = PDFDocument(parser)

# Check if the document allows text extraction. If not, abort.
if not document.is_extractable:
    raise PDFTextExtractionNotAllowed

# Create a PDF resource manager object that stores shared resources.
rsrcmgr = PDFResourceManager()

# Create a PDF device object.
device = PDFDevice(rsrcmgr)

# BEGIN LAYOUT ANALYSIS
# Set parameters for analysis.
laparams = LAParams()

# Create a PDF page aggregator object.
device = PDFPageAggregator(rsrcmgr, laparams=laparams)

# Create a PDF interpreter object.
interpreter = PDFPageInterpreter(rsrcmgr, device)


def get_variant_id(bbox):
    min_x, max_x = bbox[0], bbox[2]

    for x in range(3):
        max_c_x = 120 + 140 * x
        min_c_x = max_c_x - 140 * x

        if min_x >= min_c_x and max_x <= max_c_x < 390:
            return x + 1

    return None


def parse_obj(f, lt_objs):
    # loop over the object list

    for obj in lt_objs:

        # if it's a textbox, print text and location
        if isinstance(obj, pdfminer.layout.LTTextBoxHorizontal):
            variant = get_variant_id(obj.bbox)
            if variant is None:
                continue

            print(variant)
            if ("А" or "Б" or "В" or "Г" or "Д") in obj.get_text():
                f.write(obj.get_text() + "\n=======\n")
                # print(obj.get_text())
            elif ("1-" + "А" or "Б" or "В" or "Г" or "Д") in obj.get_text():
                f.write(obj.get_text() + "\n=======\n")

        # if it's a container, recurse
        elif isinstance(obj, pdfminer.layout.LTFigure):
            parse_obj(f, obj._objs)


# loop over all pages in the document
with open("answers.txt", "w") as old_file:
    old_file.write("")

with open("answers.txt", "a+") as old_file:
    for page in PDFPage.create_pages(document):
        # read the page into a layout object
        interpreter.process_page(page)
        layout = device.get_result()

        # extract text from this object
        parse_obj(old_file, layout._objs)

with open("new_answers.txt", "a+") as new_file:
    with open("answers.txt", "r+") as old_file:
        for line in old_file:
            meme = re.sub(r'1-A', '1', line)
            new_file.write(meme)
        for x in new_file:
            if x == "А \n":
                old_file.write("1\n")
                print("1")
            elif x == "Б \n":
                old_file.write("2\n")
                print("2")
            elif x == "В \n":
                old_file.write("3\n")
                print("3")
            elif x == "Г \n":
                old_file.write("4\n")
                print("4")
            elif x == "Д \n":
                old_file.write("5\n")
                print("5")
new_file.close()

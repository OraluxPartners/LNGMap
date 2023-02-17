from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO
import pandas as pd
from geopy.geocoders import Nominatim




def extract_text_from_pdf(pdf_path):
    resource_manager = PDFResourceManager()
    fake_file_handle = StringIO()
    converter = TextConverter(
        resource_manager, fake_file_handle, codec='utf-8', laparams=LAParams())
    page_interpreter = PDFPageInterpreter(resource_manager, converter)

    with open(pdf_path, 'rb') as fh:
        for page in PDFPage.get_pages(fh,
                                      caching=True,
                                      check_extractable=True):
            page_interpreter.process_page(page)

        text = fake_file_handle.getvalue()

    # close open handles
    converter.close()
    fake_file_handle.close()

    if text:
        return text


pdf_text = extract_text_from_pdf("lng_terminals.pdf")
pdf_text = pdf_text.splitlines()

dataset = []

pdf_text = [i for i in pdf_text if (len(i) > 2)]

status = pdf_text[1]

for i, line in enumerate(pdf_text[4:]):
    if line.startswith("1.") or line.startswith("A.") or line.startswith("MC.") or line.startswith("M1."):
        if i == 0:        
            pass
        else:
            status = pdf_text[i + 4-1]
        dataset.append([line.split(". ")[1], status])
        
    elif len(line.split(".")[0]) <= 2 and line.split(".")[0] != "U":
        if line.split(".")[0] == "7":
            dataset.append([line.split(". ")[1] +" " + pdf_text[i+5], status])
        else:
            dataset.append([line.split(". ")[1], status])

df = pd.DataFrame(dataset, columns=["lng_terminal", "status"])

def get_address(name):
    return name.split(": ")[0]
def get_info(name):
    return name.split(": ")[1]

def get_lat_lng(address):
    geolocator = Nominatim(user_agent="geoapiExercises")
    location = geolocator.geocode(address)
    return location.latitude, location.longitude

def get_capacity(name):
    return name.split("(")[0], name.split("(")[1].strip()[:-1]



df["info"] = df["lng_terminal"].apply(get_info)
df["lng_terminal"] = df["lng_terminal"].apply(get_address)
df["lat"], df["lng"] = zip(*df["lng_terminal"].apply(get_lat_lng))

df["capacity"],df["owner"] = zip(*df["info"].apply(get_capacity))


print(df)

# df.to_csv("lng_terminals.csv", index=False)









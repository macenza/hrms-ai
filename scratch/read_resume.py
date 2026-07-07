import fitz

def read():
    doc = fitz.open("e:/Akshita/work/hrms-back/uploads/resumes/1783320630825-877409904.pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    print("RESUME TEXT:")
    print(text)

read()

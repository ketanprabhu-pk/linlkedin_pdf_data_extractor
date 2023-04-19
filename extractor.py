from pdfstructure.hierarchy.parser import HierarchyParser
from pdfstructure.source import FileSource
from pdfstructure.printer import JsonFilePrinter
import json
from pdfstructure.model.document import TextElement, Section, StructuredPdfDocument, DanglingTextSection
from typing import List
import pandas as pd
from py_dto import DTO
import re


class Summary(DTO):
    description = []


class Contact(DTO):
    mobile: str
    email: str
    link: str
    description: str


class Experience(DTO):
    id: int
    companyName: str
    position: str
    date: str
    description = {}


class Education(DTO):
    course: str
    university: str
    date: str
    description = []


class User(DTO):
    name: str
    contact: Contact
    title: str
    location: str
    summary: str
    skills = []
    experience: list[Experience]
    education: list[Education]

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=False, indent=4)


# Dict = {}
Data = []


def pdf_to_json():
    parser = HierarchyParser()
    source = FileSource("./examples/profile.pdf")
    document = parser.parse_pdf(source)

    a = document.elements
    print(a[0])
    print(a[0].children[1])

    traverse(document.elements, document.elements[0].level)
    # for d in Data:
    #     print(d)
    df = pd.DataFrame(Data)
    dtoData = createData(df)
    print("The variable, name : ", dtoData.name)
    print("The variable, mobile : ", dtoData.contact.mobile)
    print("The variable, email : ", dtoData.contact.email)
    print("The variable, location : ", dtoData.location)
    print("The variable, title : ", dtoData.title)
    print("The variable, summary : ", dtoData.summary)


def traverse(elements: List[Section], level, parent=None):
    # print(len(elements))
    for e in elements:
        if (e.heading.text == "Summary" or e.heading.text == "Contact" or
           e.heading.text == "Top Skills" or e.heading.text == "Experience" or e.heading.text == "Education"):
            parent = e.heading.text
        Data.append({"level": level+1, "text": e.heading.text, "type": parent,
                    "mean_size": e.heading.style.mean_size, "max_size": e.heading.style.max_size})
        # print("Level: ", level, element)
        traverse(e.children, e.level, parent)


def createData(data):
    user = User
    summary = Summary
    contact = Contact
    experience = Experience
    education = Education
    i = 0
    for index, row in data.iterrows():
        if (row['level'] == 1 and row["mean_size"] == 26.0 and row["max_size"] == 26.0):
            user.name = row["text"]
        elif (row['level'] == 1 and row["mean_size"] == 12.0 and row["max_size"] == 12.0):
            user.title = ' '.join(map(str, row["text"].split('\n')[0:-1]))
            user.location = row['text'].split('\n')[-1]
        elif (row['level'] == 2 and row["mean_size"] == 12.0 and row["max_size"] == 12.0 and row["type"] == "Summary"):
            summary.description.append(row["text"])
        elif (row['level'] == 3 and row["mean_size"] == 10.5 and row["max_size"] == 10.5 and row["type"] == "Contact"):
            contact.description = row["text"]
        elif (row['level'] == 3 and row["mean_size"] == 10.5 and row["max_size"] == 10.5 and row["type"] == "Top Skills"):
            user.skills.append(row["text"])
        # elif (row['level'] == 2 and row["type"] == "Experience"):
        #     if (row["max_size"] == 12.0):
        #         # if(experience.companyName is not None):
        #         #     user.experience.append(experience)
        #         experience=Experience
        #         # experience.id = i
        #         print(row['text'],"\n")
        #         experience.companyName = row['text'].split('\n')[0]
        #         experience.position = row['text'].split('\n')[1]
        #         experience.date = row['text'].split('\n')[2]
        #         i = i + 1
        #     elif (row["mean_size"] == 10.5 and row["max_size"] == 10.5):
        #         experience.description.append(row["text"])
        # elif (row['level'] == 2 and row["mean_size"] == 12.0 and row["max_size"] == 12.0 and row["type"] == "Education"):
        #     education.description.append(row["text"])

    user.summary = ' '.join(map(str, summary.description))

    mobile_pattern = r'\+(\d{1,2})?\s*\d{9,10}\s*\((Mobile)\)'
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(mobile_pattern, contact.description)
    if match:
        contact.mobile = match.group(0)
        contact.email = re.search(
            email_pattern, contact.description[match.end():]).group(0)
    else:
        contact.email = re.search(email_pattern, contact.description).group(0)
    user.contact = contact
    
    return user


if __name__ == "__main__":
    pdf_to_json()

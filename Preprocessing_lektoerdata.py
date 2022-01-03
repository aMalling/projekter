import pandas as pd
import numpy as np
import os, sys, re, itertools

alledata = ["10", "11", "12", "13", "14", "15", "16", "17", "18", "19"]
path = r"C:\Users\xxxxxxxx" # insert path

# Creating a class as the main data structure
class publication:
    def __init__(self, topics, publicationYear, author, price, body, titel, dk5, indhold, read_easy):
        self.topics = topics
        self.publicationYear = publicationYear
        self.author = author
        self.price = price
        self.body = body
        self.titel = titel
        self.dk5 = dk5
        self.indhold = indhold
        self.read_easy = read_easy

    def to_dict(self):
        return {
            'Emner': self.topics,
            'Udgivelses År': self.publicationYear,
            'Forfatter': self.author,
            'Pris': self.price,
            'Brødtekst': self.body,
            'titel': self.titel,
            'Dk5':self.dk5,
            'Indhold': self.indhold,
            'Let_læs': self.read_easy
        }

########################################## Functions #########################################################

# Function to divide a list of items starting with a word and seperating them on a delimeter **** odd to write prettier
def divideOn(publication, word, delimeter):
    regex = word + ".*:((?:[\s\S]{0,100}" + delimeter + ")+.+[^A-Z]{0,30}\n)"
    match = re.search(regex, publication)
    if match is not None:
        content = match.group(1)
    else:
        content = None
    content2=re.split('\d. oplag', str(content), flags=re.IGNORECASE)
    content3=re.split('indhold:', content2[0], flags=re.IGNORECASE)
    
    content3=re.split('Oversat fra', content3[0], flags=re.IGNORECASE)
    content3 = content3[0].replace("\n","")

    content3 = re.sub((';{2,}'), "****",(content3))

    content4 = content3.replace("'", "")
    content4 = content4.replace(" ; ", ";")

    content4 = content4.strip(";[] ")

    content5 = content4.split(";")
    content6 =[]
    for a in content5:
        content6.append(a.strip(" "))
      
    content7 = str(content6).strip("[] ")
  
    return str(content7)

def getindhold(publication):
    regex= 'Indhold.*:((?:[\s\S]{0,100};)+.+)'
    match = re.search(regex,publication)
    if match is not None:
        content = match.group()
    else:
        content = None

    return str(content)

# Function to extract DK5 from the data
def getdk5(publication):
    regex ='DK5:\s*(.*)'
    match = re.search(regex,publication)
    if match is not None:
        content = match.group(1)
    else:
        content = None
    return str(content)

def getbody(publication):
    regex= '(Katalogkoder: L.+([\s\S]*))'
    match = re.search(regex, publication)
    if match is not None:
        content = match.group(2)
    else:
        content = None
    return str(content)

#Extract list of publications from text file
def getPublications(rawData):
    publications = rawData.read().split('')
    #deleting empty last datapoint
    del publications[-1]

    return publications

#Format data
def formatdata(publications):
    return pd.DataFrame.from_records([p.to_dict() for p in publications])


def sanitering(inputte, toRemove):
    output = inputte.replace(toRemove,'')
    return output
    
def removeItemInList(inputte, toRemove):
    for item in inputte:
            if (item==toRemove):
                inputte.remove(toRemove)
    return inputte

def replaceChar(inputte):
    for item in inputte:
        inputte=inputte.replace("Ã¦","æ")
        inputte=inputte.replace("Ã¸","ø")
        inputte=inputte.replace("Ã¥", "å")
    return inputte

def let_check(inputte, toCheck):
    for item in toCheck:
        if item in inputte:
             return 1

########################################## functions that arent done #########################################################
def getauther(publication):
    regex = '(.+)'
    match = re.search(regex, publication)
    if match is not None:
        content = match.group()
    else:
        content = None

    return str(content)

# Function to extract price from data #only works for 2010 and abit of 2011
def getprice(publication):
    regex = r'Pris:\D* (\d*\S\d*)'
    match = re.search(regex, publication)
    if match is not None:
        content = match.group(1)
    else:
        content = None

    return str(content)

def gettitel(inputte):
    output=inputte.split("(BOG)")
    return output[0]


def extract_data():

    allPublications = []


    # Getting list of letlæs - quick and dirty
    fileLocation_let = os.path.join(path, "./data/liste_let.xlsx")
    df_let = pd.read_excel(fileLocation_let)
    df_let.dropna(subset = ["Letlæs"], inplace=True)
    easy_read=list(df_let["0"])

    for i in alledata:
        # Open file
        fileLocation = os.path.join(path, "./data/20"+i+".FuldeData.LS.txt")
        with open(fileLocation, encoding='latin-1') as data:

            # get publications
            listOfPublictaions = getPublications(data)

            # iterate all publications 
            for p in listOfPublictaions:

                # getting price of udgivelse - alot of misssing
                price = getprice(p) 
                
                # Getting Auther name (doesnt work)
                auther = getauther(p)
                
                # Getting Brødtekst + replacing æ ø å
                body =getbody(p)
                body =replaceChar(body)

                # Getting emner + sanitizing data + replacing æ ø å
                Emner_raw = divideOn(p, "Emne", ";")
                emner =sanitering(Emner_raw,' ')
                emner =replaceChar(emner)

                #Getting titles +sanitizing data (doesnt work)
                titel=gettitel(p)
                titel =sanitering(titel,'\n')
                
                #Getting Dk5 numbers  
                dk5 = getdk5(p)
                
                # getting indhold that are a longer version of emner - with free text + sanitizing data + replacing æ ø å
                indhold =divideOn(p, "Indhold", ";")
                indhold =sanitering(indhold,' ')
                indhold =replaceChar(indhold)
                
                # Creating a dummy for easy to read from at list of emner that means easy to read
                read_easy= let_check(emner,easy_read)

                # gathering the data in a class + appending
                pub = publication(emner, "20" + i, auther , price, body, titel, dk5, indhold, read_easy)
                allPublications.append(pub)
            
        print("Done with 20" + i)

    df=formatdata(allPublications)

    # Export to excel
    df.to_excel(os.path.join(path, "output\output1.xlsx"), index = False)

    return df



########################################## Main program #########################################################

if __name__ == "__main__":
    df = extract_data()


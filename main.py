import json

#open file

def readJson(number):

    with open('riotAPI_Jsons/set'+number+'-en_us.json', 'r', encoding='utf-8') as json_file_set1:
        json_data_set1=json_file_set1.read()
    # parse file
    return json.loads(json_data_set1)

def printCard(Card):

    if Card != None:
        print(Card.name)
        print(Card.description)
        print(Card.set)
        print(Card.absolutePath)
    else:
        print("Card was not found")

def searchCard(keyword):
    list = []
    isChampion = False
    for k in range(1,6):

        for i in readJson(str(k)):
            if lowerInput(i['name']) == lowerInput(keyword) and i['supertype'] == "Champion":
                isChampion = True;
                list.append(Card(i['name'], i['descriptionRaw'], i['set'], i['assets'][0]["gameAbsolutePath"], ["cardCode"]))

            elif lowerInput(i['name']) == lowerInput(keyword):
                    isChampion = False;
                    list.append(Card(i['name'], i['descriptionRaw'], i['set'], i['assets'][0]["gameAbsolutePath"], ["cardCode"]))
    return list


def checkIfEmpty():
    for i in readJson("1"):
        if i['descriptionRaw'] != "" and i['name'] == "Lux":
            printCard(i)
            break

def lowerInput(input):
    return input.lower()


class Card:
  def __init__(self, name, description, set, absolutePath, cardCode):
    self.name = name
    self.description = description
    self.set = set
    self.absolutePath = absolutePath
    self.cardCode = cardCode


cardList = searchCard("The Howling Abyss")

if len(cardList) == 2:
    print("2 champions")

if len(cardList) == 1:
    print("1 card")
    print(cardList[0].name)

if len(cardList) == 0:
    print("No card found")

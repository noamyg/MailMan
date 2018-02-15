from bs4 import BeautifulSoup
import os

def readTemplate(filename):
    with open(filename, 'r', encoding="utf-8") as templateFile:
        templateFileContent = templateFile.read()
        soup = BeautifulSoup(templateFileContent, 'html.parser')
        templateSubject= ''
        templateSender = ''
        if soup.subject:
            templateSubject = soup.subject.string
            templateFileContent = templateFileContent.replace(templateSubject, '')
        if soup.sender:
            templateSender = soup.sender.string
            templateFileContent = templateFileContent.replace(templateSender , '')
        return templateSubject, templateSender, templateFileContent


def replaceTextWithParams(text, params):
    text = text.format(**params)
    return text

def getAllTemplates(relativePath):
    templateArr = []
    for dirname, dirnames, filenames in os.walk(relativePath):
        for filename in filenames:
            templateArr.append(filename);
    return templateArr
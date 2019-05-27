from bs4 import BeautifulSoup
from html import escape
from flask import render_template_string
import os
import logging

logger = logging.getLogger('mailman_logger')

def readTemplate(filename):
    with open(filename, 'r', encoding="utf-8") as templateFile:
        templateFileContent = templateFile.read()
        soup = BeautifulSoup(templateFileContent, 'html.parser')
        templateSubject= ''
        templateSender = ''
        templateSenderName = ''
        if soup.subject:
            templateSubject = soup.subject.string
            templateFileContent = templateFileContent.replace(escape(templateSubject), '')
        if soup.sender:
            templateSender = soup.sender.string
            templateFileContent = templateFileContent.replace(escape(templateSender), '')
        if soup.sendername:
            templateSenderName = soup.sendername.string
            templateFileContent = templateFileContent.replace(escape(templateSenderName), '')
        return templateSubject, templateSender, templateSenderName, templateFileContent


def replaceTextWithParams(text, params):
    text = render_template_string(text, **params)
    return text


def getAllTemplates(relativePath):
    templateArr = []
    for dirname, dirnames, filenames in os.walk(relativePath):
        for filename in filenames:
            templateArr.append(filename);
    return templateArr
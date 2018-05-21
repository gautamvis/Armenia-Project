# -*- coding: utf-8 -*-
from newspaper import Article
import readability
import requests
import lassie
import articleDateExtractor
from goose3 import Goose
import html2text
import urllib.request
from bs4 import BeautifulSoup
import time


############# Newspaper3k ############
def article_retreive(url):
    article = Article(url)
    try:
        article.download()
        article.parse()
        return article
    except:
        return None


def newspaper_content(url):
    article = article_retreive(url)
    if article is None:
        return ""
    text = article.text
    words = text.split(" ")
    #Debug(words)
    content = " ".join(words)
    return content


def newspaper_date(url):
    article = article_retreive(url)
    Debug(article.publish_date)


############# readability_xml ############
def readability_content(url):
    doc = readability_get_article(url)
    content = doc.summary()
    return content

def readability_get_article(url):
    response = requests.get(url)
    doc = Document(response.text)
    return doc


############# lassie ############
def lassie_content(url):
    content = lassie.fetch(url)
    try:
        if content is None or content["description"] is None:
            return ""
        return content["description"]
    except:
        return ""


############# articleDateExtractor #############
def date_extractor(url):
    d = articleDateExtractor.extractArticlePublishedDate(url)
    Debug(d)


############# Goose Extractor #############
def goose_content(url):
    g = Goose()
    try:
        article = g.extract(url)
        g.close()
        return article.cleaned_text
    except:
        return ""


############# html2text Extractor ############# 
def html2text_content(url):
    
    try:
        text_maker = html2text.HTML2Text()
        text_maker.ignore_links = True
        text_maker.bypass_tables = False
        fp = urllib.request.urlopen(url)
        mybytes = fp.read()
        #text = fp.read()
        html = mybytes.decode("utf8")
        text = text_maker.handle(html)    
        fp.close()
        return text
    except: 
        return ""


############# Testing Utilities #############
def read_file(filename):
    with open(filename) as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


def string_present(data, file_answer):
    #Debug(data, answer)
    if file_answer in data:
        return True
    else:
        return False


def content_test(data, file_answer):
    """Extract content from function"""
    #data = func(url)
    return string_present(data, file_answer)

def verify_both_lines(data, answers, answer_index):
    if content_test(data, answers[answer_index]) and content_test(data, answers[answer_index + 1]):
        return True
    else:
        return False


def date_test(func, url, date, field=None):
    return


def test_driver(func, urls, answers, answer_index, type_test):
    num_correct = 0
    for url in urls:
        Debug("Testing URL: " + url)
        if type_test == content_test:
            data = func(url)
            if verify_both_lines(data, answers, answer_index):
                Debug("Passed")
                num_correct += 1
            else:
                Debug("Failed: String not in content")
            answer_index += 2
        Debug('###')
    return num_correct


def _initialize_recorder(recorder, func):
    recorder[(str(func))] = {}
    
def _set_record(accuracy, time, recorder, func):
    recorder[str(func)]["accuracy"] = accuracy
    recorder[str(func)]["time"] = time

def function_runner(functions, type_test, data_file, url_file, recorder):
    urls = read_file(url_file)
    answers = read_file(data_file)
    num_tests = len(answers) / 2
    answer_index = 0

    for func in functions:
        _initialize_recorder(recorder, func)
        Debug("Beginning " + str(func) + " tests.")
        start = time.time();
        num_correct = test_driver(func, urls, answers, answer_index, type_test)
        end = time.time()
        accuracy = float(num_correct / num_tests)
        time_interval = end - start
        _set_record(accuracy, time_interval, recorder, func)
        Debug("Finished in "+ str(time_interval) + " seconds and with " + str(accuracy) + "% accuracy.")
        Debug("\n")


def set_content_funcs():
    content_funcs = [
                        newspaper_content, 
                        readability_content,
                        lassie_content, 
                        goose_content,
                        html2text_content
                    ]
    return content_funcs


def set_date_funcs():
    date_funcs = [
                    newspaper_date,
                    date_extractor
                ]
    return date_funcs


def Debug(data):
    if debug:
        print(data)
    return


def analyze_records(recorder, url_file):
    print("Results from " + url_file)
    for func_name in recorder:
        print(func_name + " Results")
        for attr in recorder[func_name]:
            print(attr + ": " + str(recorder[func_name][attr]))
        print("\n")


debug = 1


def main():
    recorder = {}
    content_funcs = set_content_funcs()
    print("English TESTS:")
    data_file = "testing/data-en.txt"
    url_file= "testing/urls-en.txt"
    function_runner(content_funcs, content_test, data_file, url_file, recorder)
    analyze_records(recorder, url_file)

    print("Russian TESTS:")

    recorder = {}
    data_file = "testing/data-ru.txt"
    url_file= "testing/urls-ru.txt"
    function_runner(content_funcs, content_test, data_file, url_file, recorder)
    analyze_records(recorder, url_file)

    print("Armenian TESTS:")

    recorder = {}
    data_file = "testing/data-hg.txt"
    url_file= "testing/urls-hg.txt"
    function_runner(content_funcs, content_test, data_file, url_file, recorder)
    analyze_records(recorder, url_file)

    date_funcs = set_date_funcs()
    #function_runner(date_funcs, date_test)


if __name__ == '__main__':
    main()
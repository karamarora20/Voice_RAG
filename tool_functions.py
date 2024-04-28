import wikipedia
from googlesearch import search
import speech_recognition as sr
import pyttsx3
from bs4 import BeautifulSoup
import urllib.request


engine = pyttsx3.init('sapi5')
voices= engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)

def speak(text):
    ''' Use to text as input and speak the text as output'''
    print(text)
    if "bye" in text or "exit" in text:
        return 'user said bye or exit'
    engine.say(text)
    engine.runAndWait()
    # return 'Take command from the user '


def takecommand():
        #takes voice input and string as output
    ''' Use to take voice input from the user and get the text as command'''
    r= sr.Recognizer()
    with sr.Microphone()as source:
        print('listening.....')
        r.pause_threshold=1
        r.energy_threshold=500
        audio=r.listen(source)
        
        
    try:
        print('recognizing....')
        query= r.recognize_google(audio, language='en-in')
        print(f'user said,{query}\n')
    except Exception as e:
        #print(e)
        speak('say that again please')
        return 'none'
    return query


def search_wiki(query):
            ''' Uses wikipedia to search for the query and returns the search results'''
            try:
                return wikipedia.summary(query)
            except Exception as e:
                return 'could not find the search results try again with different query'

def google_search(query):
    ''' Uses google search to search for the query and returns the search results'''
    search_results = []
    for url in search(query, num_results=4):
            try:
                search_results.append(extract_text_from_url(url))
            except Exception:
                continue
            
    return '* '.join(search_results)
    
def extract_text_from_url(url):
    ''' Uses the url to visit the webpage and extract the text from the page and returns the text'''

# Define the URL to fetch HTML from


# Fetch the HTML content
    response = urllib.request.urlopen(url)
    html = response.read().decode("utf-8")
    soup= BeautifulSoup(html, 'html.parser')
    text= soup.find_all('p')
    text= ' '.join([t.get_text() for t in text])
    return text


# print(google_search('python'))

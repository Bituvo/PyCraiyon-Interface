'''
PyCraiyon Interface
--------------------
Parameters:
  1. Prompt for Craiyon's image generation AI
  2. Directory for the images to be saved in
  3. File extension for the images, without a period

All parameters must be in "double quotes"'''

import os
from requests import post
from requests.structures import CaseInsensitiveDict
from json import loads
from PIL import Image
from io import BytesIO
from base64 import b64decode
from html import escape
from sys import argv
from colorama import init, Fore

def sendRequest(url, headers, data):
    resp = post(url, headers=headers, data=data)
    return loads(resp.text)['images']

init(convert=True) # Without this, colored text would not work

arguments = [i for i in argv[1:]]

illegalChars = '<>:"/\|?*'.join([chr(i) for i in range(32)])

if len(arguments) == 1 and arguments[0].lower() == 'help':
    print(Fore.YELLOW.join(i for i in __doc__))
    
elif len(arguments) > 1 and len(arguments) < 4:
    prompt = escape(arguments[0])
    directory = arguments[1]
    fileFormat = arguments[2].lower()

    if fileFormat.startswith('.'):
        print(Fore.YELLOW + 'Period detected in file format, fixing')
        fileFormat = fileFormat[1:]

    if directory[1] != ':': # Directory is not from main drive folder
        print(Fore.YELLOW + 'Directory is not from main drive folder, using current directory')
        directory = os.getcwd() + '\\' + directory

    print(Fore.GREEN + 'Prompt: ' + Fore.WHITE + prompt)
    print(Fore.GREEN + 'Directory: ' + Fore.WHITE + directory)
    print(Fore.GREEN + 'File format: ' + Fore.WHITE + fileFormat)

    print('\n' + Fore.BLUE + 'Sending POST request to "https://backend.craiyon.com/generate"...')

    url = 'https://backend.craiyon.com/generate'
    headers = {'Content-Type': 'application/json'}
    data = f'"prompt": "{prompt}<br>"'
    data = '{' + data + '}'

    print(Fore.GREEN + 'Headers: ' + Fore.WHITE + str(headers))
    print(Fore.GREEN + 'Data: ' + Fore.WHITE + data)

    response = sendRequest(url, headers, data)

    print(Fore.GREEN + '\nDecoding images...')

    decoded = []
    i = 0
    for image in response:
        i += 1
        decoded.append(BytesIO(b64decode(image)))
        print(Fore.BLUE + f'Decoded image {i}')

    print(Fore.GREEN + '\nSaving images...')

    newPrompt = ''.join([i for i in prompt if i not in illegalChars])
    if newPrompt != prompt:
        print(Fore.YELLOW + '\nIllegal characters detected in prompt string, removing...')

    if len(newPrompt) > 50:
        print(Fore.YELLOW + '\nPrompt string exceeds 50 characters, trimming...')
        newPrompt = newPrompt[:49]

    print('\n')

    i = 0
    for image in decoded:
        i += 1
        im = Image.open(image)
        fileName = newPrompt + f'-{i}.{fileFormat}'
        im.save(directory + '\\' + fileName)
        print(Fore.BLUE + f'Saved image {i} as {fileName}')

    print(Fore.GREEN + '\nDone!')

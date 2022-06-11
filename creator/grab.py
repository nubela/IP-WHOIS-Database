from unicodedata import decimal
from flask import Flask, render_template, flash, request, url_for, redirect, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func, update, desc
from os import path
from requests import get
import socket
from struct import unpack
from json import loads, dumps




with open('./raw/ip2asn-v4.tsv', 'r', encoding="utf-8") as f:
    ip2asn = f.read().split('\n')
with open('./ipfull2.txt', 'r', encoding="utf-8") as f:
    ipfull = f.read().split('\n')

print('STEP 1')
fullarray = []
for ip in ipfull:
    fullarray.append(ip.split(',')[0])

print('STEP 2')
asnnumber = 0
asnarray = []
for ip in ip2asn:
    asnnumber = asnnumber + 1
    asnarray.append(ip.split('\t')[0])
print(asnnumber)

print('STEP 3')
number = 0
number2 = 0
errnumber = 0
exnumber = 0
print('START IP ARRAY')

for ip in ip2asn:
    number = number + 1
    try:
        array = ip.split('\t')
        if array[0] in fullarray:
                exnumber = exnumber + 1

        else:
            number2 = number2 + 1
            try:
                ip = array[0][:-1] + "1"
                answer = get(f'https://ipinfo.io/{array[0]}?token=00607e30e8c82d')
                try:
                    lon = loads(answer.text)['loc'].split(',')[0]
                except: lon = '0'
                try:
                    lat = loads(answer.text)['loc'].split(',')[1]
                except: lat = '0'
                try:
                    region = loads(answer.text)['region']
                except: region = '0'
                try:
                    city = loads(answer.text)['city']
                except: city = '0'
                try:
                    zip = loads(answer.text)['postal'] 
                except: zip = '0'
                try:
                    countryCode =  loads(answer.text)['country']
                except: countryCode = '0'
                try:
                    name = loads(answer.text)['asn']['name']
                except: name = '0'
                try:
                    isp =  loads(answer.text)['asn']['type']
                except: isp = '0'
                try:
                    org = loads(answer.text)['company']['name']
                except: org = '0'
                try:
                    website = loads(answer.text)['asn']['domain']
                except: website = '0'

                with open('./ipfull.txt', 'a', encoding="utf-8") as f:
                    f.write(f"{array[0]},{lon},{lat},{region},{city},{zip},{countryCode},{name},{isp},{org},{website}\n")
                print(f"{number}/{asnnumber}|{number2}|{errnumber}: {array[0]},{lon},{lat},{region},{city},{zip},{countryCode},{name},{isp},{org},{website}")

            except socket.error:  
                errnumber = errnumber + 1      
                print(f'IP not valid: {ip}')



    except:
        print(f'ERROR {number2}/{number}: {ip}')

print(f"FERTIG: {number}/{asnnumber}|{number2}|{errnumber}")







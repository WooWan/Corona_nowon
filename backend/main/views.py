from django.shortcuts import render
from .models import Corona
from rest_framework.viewsets import ModelViewSet
# from dateutil.parser import parse as date_parse
from datetime import datetime
from bs4 import BeautifulSoup
# import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from .models import Corona
from .serializers import CoronaSerializer
from rest_framework.permissions import AllowAny

class CoronaViewSet(ModelViewSet):
	queryset=Corona.objects.all()
	serializer_class=CoronaSerializer
	permission_classes=[AllowAny]

	options = Options()
	options.headless = True
	browser = webdriver.Chrome(
		executable_path="./chromedriver.exe", options=options)
	browser.get("https://www.nowon.kr/corona19/index.do")
	time.sleep(1)
	req = browser.page_source

	soup = BeautifulSoup(req, "html.parser")
	#findall은 모든태그를 리스트로 리턴한다
	titles = soup.findAll("div", {"class": "accordion-title"})
	#
	get_patients_num = soup.select('.text-17')
	arr = []
	# split으로 나눌때 arr에 2중 list로 들어가게된다
	for i in range(10):
		arr.append(titles[i].text.strip().split('\n'))

	dong = {'상계1동': 0, '상계2동': 0, '상계3.4동': 0, '상계5동': 0, '상계6.7동': 0, '상계8동': 0, '상계9동': 0, '상계10동': 0, '중계1동': 0,
			'중계2.3동': 0, '중계본동': 0, '중계4동': 0, '월계1동': 0, ' 월계2동': 0, '월계3동': 0, '하계1동': 0, '하계2동': 0, '공릉1동': 0, '공릉2동': 0}
	patients = {}
	arr[2][1] = '노원구 881번 확진자(중계1동)'
	for i in range(10):
		patients[i] = {}
		for j in range(3):
			if(j == 0):
				patients[i]["ID"] = arr[i][j]
			if(j == 1):
				if '동' in arr[i][j]:
					exact_dong = arr[i][j].split("(")[1].split(")")[0]
					dong[exact_dong] += 1
				patients[i]["Region"] = arr[i][j]
			if(j == 2):
				patients[i]["Confirmed Date"] = arr[i][j]
	for dong, n in dong.items():
		Corona(region=dong, num=n).save()


import urllib.request, os
import csv
import json
import pandas as pd
import requests

 
API= "5b3ce3597851110001cf6248cb84acffbf6f45b5beb95fe0ebc3b876"
sogn_k=[]
sogn_nr =[]
sogn_navn=[]
by_k=[]
by_navn=[]
by_k_hard='12.57, 55.68', '10.209722, 56.156389', '10.383333, 55.4', '9.919444, 57.051111', '8.451389, 55.470833', '10.039167, 56.456944', '9.472222, 55.490833', '9.851944, 55.861944', '9.533333, 55.708333', '12.080833, 55.641667', '8.976667, 56.136111', '12.499167, 55.878611', '12.606667, 56.035', '9.55, 56.166667', '11.756667, 55.229444', '9.75, 55.566667', '9.4, 56.45', '12.179722, 55.456111', '8.6175, 56.358056', '12.3, 55.65', '11.35, 55.400833', '12.3, 55.933333', '11.713333, 55.719444', '9.786667, 54.911389', '10.61, 55.059722', '9.986667, 57.46', '10.536667, 57.44', '9.922778, 57.058333', '11.788056, 55.445556', '12.183333, 55.766667', '9.487778, 55.249444', '12.43, 55.838889', '9.026944, 56.566667', '12.358056, 55.808333', '12.3, 55.733333', '9.9325, 56.033333', '10.789722, 55.312222', '12.344167, 55.868611', '11.883333, 54.766667', '11.085, 55.681389', '9.418056, 55.044444', '12.219444, 55.531944', '12.0625, 55.8375, ', '9.161667, 56.136667', '9.733333, 55.5', '10.875833, 56.413333', '11.139722, 55.333611', '8.480556, 55.62', '14.7, 55.1', '8.6925, 56.955833'


# input 1 Sogn Gps -coordinates and number
with open('C:\\Users\\au337954\\Documents\\python\\Geo afstand\\Sogne_data.txt', mode='r',encoding="utf-8-sig") as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=',')
	line_count = 0

	for row in csv_reader: 
		sogn_k_temp = row["LONGITUDE"] +  "," + row["LATITUDE"]
		sogn_nr_temp = row["SOGNEKODE"]
		sogn_navn_temp = row["SOGNENAVN"]

		sogn_k.append(str(sogn_k_temp))
		sogn_nr.append(str(sogn_nr_temp))
		sogn_navn.append(str(sogn_navn_temp))

# input 2 - By -cordinates and name  
with open('C:\\Users\\au337954\\Documents\\python\\Geo afstand\\GEO_byer.csv', mode='r') as csv_file:
	csv_reader = csv.DictReader(csv_file , delimiter=',')
	line_count = 0

	for row in csv_reader: 
		temp_by_k = row["coordinates"]
		tempby = row["by"]
		by_k.append(str(temp_by_k))
		by_navn.append(str(tempby))	

#takes a list of strings and formats it into a tuple of lists
def ListToBodyFormatted(listToChange):
	tempList = []
	for x in listToChange:
		inputSplit = x.split(',')
		coordinateList = []
		coordinateList.append(float(inputSplit[0]))
		coordinateList.append(float(inputSplit[1]))
		tempList.append(coordinateList)

	return tuple(tempList)



def apicall(byen, sogn):

	#Split sogn into smaller lists
	locationsPerRequest = 300
	sogn_requests = [sogn[x:x+locationsPerRequest] for x in range(0,len(sogn),locationsPerRequest)]
	print('Sogn divided into ' + str(len(sogn_requests)) + ' sublists with ' + str(locationsPerRequest) + ' locations in each.')


	i = 0
	for sogn_sublist in sogn_requests:
		print(i)

		sogn_sublist.insert(0,byen)
		sognSublistFormatted = ListToBodyFormatted(sogn_sublist)
		body = {"locations": sognSublistFormatted,"destinations":[0],"metrics":["distance"],"units":"m"}
		headers = {
		    'Accept': 'application/json, application/geo+json, application/gpx+xml, img/png; charset=utf-8',
		    'Authorization': API,
		    'Content-Type': 'application/json; charset=utf-8'
			}

		call = requests.post('https://api.openrouteservice.org/v2/matrix/driving-car', json=body, headers=headers)
		print(str(i)+' done')
		i = i+1
			
		response = call.json()

		output_a.extend(response['distances'])
		
		output_k.extend(response['metadata']['query']['locations'])
		
	return


o=0	
for j in by_k_hard:
	output_a=[]
	output_k=[]
	print('arbejde med by #'+ str(j)) 
	apicall(j,sogn_k)
	
	data_tuples = list(zip(output_a,output_k))
	# constructing dataframe in pandas
	df=pd.DataFrame(data_tuples, columns=['afstand '+str(o),'Sogn_kordinat'])


	df.to_excel(r'C:\Users\au337954\Documents\python\Geo afstand\outputdata\output'+ str(o) + '.xlsx', index = False)
	o=o+1
	print("file with # "+str(o)+" created with " + str(len(output_a))+ " entries")

print('slut')

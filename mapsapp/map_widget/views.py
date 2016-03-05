from django.shortcuts import render
from django.http import HttpResponse

from .models import Address
from .models import FusionTable

import json

import urllib
import requests

import httplib2
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from oauth2client import file


# Create your views here.
def home_page(request):
	#create a table and insert table id if no table in the fusiontable table
	total_tables = FusionTable.objects.count()
	print(total_tables)
	if total_tables == 0:
		#no table exist then create one
		serv = get_auth_service()
		table_id = create_table(serv)
		#add the table to db for later use
		new_table = FusionTable()
		new_table.table_id = table_id
		new_table.save()

	return render(request, 'home.html')

#add click lat, lng and address to db table, and fusion table
#then return result response along with all rows in fusion table
def add_click_location_to_store(request):
	lat = request.GET.get("lat")
	lng = request.GET.get("lng")
	address = request.GET.get("address")

	if not lat:
		response_data = {
			"status": "ERROR",
			"message": "No latitude supplied"
		}
		response = request.GET.get("callback") + "(" + response_data + ")"
		return HttpResponse(response)

	if not lng:
		response_data = {
			"status": "ERROR",
			"message": "No longitude supplied"
		}
		response = request.GET.get("callback") + "(" + response_data + ")"
		return HttpResponse(response)

	if not address:
		response_data = """{
			"status": "ERROR",
			"message": "No address supplied"
		}"""
		response = request.GET.get("callback") + "(" + response_data + ")"
		return HttpResponse(response)

	new_ad = Address()
	new_ad.latitude = lat
	new_ad.longitude = lng
	new_ad.address = address

	new_ad.save()


	#get fusion table id
	fusion_table = FusionTable.objects.all()[0]

	serv = get_auth_service()
	if not is_duplicate_row(serv, fusion_table.table_id, address):
		insert_into_fusion_table(serv, fusion_table.table_id, lat, lng, address)

	rows = get_all_rows_from_fustion_table(serv, fusion_table.table_id)

	response_data = {
		"status": "OK",
		"message": "successfully saved"
	}
	response_data["rows"] = rows
	response_data = json.dumps(response_data)

	response = request.GET.get("callback") + "(" + response_data + ")"
	return HttpResponse(response)


def reset_data(request):
	Address.objects.all().delete()

	fusion_table = FusionTable.objects.all()[0]

	serv = get_auth_service()
	reset_fusion_table(serv, fusion_table.table_id)

	response_data = {
		"status": "OK",
		"message": "successfully reset"
	}
	response_data = json.dumps(response_data)
	response = request.GET.get("callback") + "(" + response_data + ")"
	return HttpResponse(response)

def get_auth_service():
	f = open('kp.p12', 'rb')
	key = f.read()
	f.close()

	credentials = ServiceAccountCredentials.from_p12_keyfile(
    'fusiontabtwo@black-seer-124016.iam.gserviceaccount.com',
    'kp.p12', scopes='https://www.googleapis.com/auth/fusiontables')

	http = httplib2.Http()
	http = credentials.authorize(http)

	http = httplib2.Http()
	http = credentials.authorize(http)
 	#api_key = AIzaSyAXhuYNkWdhSKnnq7nRzq7N1LaSsKfx9h4
	service = build("fusiontables", "v1", http=http)

	return service

def get_all_rows_from_fustion_table(service, table_id):
	sql = "SELECT * from %s" %table_id
	resp = service.query().sql(sql=sql).execute()

	return resp.get("rows")



def create_table(service):
	resp = service.query().sql(sql="CREATE TABLE 'map_data' (lat: NUMBER, lng: NUMBER, address: STRING)").execute()
	table_id = resp['rows'][0][0]
	return table_id

def insert_into_fusion_table(service, table_id, lat, lng, address):
	insert_query = """
		INSERT INTO %s (lat, lng, address)
		 VALUES(%s, %s, '%s')
	""" %(table_id, lat, lng, address)

	# print(insert_query)
	# return
	service.query().sql(sql=insert_query).execute()

def reset_fusion_table(service, table_id):
	query = "DELETE FROM %s" %table_id
	service.query().sql(sql=query).execute()


def is_duplicate_row(service, table_id, address):
	query = "SELECT * FROM %s where address = '%s'" %(table_id, address)
	resp = service.query().sql(sql=query).execute()

	if resp.get("rows"):
		return True
	return False
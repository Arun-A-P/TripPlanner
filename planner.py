#!/usr/bin/python

import foursquare
import json
import googlemaps
import greedy
import datetime
import random
import re

google_places_key = "AIzaSyBOPCrZfbG9rYtuihd3XmkBXZ2KfGRIy2I"
google_client = googlemaps.Client(google_places_key)

# Construct the client object
client = foursquare.Foursquare(client_id='OOZYA3IHMYSRWK15Z1K24BJCUY2KFYF3SIJ2J45COUNP2GBL', client_secret='OCCBQ3I1WTQAD54LYN4LRHMAY4ZIJZ1HW15YAWXFB2SLCUH5')

def get_top_places(city):
	places = google_client.places(query=city+" tourist attraction")["results"]
	places = [place for place in places if "travel_agency" not in place["types"]]
	#sorted(places, key = lambda x : x["rating"])
	random.shuffle(places)
	return places[:10]

def get_distance_matrix(places, city):
	places_names = map(lambda x: x["name"] + ", " + x["formatted_address"], places)
	matrix = google_client.distance_matrix(places_names, places_names)
	#print places
	return matrix

def filter_places(matrix):
	filtered_places = []
	for idx, place in enumerate(matrix["origin_addresses"]):
		if place == "":
			filtered_places.append(idx)
	return filtered_places

welcome_lines = ["I have an exciting day lined up for you in ", "I have an action packed day lined up for you in ", "I have an amazing day planned for you in "]

reach_lines = ['You should reach {0} by <say-as interpret-as="date">{1}</say-as>', 'By <say-as interpret-as="date">{1}</say-as>, you will be at {0}', 'Your next part of the journey awaits you at {0}, try to reach there by <say-as interpret-as="date">{1}</say-as>']
leave_here_lines = ['Leave here by <say-as interpret-as="date">{0}</say-as>', 'Wrap it up by <say-as interpret-as="date">{0}</say-as>']
next_destination_lines = ['Your next destination is {0} minutes away', 'It takes {0} minutes to reach the next spot', 'You are {0} minutes away from your next destination']

def get_random_string(strings):
	return random.choice(strings)

def build_text_response(city, route_sequence, matrix, places):
	text_response = get_random_string(welcome_lines) + city + ". "
	current_time = datetime.datetime(100,1,1,9,0,0)

	text_response += 'Your day starts at ' + places[route_sequence[0]]["name"] + ", "
	text_response += 'and includes amazing places to visit such as '
	text_response += ", ".join(map(lambda x: places[x]["name"], route_sequence[1:-1]))
	text_response += " and your trip finally comes to an end with you visiting " + places[route_sequence[len(route_sequence)-1]]["name"] + "."
	text_response += " Visit the alexa app, to review the trip schedule in a greater detail."
	print text_response
	return text_response

def build_card_response(route_sequence, matrix, places):
	card_response = "Your Trip Itinerary follows: \n\n"
	current_time = datetime.datetime(100,1,1,9,0,0)
	for i in range(len(route_sequence)):
		idx = route_sequence[i]
		place = places[idx]
		card_response += str(current_time.time().strftime('%I:%M%p')) + " " +place["name"] + "\n"

		current_time = current_time + datetime.timedelta(0,1800)

		card_response += "Leave here by " + str(current_time.time().strftime('%I:%M%p')) + "\n"

		if i+1 < len(route_sequence):
			current_time = current_time + datetime.timedelta(0, matrix[idx][route_sequence[i + 1]])
			card_response += "Next destination is " + str(matrix[idx][route_sequence[i + 1]] / 60) + " minutes away\n\n"
		else:
			card_response += "\nYour day ends here, Hope you have a great trip!"
	print card_response
	return card_response

def get_image(places):
	random.shuffle(places)
	for place in places:
		if "photos" in place and len(place["photos"]) >= 1:
			photo = place["photos"][0]
			photo_reference = photo["photo_reference"]
			photo = {
		        "smallImageUrl": "https://maps.googleapis.com/maps/api/place/photo?maxwidth=800&photoreference={0}&key={1}".format(photo_reference, google_places_key),
		        "largeImageUrl": "https://maps.googleapis.com/maps/api/place/photo?maxwidth=1600&photoreference={0}&key={1}".format(photo_reference, google_places_key)
		      }
			return photo
	return None

def get_time_hours(time):
	duration = 0
	temp = 0
	index = re.search("\d", time)
	for i in range(index.start(), len(time)):
		if time[i].isdigit():
			temp = temp * 10 + int(time[i])
		else:
			if time[i] == "H":
				duration = duration + temp
			elif time[i] == "M":
				duration = duration + temp/60
			elif time[i] == "D":
				duration = duration + temp * 24
			temp = 0
	print duration
	return duration

def check_time(route_sequence, matrix):
	time_taken = 0
	for i in range(len(route_sequence)):
		idx = route_sequence[i]
		if i+1 < len(route_sequence):
			time_taken += 30 + (matrix[idx][route_sequence[i + 1]]) / 60
	return (time_taken + 30)

def get_route_sequence(city, time):
	print "Getting route sequence"
	time = get_time_hours(time)
	places = get_top_places(city)
	matrix = get_distance_matrix(places, city)
	filtered_places = filter_places(matrix)
	places = [place for idx, place in enumerate(places) if idx not in filtered_places]
	mat = []
	route_sequence = []
	for idx, row in enumerate(matrix["rows"]):
		if idx in filtered_places:
			continue
		matrow = []
		for jdx, col in enumerate(row["elements"]):
			if jdx not in filtered_places:
				matrow.append(col["distance"]["value"])
		mat.append(matrow)
	timemat = []
	for idx, row in enumerate(matrix["rows"]):
		if idx in filtered_places:
			continue
		matrow = []
		for jdx, col in enumerate(row["elements"]):
			if jdx not in filtered_places:
				matrow.append(col["duration"]["value"])
		timemat.append(matrow)
	i = 0
	for i in range(len(mat) + 1):
		route_sequence = greedy.solve_tsp(mat)
		if check_time(route_sequence, timemat) <= time * 60:
			break
		else:
			mat = mat[:len(mat) - 1]
			for row in mat:
				del row[len(mat)]
	places_names = map(lambda x: x["name"], places)
	places = places[:len(route_sequence)]
	route = map(lambda x: places_names[x], route_sequence)
	card_response = build_card_response(route_sequence, timemat, places)
	text_response = build_text_response(city, route_sequence, timemat, places)
	photo = get_image(places)
	return (text_response, card_response, photo)

import requests
import json
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

#global variables
state = ""
cat1_list = []
cat2_list = []
cat3_list = []
length_of_data = 0

abbre_to_fullName_dict = {
	"AL": "Alabama",
	"AK": "Alaska", 
	"AZ": "Arizona",
	"AR": "Arkansas", 
	"CA": "California",
	"CO": "Colorado",
	"CT": "Connecticut",
	"DE": "Delaware",
	"FL": "Florida",
	"GA": "Georgia",
	"HI": "Hawaii",
	"ID": "Idaho",
	"IL": "Illinois",
	"IA": "Iowa",
	"KS": "Kansas",
	"KY": "Kentucky",
	"LA": "Lousiana",
	"ME": "Maine",
	"MD": "Maryland",
	"MA": "Massachusetts",
	"MI": "Michigan",
	"MN": "Minnesota",
	"MO": "Missouri",
	"MT": "Montana",
	"NE": "Nebraska",
	"NV": "Nevada",
	"NH": "New Hampshire",
	"NJ": "New Jersey",
	"NM": "New Mexico",
	"NY": "New York",
	"NC": "North Carolina",
	"ND": "North Dakota", 
	"OH": "Ohio",
	"OK": "Oklahoma",
	"OR": "Oregon",
	"PA": "Pennsylvania",
	"RI": "Rhode Island",
	"SC": "South Carolina",
	"SD": "South Dakota",
	"TN": "Tennessee",
	"TX": "Texas",
	"UT": "Utah",
	"VT": "Vermont",
	"VA": "Virginia",
	"WA": "Washington",
	"WV": "West Virginia",
	"WI": "Wisconsin",
	"WY": "Wyoming"
}

@app.route("/")
def home():
	return render_template("home.html", errorMessage="")

@app.route("/", methods=['POST'])
def form_post():
	global state

	stateCode = None
	state = request.form['state'].upper()

	stateAbbreviationsList = ["AL", "AZ", "AK", "AR", "CA",
							"CO", "CT", "DE", "FL", "GA",
							 "HI", "ID", "IL", "IN", "IA",
							 "KS", "KY", "LA", "ME", "MD",
							 "MA", "MI", "MN", "MS", "MO",
							 "MT", "NE", "NV", "NH", "NJ",
							 "NM", "NY", "NC", "ND", "OH",
							 "OK", "OR", "PA", "RI", "SC", 
							 "SD", "TN", "TX", "UT", "VT", 
							 "VA", "WA", "WV", "WI", "WY"]


	if state not in stateAbbreviationsList:
		return render_template("home.html", errorMessage="Invalid state code! Please enter again.")
	else:
		return redirect(url_for("categories"))

@app.route("/categories")
def categories():
	return render_template("categories.html", state=abbre_to_fullName_dict[state])

@app.route("/categories", methods=['POST'])
def onClickedCategory():
	global cat1_list
	global cat2_list
	global cat3_list
	global length_of_data

	category_name = request.form['clicked_button']

	cat1_list = []
	cat2_list = []
	cat3_list = []

	counter = 0

	if category_name == "parks":
		cat1 = "fullName"
		cat2 = "description"
		cat3 = "directionsUrl"
	elif category_name == "campgrounds":
		cat1 = "name"
		cat2 = "description"
		cat3 = "directionsUrl"
	elif category_name == "alerts":
		cat1 = "title"
		cat2 = "description"
		cat3 = "category"
	elif category_name == "news":
		category = "newsreleases"
		cat1 = "title"
		cat2 = "abstract"
		cat3 = "releasedate"
	elif category_name == "visitor centers":
		category = "visitorcenters"
		cat1 = "name"
		cat2 = "description"
		cat3 = "directionsUrl"

	if category_name != "news" and category_name != "visitor centers":
		category = category_name

	api_url = "https://developer.nps.gov/api/v1/"+ category + \
			  "?stateCode=" + state + \
			   "&limit=5&start=0&api_key=OV49BihhD2aJhbNA0Q4GIcT42NrecOppG2pUAwCX"

	api_response = requests.get(api_url)

	api_json = api_response.json() # .json() returns a dictionary I think???

	length_of_data = len(api_json['data'])
	while (counter < 5 and counter < length_of_data):
		cat1_data = api_json['data'][counter][cat1]
		cat2_data = api_json['data'][counter][cat2]
		cat3_data = api_json['data'][counter][cat3]

		cat1_list.append(cat1_data)
		cat2_list.append(cat2_data)
		cat3_list.append(cat3_data)

		counter += 1

	if length_of_data > 0:
		return redirect(category)
	else:
		return redirect(url_for("categories"))

@app.route("/parks")
def parks():
	return render_template("parks.html", list1=cat1_list, \
						   list2=cat2_list, list3=cat3_list, \
						   length=length_of_data, state=abbre_to_fullName_dict[state].upper(),\
						   info2="Description", info3="Directions URL")

@app.route("/campgrounds")
def campgrounds():
	return render_template("campgrounds.html", list1=cat1_list, \
						   list2=cat2_list, list3=cat3_list, \
						   length=length_of_data, state=abbre_to_fullName_dict[state].upper(),\
						   info2="Description", info3="Directions URL")

@app.route("/alerts")
def alerts():
	return render_template("alerts.html", list1=cat1_list, \
						   list2=cat2_list, list3=cat3_list, \
						   length=length_of_data, state=abbre_to_fullName_dict[state].upper(),\
						   info2="Description", info3="Category")

@app.route("/newsreleases")
def newsreleases():
	return render_template("newsreleases.html", list1=cat1_list, \
						   list2=cat2_list, list3=cat3_list, \
						   length=length_of_data, state=abbre_to_fullName_dict[state].upper(),\
						   info2="Description", info3="Release Date")

@app.route("/visitorcenters")
def visitorcenters():
	return render_template("visitorcenters.html", list1=cat1_list, \
						   list2=cat2_list, list3=cat3_list, \
						   length=length_of_data, state=abbre_to_fullName_dict[state].upper(),\
						   info2="Description", info3="Directions URL")


if __name__ == "__main__":
	app.run(debug=True)
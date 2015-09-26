#Import necessary libraries
import sqlite3
from flask import Flask, jsonify, render_template
from flask_restful import Resource, Api, request

#Create Flask's class instance
app = Flask(__name__)
api = Api(app)

#Function to accept query and return the first 10 foods and their ID's
def get_from_DB(text):
	conn = sqlite3.connect('holmusk.db')

	if text == ' ':
		cursor = conn.execute("SELECT * FROM FOOD_INFO")
	else:
		cursor = conn.execute("SELECT * FROM FOOD_INFO WHERE Food LIKE '%" + text + "%'")
	
	out = []

	if(cursor):
		for i in cursor:
			out.append({
				'id': i[0],
				'Food': i[1],
				})

	conn.close()

	return jsonify({'Result': out})

#Function to retrieve nutritional information based on a give food ID
def get_nutritional(id_input):
	conn = sqlite3.connect('holmusk.db')

	cursor = conn.execute("SELECT * FROM FOOD_INFO WHERE ID=" + str(id_input))
	
	out = []

	col_idx = 0

	for i in cursor:
		out.append({
			'ID': i[0],
			'Food': i[1],
			'Company': i[2],
			'Calories': i[3],
			'Sodium': i[4],
			'Total Fat': i[5],
			'Potassium': i[6],
			'Saturated': i[7],
			'Total Carbs': i[8],
			'Polyunsaturated': i[9],
			'Dietary Fiber': i[10],
			'Monounsaturated': i[11],
			'Sugars': i[12],
			'Trans': i[13],
			'Protein': i[14],
			'Cholesterol': i[15],
			'Vitamin A': i[16],
			'Calcium': i[17],
			'Vitamin C': i[18],
			'Iron': i[19],
			})

	conn.close()

	return jsonify({'Result NUTRITION': out})

#Function to manually insert the data into the database
def addData(Food_input, Company_input, Calories_input, Sodium_input, Total_Fat_input, Potassium_input, Saturated_input, Total_Carbs_input, Polyunsaturated_input, Dietary_Fiber_input, Monounsaturated_input, Sugars_input, Trans_input, Protein_input, Cholesterol_input, Vitamin_A_input, Calcium_input, Vitamin_C_input, Iron_input):

	conn = sqlite3.connect('holmusk.db')
	print "Database opened"

	cursor = conn.execute("SELECT ID FROM FOOD_INFO")

	ids = []

	for i in cursor:
		ids.append(i[0])

	next_id = max(ids) + 1

	inp = [Food_input, Company_input, Calories_input, Sodium_input, Total_Fat_input, Potassium_input, Saturated_input, Total_Carbs_input, Polyunsaturated_input, Dietary_Fiber_input, Monounsaturated_input, Sugars_input, Trans_input, Protein_input, Cholesterol_input, Vitamin_A_input, Calcium_input, Vitamin_C_input, Iron_input]

	str_in = "INSERT INTO FOOD_INFO VALUES (" + str(next_id)

	for i in inp:
		str_in += ", '" + str(i) + "'"

	str_in += ')'

	conn.execute(str_in)
	conn.commit()
	conn.close()

#Display home page (html) as root of the application
@app.route('/')
def run():
    return render_template("/homePage.html")

#Run the get_from_DB function when the particular form (query) is submitted
@app.route('/result_query', methods=['POST', 'GET'])
def query_name():
	id_input = request.form['query']
	return get_from_DB(id_input)

#Run the get_nutritional function when the particular form (query2) is submitted
@app.route('/result_nutrition', methods=['POST', 'GET'])	
def query_name2():
	id_input = request.form['query2']
	return get_nutritional(id_input)

#Retrieve the input and pass it to addData function when the form is submitted
@app.route('/add', methods=['POST', 'GET'])	
def add():
	Food_input = request.form['Food']
	Company_input = request.form['Company']
	Calories_input = request.form['Calories']
	Sodium_input = request.form['Sodium']
	Total_Fat_input = request.form['Total_Fat']
	Potassium_input = request.form['Potassium']
	Saturated_input = request.form['Saturated']
	Total_Carbs_input = request.form['Total_Carbs']
	Polyunsaturated_input = request.form['Polyunsaturated']
	Dietary_Fiber_input = request.form['Dietary_Fiber']
	Monounsaturated_input = request.form['Monounsaturated']
	Sugars_input = request.form['Sugars']
	Trans_input = request.form['Trans']
	Protein_input = request.form['Protein']
	Cholesterol_input = request.form['Cholesterol']
	Vitamin_A_input = request.form['Vitamin_A']
	Calcium_input = request.form['Calcium']
	Vitamin_C_input = request.form['Vitamin_C']
	Iron_input = request.form['Iron']
	addData(Food_input, Company_input, Calories_input, Sodium_input, Total_Fat_input, Potassium_input, Saturated_input, Total_Carbs_input, Polyunsaturated_input, Dietary_Fiber_input, Monounsaturated_input, Sugars_input, Trans_input, Protein_input, Cholesterol_input, Vitamin_A_input, Calcium_input, Vitamin_C_input, Iron_input)
	return get_from_DB(' ')

if __name__ == '__main__':
    app.run(debug = True)

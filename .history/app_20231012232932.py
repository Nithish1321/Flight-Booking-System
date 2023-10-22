from flask import Flask,render_template,url_for,request, redirect,jsonify
from chat import get_response
from flask_cors import CORS

import pymysql
def sql_connector():
    conn=pymysql.connect(
        user='root',password='850885@nithish',db='flight',host='localhost')
    cursor=conn.cursor()
    return conn,cursor

app=Flask(__name__)
CORS(app)

app.config['SESSION_TYPE'] = 'filesystem'

@app.post("/predict")
def predict():
    text=request.get_json().get("message")
    response=get_response(text)
    message={"answer":response}
    return jsonify(message)


flight_data = [
    {"from": "Bangalore", "to": "Chennai", "flight_number": "123", "departure_time": "09:00 AM", "arriving_time": "10:30 AM"},
    {"from": "Bangalore", "to": "Chennai", "flight_number": "456", "departure_time": "10:30 AM", "arriving_time": "01:15 PM"},
    {"from": "Bangalore", "to": "Mumbai", "flight_number": "789", "departure_time": "11:45 AM", "arriving_time": "02:00 PM"},
    {"from": "Chennai", "to": "Delhi", "flight_number": "101", "departure_time": "12:15 PM", "arriving_time": "03:00 PM"},
    {"from": "Delhi", "to": "Mumbai", "flight_number": "202", "departure_time": "01:30 PM", "arriving_time": "03:45 PM"},
    {"from": "Delhi", "to": "Kolkata", "flight_number": "303", "departure_time": "02:45 PM", "arriving_time": "05:00 PM"},
    {"from": "Mumbai", "to": "Hyderabad", "flight_number": "404", "departure_time": "03:15 PM", "arriving_time": "04:30 PM"},
    {"from": "Mumbai", "to": "Chennai", "flight_number": "505", "departure_time": "04:30 PM", "arriving_time": "06:15 PM"},
    {"from": "Kolkata", "to": "Chennai", "flight_number": "606", "departure_time": "05:45 PM", "arriving_time": "07:30 PM"},
    {"from": "Kolkata", "to": "Mumbai", "flight_number": "707", "departure_time": "06:00 PM", "arriving_time": "08:45 PM"},
    {"from": "Hyderabad", "to": "Bangalore", "flight_number": "808", "departure_time": "07:15 PM", "arriving_time": "09:00 PM"},
    {"from": "Hyderabad", "to": "Delhi", "flight_number": "909", "departure_time": "08:30 PM", "arriving_time": "11:15 PM"},
    # Add more flight data here
]



@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        # Retrieve user input from the form
        from_location = request.form.get('from')
        to_location = request.form.get('to')

        # Filter flight data based on user input
        matching_flights = [flight for flight in flight_data if flight["from"] == from_location and flight["to"] == to_location]

        # Pass matching flights to the display page
        return render_template('display.html', flights=matching_flights)

    return render_template('index.html')

@app.route("/chatbox")
def chatbox():
    return render_template('chatbox.html')


@app.route("/payprocess")
def payprocess():
    return render_template('paymentprocess.html')

@app.route("/display")
def display():
    return render_template('display.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        conn, c = sql_connector()
        c.execute("INSERT INTO SIGNUP VALUES ('{}','{}','{}')".format(
            name, email, password))
        conn.commit()
        conn.close()
        c.close()
        print(name, email, password)

    return render_template("signup.html")


@app.route('/signin', methods=['POST'])
def signin():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        connection = pymysql.connect(host='localhost',
                                 user='root',
                                 password='850885@nithish',
                                 database='flight')
        
        cursor = connection.cursor()
        query = "SELECT * FROM SIGNUP WHERE user_email = %s AND password = %s"
        cursor.execute(query, (email, password))

        result = cursor.fetchone()
        cursor.close()
        connection.close()

        if result:
           
            return render_template("index.html")
        else:
            return redirect(url_for("nit", name="Invalid Login!"))
 

@app.route("/<name>")
def nit(name):
    return render_template("signin.html",content=name)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        conn, c = sql_connector()
        c.execute("INSERT INTO CONTACT VALUES ('{}','{}','{}')".format(
            name, email, message))
        conn.commit()
        conn.close()
        c.close()
        print(name, email, message)

    return render_template("contact.html")


@app.route('/payment')
def payment():
    return render_template("payment.html")



@app.route('/customerdetail', methods=['GET', 'POST'])
def customerdetail():
        if request.method == 'POST':
            first_name = request.form.get('first-name')
            last_name = request.form.get('last-name')
            email = request.form.get('email')
            phone = request.form.get('phone')
            billingAddress = request.form.get('billingAddress')
            city = request.form.get('city')
            state = request.form.get('state')
            depature_city = request.form.get('depature city')
            arrival_city = request.form.get('arrival city')
            depature_date = request.form.get('depature date')
            arrival_date = request.form.get('arrival date')
            classOfService = request.form.get('classOfService')
            passport_number = request.form.get('passnumber')
            passport_expiry_date = request.form.get('passexpirydate')
            visa = request.form.get('visa')
            conn, c = sql_connector()
            c.execute("INSERT INTO customerdetails (first_name, last_name, email, phone, billingAddress, city, state, depature_city, arrival_city, depature_date, arrival_date, classOfService, passport_number, passport_expiry_date, visa) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                       (first_name, last_name, email, phone, billingAddress, city, state, depature_city, arrival_city, depature_date, arrival_date, classOfService, passport_number, passport_expiry_date, visa))
            conn.commit()
            conn.close()
            c.close()

        return render_template("customerdetails.html")



if __name__ == "__main__":
    app.run(debug=True)


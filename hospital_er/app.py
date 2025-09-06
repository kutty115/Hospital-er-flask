from flask import Flask, render_template, request, redirect, url_for
import heapq

app = Flask(__name__)

class Patient:
    def __init__(self, name, age, condition, priority):
        self.name = name
        self.age = age
        self.condition = condition
        self.priority = priority

    def __lt__(self, other):
        return self.priority > other.priority

    def __str__(self):
        return f"{self.name} (Age: {self.age}, Condition: {self.condition}, Priority: {self.priority})"

waiting_list = []
discharged = []

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/add", methods=["POST"])
def add_patient():
    name = request.form["name"]
    age = int(request.form["age"])
    condition = request.form["condition"]
    priority = int(request.form["priority"])
    patient = Patient(name, age, condition, priority)
    heapq.heappush(waiting_list, patient)
    return redirect(url_for("show_waiting"))

@app.route("/waiting")
def show_waiting():
    patients = sorted(waiting_list, reverse=True)
    return render_template("waiting.html", patients=patients)

@app.route("/treat")
def treat_patient():
    if waiting_list:
        patient = heapq.heappop(waiting_list)
        discharged.append(patient)
    return redirect(url_for("show_waiting"))

@app.route("/discharged")
def show_discharged():
    return render_template("discharged.html", patients=discharged)

if __name__ == "__main__":
    app.run(debug=True)

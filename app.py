from flask import Flask, request, jsonify
from allocation import allocate_students

app = Flask(__name__)

@app.route("/allocate", methods=["POST"])
def allocate():
    data = request.json
    students = data["students"]
    internships = data["internships"]

    results = allocate_students(students, internships)

    return jsonify({"allocations": results})

if __name__ == "__main__":
    app.run(debug=True)
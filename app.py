from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_folder="static")

def calculate_need(max_matrix, alloc_matrix):
    n = len(max_matrix)
    m = len(max_matrix[0])
    return [[max_matrix[i][j] - alloc_matrix[i][j] for j in range(m)] for i in range(n)]

def is_safe_state(processes, avail, max_matrix, alloc_matrix):
    n = len(processes)
    m = len(avail)
    need = calculate_need(max_matrix, alloc_matrix)
    finish = [False]*n
    safe_seq = []
    work = avail.copy()

    while len(safe_seq) < n:
        allocated = False
        for i in range(n):
            if not finish[i] and all(need[i][j] <= work[j] for j in range(m)):
                for j in range(m):
                    work[j] += alloc_matrix[i][j]
                safe_seq.append(f"P{i}")
                finish[i] = True
                allocated = True
        if not allocated:
            break
    return (len(safe_seq) == n, safe_seq)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        num_processes = int(request.form["num_processes"])
        num_resources = int(request.form["num_resources"])
        avail = list(map(int, request.form["available"].split(",")))

        max_matrix = []
        alloc_matrix = []
        for i in range(num_processes):
            max_row = list(map(int, request.form.get(f"max_{i}").split(",")))
            alloc_row = list(map(int, request.form.get(f"alloc_{i}").split(",")))
            max_matrix.append(max_row)
            alloc_matrix.append(alloc_row)

        safe, seq = is_safe_state(list(range(num_processes)), avail, max_matrix, alloc_matrix)
        return render_template("dashboard.html", safe=safe, seq=seq, n=num_processes)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)

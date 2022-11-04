from flask import Flask, render_template, request, redirect
import pymysql

catBlog = Flask(__name__)


def connection():
    s = 'localhost'  # Your server(host) name
    d = 'cat'
    u = 'root'  # Your login user
    p = 'ztech@44'  # Your login password
    conn = pymysql.connect(host=s, user=u, password=p, database=d)
    return conn


@catBlog.route("/")  # For default route
def main():
    cats = []
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cat")

    for row in cursor.fetchall():
        cats.append({"id": row[0], "name": row[1], "color": row[2]})
    conn.close()
    return render_template("catlist.html", cats=cats)


@catBlog.route("/addcat", methods=['GET', 'POST'])
def addcat():
    if request.method == 'GET':
        return render_template("addCat.html", cats={})
    if request.method == 'POST':
        id = int(request.form["id"])
        name = request.form["name"]
        color = request.form["color"]
        conn = connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO cat (id, name, color) VALUES (%s, %s, %s)", (id, name, color))
        conn.commit()
        conn.close()
        return redirect('/')


# @catBlog.route('/updatecat/<int:id>', methods=['GET', 'POST'])
# def updatecat(id):
#     ct = []
#     conn = connection()
#     cursor = conn.cursor()
#
#     if request.method == 'GET':
#         cursor.execute("SELECT * FROM cat where id = %s", (id))
#         for row in cursor.fetchall():
#             ct.append({"id": row[0], "name": row[1], "color": row[2]})
#             conn.close()
#             return render_template('addCat.html', cats=ct[0])
#         if request.method == "POST":
#             name = str(request.form["name"])
#             color = str(request.form["color"])
#             cursor.execute("UPDATE cat SET name = %s, color = %s WHERE id = %s", (name, color,id))
#             conn.commit()
#             conn.close()
#             return redirect('/')
@catBlog.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    cr = []
    conn = connection()
    cursor = conn.cursor()
    if request.method == 'GET':
        cursor.execute("SELECT * FROM cat WHERE id = %s", (id))
        for row in cursor.fetchall():
            cr.append({"id": row[0], "name": row[1], "color": row[2]})
            conn.close()
        return render_template("addCat.html", cats=cr[0])
    if request.method == 'POST':
        name = str(request.form["name"])
        color = str(request.form["color"])

        cursor.execute("UPDATE cat SET name = %s, color = %s  WHERE id = %s", (name, color, id))
        conn.commit()
        conn.close()
        return redirect('/')
@catBlog.route('/deletecat/<int:id>')
def deletecat(id):
    conn = connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM cat WHERE id = %s", (id))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == "__main__":
    catBlog.run()

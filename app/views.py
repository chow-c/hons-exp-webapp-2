from flask import (
    render_template,
    flash,
    redirect,
    session,
    url_for,
    escape,
    request,
    json,
    jsonify,
)
from app import app
from .forms import DemographicsForm, IntroductionForm, StressForm, DocumentsForm
import MySQLdb
import time

# Connect to db
db = MySQLdb.connect(host="localhost", user="alpha", passwd="***REMOVED***", db="alpha")
cur = db.cursor()

f = open(r".\static\docs.json", "r",)
doc_file = json.load(f)
f.close()


@app.route("/log_time", methods=["POST"])
def log_time():
    try:
        with open(str(session["id"]) + "_neulog.txt", "a") as f:
            json.dump(request.json, f)
        return json.dumps({"Dump neulog file": "ok"})
    except:
        return json.dumps({"Dump neulog file": "Fail"})


def create_new_entry():
    cur.execute(
        """SELECT `order`, count(*) as count from users group by `order` order by count asc limit 1"""
    )
    lowest_order = cur.fetchall()[0][0]

    cur.execute(
        """SELECT `target`, count(*) as count from users group by `target` order by count asc limit 1"""
    )
    lowest_target = cur.fetchall()[0][0]

    query = """insert into users (`order`, `target`) values (%s, %s)"""
    args = (lowest_order, lowest_target)
    cur.execute(query, args)
    db.commit()

    return


# View for debugging
@app.route("/_test", methods=["GET", "POST"])
def test():
    cur.execute(
        "SELECT COUNT(*) FROM information_schema.columns WHERE TABLE_NAME = 'Orders' AND COLUMN_NAME LIKE 'doc%'"
    )
    col_count = int(cur.fetchall()[0][0])
    query = "SELECT `doc_"
    for x in range(1, 41):
        query = query + str(x) + "`, `doc_"
    query = query + "{} FROM Orders WHERE `order` = {}"
    cur.execute(query.format(str(col_count) + "`", str("'" + session["order"] + "'")))
    order_array = [int(i) for i in list(cur.fetchall())[0]]
    order_array.insert(0, "X")

    text = []
    text_dict = []

    for x in range(0, len(order_array)):
        for i in range(0, len(doc_file)):
            if doc_file[i]["number"] == str(order_array[x]):
                text.append(doc_file[i]["text"])
                text_dict.append(
                    {
                        "doc_num": doc_file[i]["number"],
                        "doc_sec": doc_file[i]["sec"],
                        "doc_dis": doc_file[i]["dis"],
                        "doc_com": doc_file[i]["com"],
                        "doc_psy": doc_file[i]["psy"],
                    }
                )

    title = "text_dict"
    data = text_dict
    text = text_dict[0]
    lol = text_dict[1]

    return render_template("test.html", title=title, data=data, text=text, lol=lol)


def get_user():
    query = """SELECT Users.uid, Users.target, Users.order FROM Users WHERE Users.complete = %s ORDER BY Users.order LIMIT 1"""
    args = (0,)
    cur.execute(query, args)
    data = cur.fetchall()

    # Set session variables
    session["id"] = int(data[0][0])
    session["target"] = data[0][1]
    session["order"] = data[0][2]

    print("id", session["id"])
    print("target", session["target"])
    print("order", session["order"])

    return


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def demographics():
    # Get next incomplete userID from database
    try:
        get_user()
    except:
        create_new_entry()
        get_user()

    global text
    global text_dict

    text, text_dict = get_text()

    # Generate the demographics form
    form = DemographicsForm()
    title = "Demographics"

    # If form is submitted
    if form.validate_on_submit():
        # Update database with values
        query = """UPDATE Users SET age = %s, gender = %s, degree = %s, vision = %s, complete = %s WHERE uid= %s"""
        args = (
            form.age.data,
            form.gender.data,
            form.degree.data,
            form.vision.data,
            1,
            session["id"],
        )
        cur.execute(query, args)
        db.commit()
        # Move to next page
        return redirect("/introduction")

    return render_template("demographics.html", title=title, form=form)


def get_text():
    query = """SELECT COUNT(*) FROM information_schema.columns WHERE TABLE_NAME = 'Orders' AND COLUMN_NAME LIKE 'doc%'"""
    cur.execute(query)
    col_count = int(cur.fetchall()[0][0])
    query = """SELECT doc_"""
    for x in range(1, 40):
        query = query + str(x) + """, doc_"""
    query = query + """%s FROM Orders WHERE `order` = %s"""
    args = (40, session["order"])
    cur.execute(query, args)
    order_array = [int(i) for i in list(cur.fetchall())[0]]
    order_array.insert(0, "X")

    text = []
    text_dict = []

    for x in range(0, len(order_array)):
        for i in range(0, len(doc_file)):
            if doc_file[i]["number"] == str(order_array[x]):
                text.append(doc_file[i]["text"])
                for w in ["sec", "dis", "psy", "com"]:
                    if doc_file[i][w] == "":
                        doc_file[i][w] = None
                text_dict.append(
                    {
                        "doc_num": doc_file[i]["number"],
                        "doc_sec": doc_file[i]["sec"],
                        "doc_dis": doc_file[i]["dis"],
                        "doc_com": doc_file[i]["com"],
                        "doc_psy": doc_file[i]["psy"],
                    }
                )

    return (text, text_dict)


@app.route("/introduction", methods=["GET", "POST"])
def introduction():
    form = IntroductionForm()
    title = "Introduction"
    topic, topic_para = get_topic(session["target"])
    if form.validate_on_submit():
        query = """UPDATE Users SET familiarity = %s WHERE uid= %s"""
        args = (form.familiar.data, session["id"])
        cur.execute(query, args)
        db.commit()
        # flash('Introduction data: familiar=%s' %(str(form.familiar.data)))
        return redirect("/initialstress")
    return render_template(
        "introduction.html", topic=topic, topic_para=topic_para, title=title, form=form
    )


def get_topic(target):
    if target == "dis":
        topic = "natural disasters"
        topic_para = "A <strong>natural disaster</strong> is a major adverse event resulting from natural processes of the Earth. A natural disaster can c	ause loss of life or property damage, and typically leaves some economic damage in its wake. The severity of the damage depends on the affected population's resilience, or ability to recover. An adverse event will not rise to the level of a disaster if it occurs in an area without vulnerable population."
    elif target == "com":
        topic = "computer science"
        topic_para = "<strong>Computer science</strong> is the scientific and practical approach to computation and its applications. It is the systematic study of the feasibility, structure, expression, and mechanization of the methodical procedures (or algorithms) that underlie the acquisition, representation, processing, storage, communication of, and access to information, whether such information is encoded as bits in a computer memory or transcribed in genes and protein structures in a biological cell."
    elif target == "sec":
        topic = "national security (terrorism)"
        topic_para = "<strong>National security</strong> is a concept that a government should protect the state and its citizens against all kinds of national crises through a variety of power projections, such as political power, diplomacy, economic power and military might, for example. <strong>Terrorism</strong> refers to criminal acts intended or calculated to provoke a state of terror in the general public, a group of persons or particular persons for political purposes."
    elif target == "psy":
        topic = "psychology"
        topic_para = "<strong>Psychology</strong> is the study of mind and behavior. It is an academic discipline and an applied science which seeks to understand individuals and groups by establishing general principles and researching specific cases. Psychology attempts to understand the role of mental functions in individual and social behavior, while also exploring the physiological and biological processes that underlie cognitive functions and behaviors."
    else:
        topic = "ERROR"
        topic_para = "Please speak to the instructor"
    return topic, topic_para


@app.route("/initialstress", methods=["GET", "POST"])
def initial_stress():
    form = StressForm()
    title = "Stress Levels"
    if form.validate_on_submit():
        query = """UPDATE Users SET initial_stress = %s WHERE uid= %s"""
        args = (form.stress.data, session["id"])
        cur.execute(query, args)
        db.commit()
        return redirect("/documents")
    return render_template("initial_stress.html", title=title, form=form)


@app.route("/documents", methods=["GET", "POST"])
def documents():
    form = DocumentsForm()
    title = "Documents"
    return render_template("documents.html", title=title, form=form)


@app.route("/_get_doc")
def get_doc():
    if len(text) > 1:
        doc = text[0]
        doc_next = text[1]
        del text[0]
    elif len(text) == 1:
        doc = text[0]
        doc_next = "ENDED"
        del text[0]
    else:
        doc = "ENDED"
    return jsonify(result=doc, next=doc_next)


@app.route("/_set_results", methods=["GET", "POST"])
def set_results():
    try:
        conf = request.json["conf"]
        sel = request.json["sel"]

        t = int(time.time())

        if sel == "NULL":
            sel = None
            score = 0
        elif (
            sel == str(1) and text_dict[0]["doc_%s" % session["target"]] != str(0)
        ) or (sel == str(0) and text_dict[0]["doc_%s" % session["target"]] == str(0)):
            score = 1
        # elif (sel == str(1) and text_dict[0]['doc_%s' % session['target']] == 0) or (text_dict[0]['doc_%s' % session['target']] != 0 and sel == str(0)):
        # 	score = 0
        else:
            score = 0

        if text_dict[0]["doc_num"] == "X":
            text_dict[0]["doc_num"] = 0

        query = """INSERT INTO Results (uid, target, doc_number, doc_sec, doc_com, doc_dis, doc_psy, time_spent, confidence, decision, score) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
        args = (
            session["id"],
            session["target"],
            text_dict[0]["doc_num"],
            text_dict[0]["doc_sec"],
            text_dict[0]["doc_com"],
            text_dict[0]["doc_dis"],
            text_dict[0]["doc_psy"],
            t,
            conf,
            sel,
            score,
        )
        cur.execute(query, args)
        db.commit()
        del text_dict[0]
        return json.dumps({"Set results": "ok"})
    except:
        return json.dumps({"Set results": "Fail"})
    # return json.dumps({'sel' : sel,'score':score,'target':session['target'],'type':'doc_%s' % session['target'],'content':debug['doc_%s' % session['target']]})


@app.route("/_dump_eyegaze", methods=["POST"])
def recordEye():
    try:
        with open(str(session["id"]) + "_eyedata.txt", "w") as f:
            json.dump(request.json, f)
        return json.dumps({"Dump eye gaze file": "ok"})
    except:
        return json.dumps({"Dump eye gaze file": "Fail"})


@app.route("/_dump_neulog", methods=["POST"])
def recordNeulog():
    try:
        with open(str(session["id"]) + "_neulog.txt", "a") as f:
            json.dump(request.json, f)
        return json.dumps({"Dump neulog file": "ok"})
    except:
        return json.dumps({"Dump neulog file": "Fail"})


@app.route("/finalstress", methods=["GET", "POST"])
def final_stress():
    form = StressForm()
    title = "Stress Levels"
    if form.validate_on_submit():
        query = """UPDATE Users SET final_stress = %s WHERE uid= %s"""
        args = (form.stress.data, session["id"])
        cur.execute(query, args)
        db.commit()
        # flash('Stress data: istress=%s' %(str(form.stress.data)))
        return redirect("/complete")
    return render_template("final_stress.html", title=title, form=form)


@app.route("/complete")
def complete():
    title = "Finished"
    query_s = """SELECT SUM(score) FROM Results WHERE uid = %s AND doc_number != '0'"""
    args_s = (session["id"],)
    cur.execute(query_s, args_s)
    score = cur.fetchall()
    query_h = """SELECT SUM(score) FROM Results WHERE doc_number != '0' GROUP BY uid ORDER BY SUM(score) DESC LIMIT 1"""
    cur.execute(query_h)
    high = cur.fetchall()
    return render_template("complete.html", title=title, score=score, high=high)

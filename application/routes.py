from flask import send_from_directory, redirect, url_for, render_template, request
import pandas as pd

from application import app

ALLOWED_EXTENSIONS = {'xls'}

GROUPS = {}
FILENAME = ""

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=['GET', 'POST'])
@app.route("/main", methods=['GET', 'POST'])
def home(message=""):
    if request.method == 'POST':
        print(request.form)
        num_groups = request.form.get('num_groups')
        if 'people' not in request.files:
            return render_template("main.html", message="Please choose a valid file.")
        file = request.files['people']
        if file.filename == '':
            return render_template("main.html", message="Please choose a valid file.")
        if num_groups == '':
            return render_template("main.html", message="Please input your desired number of groups.")
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(request.files['people'].filename)
            return redirect(url_for('calc_groups', filename=filename, num_groups=num_groups))
    return render_template("main.html", message=message)


@app.route("/calc_groups/<filename>/<num_groups>")
def calc_groups(filename="/", num_groups=1):
    print("IN CALC GROUPS")
    # f = send_from_directory("../", filename)
    # df = pd.read_excel(filename)
    # final_groups = [
    #     {"id": "1", "people": {"Bob", "Joe"}},
    #     {"id": "2", "people": {"Bob", "Joe"}},
    #     {"id": "3", "people": {"Bob", "Joe"}}
    # ]
    global FILENAME
    FILENAME = filename
    global GROUPS
    GROUPS = compute_groups(num_groups)
    print(GROUPS)
    return redirect(url_for('groups'))

@app.route("/groups")
def groups():
    return render_template("groups.html", groups=GROUPS)


@app.route("/about")
def about():
    return render_template("about.html")

import pandas as pd
from itertools import permutations
import numpy as np

def makeGroups(chunk_size):
    df = pd.read_excel(FILENAME)
    print(df)
    perms = permutations( df['Group Member Name'].tolist())
    groups = []
    print("GOT HERE")
    # print(list(perms)[0])
    for c in list(perms):
        print(c)
        group = chunkArray(c, chunk_size)
        if group in groups:
            continue
        groups.append(group)

    return groups

def chunkArray(myArray, chunk_size):
    index = 0
    arrayLength = len(myArray)
    tempArray = []

    while index < arrayLength:
        myChunk = myArray[index : index + chunk_size]
        tempArray.append(myChunk)
        index += chunk_size
    return frozenset(frozenset(i) for i in tempArray)

def getGroupRows(group):
    df = pd.read_excel(FILENAME)
    return df[df["Group Member Name"].isin(group)]

def getAvgAge(group):
    dfgroup = getGroupRows(group)
    return np.sum(dfgroup['Age'].tolist()) / len(dfgroup['Age'].tolist())

def getMaleFemaleRatio(group):
    dfgroup = getGroupRows(group)
    return (dfgroup['Gender'].tolist().count('Male'))/len(dfgroup['Gender'].tolist())

def getAvgSkill(group):
    dfgroup = getGroupRows(group)
    people_list = dfgroup['How comfortable are you with the task that is to be done? (Scale: 1 completely lost and 5 is very comfortable)'].tolist();
    avg_skill = np.sum(people_list) / len(people_list)
    return avg_skill

def getRaceIndex(group):
    dfgroup = getGroupRows(group)
    percentblack = dfgroup['Race '].tolist().count('Black or African American')/len(dfgroup['Race '].tolist())
    percentasian = dfgroup['Race '].tolist().count('Asian')/len(dfgroup['Race '].tolist())
    percentamerind = dfgroup['Race '].tolist().count('American Indian or Alaska Native')/len(dfgroup['Race '].tolist())
    percentwhite = dfgroup['Race '].tolist().count('White')/len(dfgroup['Race '].tolist())
    percentnathaw = dfgroup['Race '].tolist().count('Native Hawaiian or Other Pacific Islander')/len(dfgroup['Race '].tolist())

    return [percentblack, percentasian, percentamerind, percentwhite, percentnathaw]

def getPopulationValues(dfpop):
    return [getRaceIndex(dfpop['Group Member Name']),getAvgAge(dfpop['Group Member Name']),getMaleFemaleRatio(dfpop['Group Member Name']),getAvgSkill(dfpop['Group Member Name'])]

def compute_groups(num_groups):
    print("HELOOOOOOOO")
    groupslist = list(makeGroups(int(num_groups)))
    popValues = getPopulationValues(pd.read_excel(FILENAME))

    list(list(groupslist[0])[0])
    groupvaluelist = []
    for i in groupslist:
        for x in i:
            groupvaluelist.append(getPopulationValues(getGroupRows(list(x))))

    best = 1000
    bestgroup = []

    for i in range(len(groupvaluelist)):
        the_sum = 0
        for x in range(4):
            if x == 0 :
                for y in range(5):
                    the_sum = the_sum +( abs(popValues[0][y]-groupvaluelist[i][x][y]))
            else:
                the_sum = the_sum +abs(popValues[x] - groupvaluelist[i][x])
        if the_sum < best:
            best = the_sum
            bestgroup = groupslist[i]

    final_groups = []
    idx = 1
    for g in bestgroup:
        team = {}
        team["id"] = idx
        team["people"] = list(g)
        final_groups.append(team)
        idx += 1
    return final_groups

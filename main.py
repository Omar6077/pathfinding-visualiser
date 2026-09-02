import tkinter as tk
from customtkinter import CTk, CTkOptionMenu, CTkFrame, CTkLabel, CTkButton, CTkEntry, CTkCheckBox
from collections import deque
import time
import heapq

walls = set()
weights = {}
cellrectangles = {}
start = None
end = None
mode = "wall"
algo = "BFS"
resultsvalid = False
animate = True

def creategrid():
    for row in range(rows):
        for column in range(columns):
            x1 = column * cellsize
            y1 = row * cellsize
            x2 = x1 + cellsize
            y2 = y1 + cellsize

            rectangleid = canvas.create_rectangle(x1, y1, x2, y2, fill = "white")
            cellrectangles[(row, column)] = rectangleid

def placecell(event):
    global start
    global end
    column = (event.x - offsetx) // cellsize
    row = (event.y - offsety) // cellsize
    if row < 0 or row >= rows or column < 0 or column >= columns:
        return
    rectangleid = cellrectangles[(row, column)]
    if mode == "wall":
        addwall(event)

    elif mode == "start":
        if (row, column) == end:
            return
        if (row, column) != start:
            invalidate()
        if (row, column) in walls:
            walls.remove((row, column))
        if (row, column) in weights:
            del weights[(row, column)]
        if start is not None:
            oldrectangle = cellrectangles[start]
            canvas.itemconfig(oldrectangle, fill = "white")
        start = (row, column)
        canvas.itemconfig(rectangleid, fill = "green")

    elif mode == "end":
        if (row, column) == start:
            return
        if (row, column) in walls:
            walls.remove((row, column))
        if (row, column) in weights:
            del weights[(row, column)]
        if (row, column) != end:
            invalidate()
        if end is not None:
            oldrectangle = cellrectangles[end]
            canvas.itemconfig(oldrectangle, fill = "white")
        end = (row, column)
        canvas.itemconfig(rectangleid, fill = "red")

    elif mode == "weight":
        if (row, column) == start or (row, column) == end:
            return
        invalidate()

        if (row, column) in walls:
            walls.remove((row, column))

        weights[(row, column)] = 5
        canvas.itemconfig(rectangleid, fill = "#ff6e2b")


    elif mode == "erase":
        removewall(event)

def setmode(newmode):
    global mode
    mode = newmode
    feedback.configure(text = f"Mode changed to {mode}")

def addwall(event):
    column = (event.x - offsetx) // cellsize
    row = (event.y - offsety) // cellsize
    if row < 0 or row >= rows or column < 0 or column >= columns:
        return
    rectangleid = cellrectangles[(row, column)]
    if (row, column) not in walls and (row, column) != start and (row, column) != end:
        invalidate()

        if (row, column) in weights:
            del weights[(row, column)]


        canvas.itemconfig(rectangleid, fill = "black")
        walls.add((row, column))

def resizegrid(event = None):
    global cellsize, offsetx, offsety

    currentwidth = canvas.winfo_width()
    currentheight = canvas.winfo_height()

    if currentwidth <= 1 or currentheight <= 1:
        return

    cellsize = min(currentwidth / columns, currentheight / rows)

    gridwidth = cellsize * columns
    gridheight = cellsize * rows

    offsetx = (currentwidth - gridwidth) / 2
    offsety = (currentheight - gridheight) / 2

    for row in range(rows):
        for column in range(columns):
            rectangleid = cellrectangles[(row, column)]

            x1 = offsetx + column * cellsize
            y1 = offsety + row * cellsize
            x2 = x1 + cellsize
            y2 = y1 + cellsize

            canvas.coords(rectangleid, x1, y1, x2, y2)

def applygridsize():
    global rows, columns, start, end

    try:
        newrows = int(rentry.get())
        newcolumns = int(centry.get())
    except ValueError:
        gfeedback.configure(text = "Please enter whole numbers only")
        return

    if newrows < 2 or newcolumns < 2:
        gfeedback.configure(text = "Must be 2x2 or larger")
        return

    if newrows > 300 or newcolumns > 300:
        gfeedback.configure(text = "Must be smaller than 300x300")
        return

    canvas.delete("all")
    cellrectangles.clear()
    walls.clear()
    weights.clear()

    start = None
    end = None

    gfeedback.configure(text = "")
    rows = newrows
    columns = newcolumns

    invalidate()
    creategrid()
    resizegrid()

def removewall(event):
    column = (event.x - offsetx) // cellsize
    row = (event.y - offsety) // cellsize
    if row < 0 or row >= rows or column < 0 or column >= columns:
        return
    rectangleid = cellrectangles[(row, column)]
    if (row, column) in walls:
            invalidate()
            canvas.itemconfig(rectangleid, fill = "white")
            walls.remove((row, column))
    elif (row, column) in weights:
        invalidate()
        canvas.itemconfig(rectangleid, fill = "white")
        del weights[(row, column)]

def clearsearch():
    for cell in cellrectangles:
        rectangleid = cellrectangles[cell]

        if cell in weights:
            canvas.itemconfig(rectangleid, fill = "#ff6e2b")

        elif cell not in walls and cell != start and cell != end:
            canvas.itemconfig(rectangleid, fill = "white")

def clearall():
    global start, end
    start = None
    end = None
    for cell in cellrectangles:
        rectangleid = cellrectangles[cell]
        canvas.itemconfig(rectangleid, fill = "white")
    walls.clear()
    weights.clear()
    invalidate()
    clearsearch()

def setalgo(newalgo):
    global algo
    algo = newalgo
    feedback.configure(text = f"Algorithm changed to {algo}")

def runalgo():
    global resultsvalid
    if start is None or end is None:
        feedback.configure(text = "Please pick a start and end point first")
        return

    clearsearch()
    if algo == "BFS":
        success = bfs()
    elif algo == "Dijkstra's":
        success = dijkstra()
    elif algo == "A*":
        success = a()

    if success:
        resultsvalid = True

def clearresults():
    bfsvisit.configure(text = "-")
    bfspath.configure(text = "-")
    bfstime.configure(text = "-")
    bfscost.configure(text = "-")

    dijkvisit.configure(text = "-")
    dijkpath.configure(text = "-")
    dijktime.configure(text = "-")
    dijkcost.configure(text = "-")

    avisit.configure(text = "-")
    apath.configure(text = "-")
    atime.configure(text = "-")
    acost.configure(text = "-")

def invalidate():
    global resultsvalid



    if resultsvalid:
        clearsearch()
        clearresults()
        resultsvalid = False

def bfs():
    starttime = time.perf_counter()
    nodesexp = 0
    queue = deque([start])
    visited = {start}
    camefrom = {}
    path = []
    visitorder = []
    while queue:
        current = queue.popleft()
        visitorder.append(current)
        nodesexp += 1
        if current == end:
            break
        row, column = current
        neighbours = [(row - 1, column), (row + 1, column), (row, column - 1), (row, column + 1)]
        for neighbour in neighbours:
            nrow, ncolumn = neighbour
            if neighbour not in walls and neighbour not in visited:
                if 0 <= nrow < rows and 0 <= ncolumn < columns:
                    queue.append(neighbour)
                    visited.add(neighbour)
                    camefrom[neighbour] = current
    current = end
    if end not in camefrom:
        feedback.configure(text = "No path found!")
        return False
    while current != start:
        path.append(current)
        current = camefrom[current]
    path.append(current)
    path.reverse()
    pathcost = 0
    for cell in path[1:]:
        pathcost += weights.get(cell, 1)
    endtime = time.perf_counter()
    exetime = endtime - starttime
    if exetime > 0.1:
        multiplier = 100
    elif exetime > 0.05:
        multiplier = 500
    elif exetime > 0.01:
        multiplier = 750
    elif exetime > 0.005:
        multiplier = 1250
    elif exetime > 0.0025:
        multiplier = 1500
    elif exetime > 0.001:
        multiplier = 2500
    else:
        multiplier = 5000
    aniduration = exetime * multiplier
    delay = max(round((aniduration * 1000) / len(visitorder)), 15)
    anidurationprint = round((delay * len(visitorder)) / 1000, 2)
    estslowdown = int(round(anidurationprint / exetime, -1))
    bfsvisit.configure(text = nodesexp)
    bfspath.configure(text = len(path) - 1)
    bfstime.configure(text = f"{exetime * 1000:.3f} ms")
    bfscost.configure(text = pathcost)
    if animate is True:
        feedback.configure(text = f"Path found!")
        tfeedback.configure(text = f"Est. Animation duration: {anidurationprint}s ({estslowdown}x slower)")
        animatevisited(visitorder, path, delay)
    else:
        feedback.configure(text = "Path found!")
        showpath(path)

    return True

def dijkstra():
    starttime = time.perf_counter()
    nodesexp = 0
    visitorder = []
    distances = {}
    camefrom = {}
    for cell in cellrectangles:
        if cell not in walls:
            distances[cell] = float("inf")
    distances[start] = 0
    priorityqueue = [(0, start)]
    while priorityqueue:
        currentdist, current = heapq.heappop(priorityqueue)
        if currentdist > distances[current]:
            continue
        visitorder.append(current)
        nodesexp += 1
        if current == end:
            break
        row, column = current
        neighbours = [(row - 1, column), (row + 1, column), (row, column - 1), (row, column + 1)]
        for neighbour in neighbours:
            nrow, ncolumn = neighbour
            if 0 <= nrow < rows and 0 <= ncolumn < columns:
                if neighbour not in walls:
                    stepcost = weights.get(neighbour, 1)
                    newdist = currentdist + stepcost
                    if distances[neighbour] > newdist:
                        distances[neighbour] = newdist
                        camefrom[neighbour] = current
                        heapq.heappush(priorityqueue,(newdist, neighbour))
    path = []
    current = end
    if end not in camefrom:
        feedback.configure(text = "No path found!")
        return False
    while current != start:
        path.append(current)
        current = camefrom[current]
    path.append(current)
    path.reverse()
    endtime = time.perf_counter()
    exetime = endtime - starttime
    if exetime > 0.1:
        multiplier = 100
    elif exetime > 0.05:
        multiplier = 500
    elif exetime > 0.01:
        multiplier = 750
    elif exetime > 0.005:
        multiplier = 1250
    elif exetime > 0.0025:
        multiplier = 1500
    elif exetime > 0.001:
        multiplier = 2500
    else:
        multiplier = 5000
    aniduration = exetime * multiplier
    delay = max(round((aniduration * 1000) / len(visitorder)), 15)
    anidurationprint = round((delay * len(visitorder)) / 1000, 2)
    estslowdown = int(round(anidurationprint / exetime, -1))
    dijkvisit.configure(text = nodesexp)
    dijkpath.configure(text = len(path) - 1)
    dijktime.configure(text = f"{exetime * 1000:.3f} ms")
    dijkcost.configure(text = distances[end])
    if animate is True:
        feedback.configure(text = f"Path found!")
        tfeedback.configure(text = f"Est. Animation duration: {anidurationprint}s ({estslowdown}x slower)")
        animatevisited(visitorder, path, delay)
    else:
        feedback.configure(text = "Path found!")
        showpath(path)
    return True

def a():
    starttime = time.perf_counter()
    nodesexp = 0
    visitorder = []
    distances = {}
    camefrom = {}

    for cell in cellrectangles:
        if cell not in walls:
            distances[cell] = float("inf")

    distances[start] = 0
    priorityqueue = [(heuristic(start), 0, start)]
    while priorityqueue:
        currentf, currentdist, current = heapq.heappop(priorityqueue)
        if currentdist > distances[current]:
            continue
        visitorder.append(current)
        nodesexp += 1
        if current == end:
            break
        row, column = current
        neighbours = [(row - 1, column), (row + 1, column), (row, column - 1), (row, column + 1)]
        for neighbour in neighbours:
            nrow, ncolumn = neighbour
            if 0 <= nrow < rows and 0 <= ncolumn < columns:
                if neighbour not in walls:
                    stepcost = weights.get(neighbour, 1)
                    newdist = currentdist + stepcost
                    if distances[neighbour] > newdist:
                        distances[neighbour] = newdist
                        camefrom[neighbour] = current
                        newf = newdist + heuristic(neighbour)
                        heapq.heappush(priorityqueue,(newf, newdist, neighbour))
    path = []
    current = end
    if end not in camefrom:
        feedback.configure(text = "No path found!")
        return False
    while current != start:
        path.append(current)
        current = camefrom[current]
    path.append(current)
    path.reverse()
    endtime = time.perf_counter()
    exetime = endtime - starttime
    if exetime > 0.1:
        multiplier = 100
    elif exetime > 0.05:
        multiplier = 500
    elif exetime > 0.01:
        multiplier = 750
    elif exetime > 0.005:
        multiplier = 1250
    elif exetime > 0.0025:
        multiplier = 1500
    elif exetime > 0.001:
        multiplier = 2500
    else:
        multiplier = 5000
    aniduration = exetime * multiplier
    delay = max(round((aniduration * 1000) / len(visitorder)), 15)
    anidurationprint = round((delay * len(visitorder)) / 1000, 2)
    estslowdown = int(round(anidurationprint / exetime, -1))
    avisit.configure(text = nodesexp)
    apath.configure(text = len(path) - 1)
    atime.configure(text = f"{exetime * 1000:.3f} ms")
    acost.configure(text = distances[end])
    if animate is True:
        feedback.configure(text = f"Path found!")
        tfeedback.configure(text = f"Est. Animation duration: {anidurationprint}s ({estslowdown}x slower)")
        animatevisited(visitorder, path, delay)
    else:
        feedback.configure(text = "Path found!")
        showpath(path)
    return True

def heuristic(cell):
    row, column = cell
    endrow, endcolumn = end
    manhattandist = abs(endrow - row) + abs(endcolumn - column)
    return manhattandist

def setanimation():
    global animate
    animate = bool(anicheckbox.get())

def animatevisited(visitorder, path, delay, index = 0, anistart = None):
    if anistart is None:
        anistart = time.perf_counter()
    if index >= len(visitorder):
        actualdur = time.perf_counter() - anistart
        tfeedback.configure(text = f"Actual animation duration: {actualdur:.2f}s")
        showpath(path)
        return
    cell = visitorder[index]

    if cell != start and cell != end:
        rectangleid = cellrectangles[cell]

        if cell in weights:
            canvas.itemconfig(rectangleid, fill = "#B98565")
        else:
            canvas.itemconfig(rectangleid, fill = "#00c3ff")

    window.after(int(delay), lambda: animatevisited(visitorder, path, delay, index + 1, anistart))

def showpath(path):
    for cell in path:
        if cell != start and cell != end:
            rectangleid = cellrectangles[cell]
            canvas.itemconfig(rectangleid, fill = "yellow")

window = CTk()
window.grid_rowconfigure(0, weight = 1)
window.grid_columnconfigure(0, weight = 1)
window.grid_columnconfigure(1, weight = 0)
width = 1000
height = 800
window.geometry(f"{width}x{height}")
window.title("Pathfinding Visualiser")
canvaswidth = 600
canvasheight = 600
canvas = tk.Canvas(window, width = canvaswidth, height = canvasheight, background = "#242424", highlightthickness = 0, bd = 0)
canvas.grid(row = 0, column = 0, sticky = "nsew")
cellsize = 20
columns = canvaswidth // cellsize
rows = canvasheight // cellsize

creategrid()

controlpanel = CTkFrame(window, width=200, height=600)
controlpanel.grid(row = 0, column = 1, sticky = "ns")


title = CTkLabel(controlpanel, text = "Pathfinding Controls", font = ("Arial", 16), fg_color = "transparent")
title.pack(pady = (20,10))

gridlabel = CTkLabel(controlpanel, text = "Grid size", font = ("Arial", 12), fg_color = "transparent")
gridlabel.pack(pady = (20,10))

dimensionframe = CTkFrame(controlpanel, fg_color = "transparent")
dimensionframe.pack()

rentry = CTkEntry(dimensionframe, width = 55)
rentry.insert(0, "30")
rentry.pack(side = "left")
xlab = CTkLabel(dimensionframe, text = "x", fg_color = "transparent")
xlab.pack(side = "left", padx = 8)
centry = CTkEntry(dimensionframe, width = 55)
centry.insert(0, "30")
centry.pack(side = "left")
applybutton = CTkButton(controlpanel, text = "Apply", command = applygridsize, fg_color="#0099FF", text_color="black")
applybutton.pack(padx = 20, pady = 10)

gfeedback = CTkLabel(controlpanel, text = "", font = ("Arial", 12), fg_color = "transparent", text_color = "red")
gfeedback.pack(pady = (0,0))

dmode = CTkLabel(controlpanel, text = "Drawing mode", font = ("Arial", 12), fg_color = "transparent")
dmode.pack(pady = (20,10))

modemenu = CTkOptionMenu(controlpanel, values = ["wall", "start", "end", "weight", "erase"], command = setmode)
modemenu.set(mode)
modemenu.pack(padx = 20, pady = (0,20))

algoselect = CTkLabel(controlpanel, text = "Algorithm", font = ("Arial", 12), fg_color = "transparent")
algoselect.pack(pady = (20,10))

algomenu = CTkOptionMenu(controlpanel, values = ["BFS", "Dijkstra's", "A*"], command = setalgo)
algomenu.set(algo)
algomenu.pack(padx = 20, pady = (0,20))

anicheckbox = CTkCheckBox(controlpanel, text = "Animate search", command = setanimation)
anicheckbox.select()
anicheckbox.pack(padx = 20, pady = 10)

runbutton = CTkButton(controlpanel, text = "Run", command = runalgo, fg_color="yellow", text_color="black")
runbutton.pack(padx = 20, pady = 10)

clearbutton = CTkButton(controlpanel, text = "Clear", command = clearall, fg_color="red")
clearbutton.pack(padx = 20, pady = 10)

resultsframe = CTkFrame(controlpanel)
resultsframe.pack(padx = 10, pady = (15, 10), fill = "x")

resultstitle = CTkLabel(resultsframe, text = "Results", font = ("Arial", 14), fg_color = "transparent")
resultstitle.grid(row = 0, column = 0, columnspan = 5, pady = (8, 6))

CTkLabel(resultsframe, text = "Algorithm").grid(row = 1, column = 0, padx = 4)
CTkLabel(resultsframe, text = "Nodes visited").grid(row = 1, column = 1, padx = 4)
CTkLabel(resultsframe, text = "Path").grid(row = 1, column = 2, padx = 4)
CTkLabel(resultsframe, text = "Time taken").grid(row = 1, column = 3, padx = 4)
CTkLabel(resultsframe, text = "Cost").grid(row = 1, column = 4, padx = 4)

CTkLabel(resultsframe, text = "BFS").grid(row = 2, column = 0, padx = 4)
CTkLabel(resultsframe, text = "Dijkstra's").grid(row = 3, column = 0, padx = 4)
CTkLabel(resultsframe, text = "A*").grid(row = 4, column = 0, padx = 4)

bfsvisit = CTkLabel(resultsframe, text = "-")
bfsvisit.grid(row = 2, column = 1)
bfspath = CTkLabel(resultsframe, text = "-")
bfspath.grid(row = 2, column = 2)
bfstime = CTkLabel(resultsframe, text = "-")
bfstime.grid(row = 2, column = 3)
bfscost = CTkLabel(resultsframe, text = "-")
bfscost.grid(row = 2, column = 4)

dijkvisit = CTkLabel(resultsframe, text = "-")
dijkvisit.grid(row = 3, column = 1)
dijkpath = CTkLabel(resultsframe, text = "-")
dijkpath.grid(row = 3, column = 2)
dijktime = CTkLabel(resultsframe, text = "-")
dijktime.grid(row = 3, column = 3)
dijkcost = CTkLabel(resultsframe, text = "-")
dijkcost.grid(row = 3, column = 4)

avisit = CTkLabel(resultsframe, text = "-")
avisit.grid(row = 4, column = 1)
apath = CTkLabel(resultsframe, text = "-")
apath.grid(row = 4, column = 2)
atime = CTkLabel(resultsframe, text = "-")
atime.grid(row = 4, column = 3)
acost = CTkLabel(resultsframe, text = "-")
acost.grid(row = 4, column = 4)

feedback = CTkLabel(controlpanel, text = "", font = ("Arial", 12), fg_color = "transparent")
feedback.pack(pady = (0,1))

tfeedback = CTkLabel(controlpanel, text = "", font = ("Arial", 12), fg_color = "transparent")
tfeedback.pack(pady = (0,1))

canvas.bind("<B1-Motion>", placecell)
canvas.bind("<Button-1>", placecell)
canvas.bind("<Button-3>", addwall)
canvas.bind("<B3-Motion>", addwall)
canvas.bind("<Button-2>", removewall)
canvas.bind("<B2-Motion>", removewall)
canvas.bind("<Configure>", resizegrid)

window.after_idle(resizegrid)

window.mainloop()
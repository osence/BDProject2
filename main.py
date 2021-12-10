import redis
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

# Подключаем БД
# client = redis.Redis(host='192.168.112.103', password='student')
client = redis.Redis(host='127.0.0.1')


def raise_score(judge, score_increment, sportsman):
    if isfloat(score_increment):
        # Увеличиваем счет на x
        client.zincrby('22305_sergeevs-' + judge, score_increment, sportsman)
        refresh()
    else:
        messagebox.showerror(title="Ошибка", message="Введите число")


def on_closing():
    for key in client.keys():
        if '22305_sergeevs-' in str(key):
            client.delete(key)
    root.destroy()


def refresh():
    treeTable.delete(*treeTable.get_children())

    client.zunionstore(dest="22305_sergeevs-sorevnovanie", keys=lJudgeBD, aggregate='SUM')
    res = client.zrevrange(name="22305_sergeevs-sorevnovanie", start=0, end=-1, withscores=True)

    for r in res:
        treeTable.insert('', 'end', values=[r[0].decode('utf-8'), r[1]])


def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


lSports = []
for i in range(1, 7):
    lSports.append("Спортсмен" + str(i))

lJudge = []
lJudgeBD = []

for i in range(1, 4):
    lJudge.append("Судья" + str(i))
    lJudgeBD.append("22305_sergeevs-Судья" + str(i))

# ---------Основное окно----------
root = tk.Tk()
root.title("BDLab2")
root.geometry("500x400")
root.protocol("WM_DELETE_WINDOW", on_closing)
# -------Список Спортсменов-------
lblSportsman = Label(text="Кому:")
boxSports = ttk.Combobox(root, values=lSports)
boxSports.current(0)
# ----------Список Судей----------
lblJudge = Label(text="От кого:")
boxJudge = ttk.Combobox(root, values=lJudge)
boxJudge.current(0)
# --------Окно ввода очков--------
lblScore = Label(text="Добавить очков:")
entryScore = tk.Entry(root)
# -------Кнопка добавления--------
btnAdd = tk.Button(root, text="OK", width=15,
                   command=lambda: raise_score(boxJudge.get(), entryScore.get(), boxSports.get()))
# --------Окно со списком---------
treeTable = ttk.Treeview(root, show="headings")
treeTable["columns"] = ["sportsman", "score"]
for i in range(0, len(treeTable["columns"]) - 3):
    treeTable.column(treeTable["columns"][i])
treeTable.heading("sportsman", text="Имя", anchor=tk.CENTER)
treeTable.heading("score", text="Общий балл", anchor=tk.CENTER)

# ------------Дизайн-------------
treeTable.place(relx=0.1, rely=0.1, relwidth=0.81)
lblJudge.place(relx=.1, rely=.7, relwidth=0.35)
boxJudge.place(relx=.1, rely=.75, relwidth=0.35)
lblSportsman.place(relx=.56, rely=.7, relwidth=0.35)
boxSports.place(relx=.56, rely=.75, relwidth=0.35)
lblScore.place(relx=.15, rely=.85)
entryScore.place(relx=0.35, rely=0.85, relwidth=0.1)
btnAdd.place(relx=.6, rely=.84, relwidth=0.1)

refresh()

root.mainloop()
client.close()

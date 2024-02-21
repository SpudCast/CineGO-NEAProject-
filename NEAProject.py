import tkinter as tk
from tkinter import *
from tkinter import ttk
import sqlite3 as sq
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import random



class Controller:
    def __init__(self, login, register, home):
        self.login = login
        self.register = register
        self.home = home
        self.Main = self
        self.Page = tk.Tk()
        self.windowGeometry(self.Page, 1000, 600, 'CINEGO')
        self.AccountAccessed = ''
        ttk.Button(self.Page, text="CineGo",command= lambda: self.loadPage(self.Page, self.login, self.Main)).place(relx=0.5, rely=0.5, anchor=CENTER)
        self.Page.mainloop()

    
    def loadPage(self, currentPage, page, Main):
        currentPage.destroy()
        page(Main)

    def windowGeometry(self, window, width, height, title):
        window.title(title)
        window.resizable(False, False)
        window.config(bg='#303030')
        style = ttk.Style(window)
        style.theme_use('clam')
        style.configure("TLabel", font='Minecraft', foreground="#ffffff", background="#303030")
        style.configure("TMenubutton", font='Minecraft', foreground="#ffffff", background="#303030")
        style.configure("TEntry", font='Minecraft', foreground="#000000", background="#303030")
        style.configure("TButton", font='Minecraft', foreground="#ffffff", background="#303030")
        style.configure("TFrame", foreground="#ffffff", background="#303030")
        style.configure("Greyed.TButton", font='Minecraft', foreground="#ff0022", background="#303030")
        screen_height = window.winfo_screenheight()
        screen_width = window.winfo_screenwidth()
        window_center_x = int(screen_width/2 - width / 2)
        window_center_y = int(screen_height/2 - height / 2)

        window.geometry(f'{width}x{height}+{window_center_x}+{window_center_y}')

class LoginPage:
    def __init__(self, Main):
        self.Main = Main
        self.Page = tk.Tk()
        self.Main.windowGeometry(self.Page, 380, 300, 'LOGIN')
        ttk.Label(self.Page, text='Login').grid(column=0, row=0, sticky='W', padx=10, pady=10)

        ttk.Label(self.Page, text='Username').grid(column=0, row=1, sticky='W', pady=10, padx=10)
        self.username = StringVar()
        self.usernameEntry = ttk.Entry(self.Page, textvariable=self.username,width=30).grid(column=1, row=1, sticky='W', pady=10, padx=10)

        ttk.Label(self.Page, text='Password').grid(column=0, row=2, sticky='W', pady=10, padx=10)
        self.password = StringVar()
        self.passwordEntry = ttk.Entry(self.Page, textvariable=self.password,width=30, show='*').grid(column=1, row=2, sticky='W', pady=10, padx=10)
        self.Page.bind('<Return>', lambda event: self.verifyUser(self.username.get(), self.password.get()))

        ttk.Button(self.Page, text='Login', command= lambda: self.verifyUser(self.username.get(), self.password.get())).grid(column=1, row=3, sticky='W', pady=10)
        ttk.Button(self.Page, text='Register', command= lambda: self.Main.loadPage(self.Page, self.Main.register, self.Main)).grid(column=1, row=4, sticky='W', pady=10)
    
    def verifyUser(self, username, password):
        loginDatabase = open("UserInfo.txt", "r")
        enteredLoginInfo = (str(username) + "." + str(password))
        verify = False
        for line in loginDatabase:
            if enteredLoginInfo == line.strip():
                verify = True
                self.Main.AccountAccessed = username
        if verify == True:
            self.Main.loadPage(self.Page, self.Main.home, self.Main)
        else:
            ttk.Label(self.Page, text='Incorrect!, Username Or Password Incorrect', wraplength=70).grid(column=0, row=4, sticky='W', pady=10, padx=10)

class registerPage:
    def __init__(self, Main):
        self.Main = Main
        self.Page = tk.Tk()

        self.con = sq.connect('content.db')
        self.cur = self.con.cursor()

        self.Main.windowGeometry(self.Page, 400, 400, 'REGISTER')

        ttk.Label(self.Page, text='Register').grid(column=0, row=0, sticky='W', padx=10, pady=10)

        ttk.Label(self.Page, text='Username').grid(column=0, row=1, sticky='W', padx=10, pady=10)
        self.username = StringVar()
        self.usernameEntry = ttk.Entry(self.Page, textvariable=self.username,width=30).grid(column=1, row=1, sticky='W', padx=10, pady=10)

        ttk.Label(self.Page, text='Password').grid(column=0, row=2, sticky='W', padx=10, pady=10)
        self.password = StringVar()
        self.passwordEntry = ttk.Entry(self.Page, textvariable=self.password,width=30, show='*').grid(column=1, row=2, sticky='W', padx=10, pady=10)

        self.error = ttk.Label(self.Page, text='')
        self.error.grid(column=1, row=3, sticky='W', padx=10, pady=10)

        ttk.Button(self.Page, text='Register', command= lambda: self.save_register(self.username.get(), self.password.get())).grid(column=1, row=3, sticky='W', padx=10, pady=10)
        ttk.Button(self.Page, text='Login', command= lambda: self.Main.loadPage(self.Page, self.Main.login, self.Main)).grid(column=1, row=4, sticky='W', padx=10, pady=10)

        self.Page.bind('<Return>', lambda event: self.save_register(self.username.get(), self.password.get()))

    def save_register(self, username, password):
        self.saveLoginInfo = (str(username) + "." + str(password))
        self.loginDatabase = open("UserInfo.txt", "r+")
        self.loginDatabase.seek(0)
        for lines in self.loginDatabase:
            if (username + ".") in lines:
                self.error.config(text="Username Already Exists !")
                self.loginDatabase.close()
                return
            elif password == "":
                self.error.config(text= "Please enter a Password")
                self.loginDatabase.close()
                return
            elif len(username) > 20:
                self.error.config(text= "Username is too long!")
                self.loginDatabase.close()
                return
            elif len(password) < 4:
                self.error.config(text= "Password is too short!")
                self.loginDatabase.close()
                return
        with self.con:
            self.cur.execute("INSERT INTO user (username) VALUES (?)",(username,))
        self.loginDatabase.write(self.saveLoginInfo + '\n')
        self.loginDatabase.close()
        self.Main.AccountAccessed = username
        self.Main.loadPage(self.Page, self.Main.home, self.Main)   

class homePage:
    def __init__(self, Main):
        self.Main = Main
        self.Page = tk.Tk()
        self.Main.windowGeometry(self.Page, 1000, 600, 'HOME')

        self.con = sq.connect('content.db')
        self.cur = self.con.cursor()

        self.svc1 = ttk.Button(self.Page, text="Fakeflix", command= lambda: self.filterSvc('Fakeflix')).place(relx=.3, rely=.1, anchor=CENTER)
        self.svc2 = ttk.Button(self.Page, text="Fakezon Prime", command= lambda: self.filterSvc('Fakezon Prime')).place(relx=.5, rely=.1, anchor=CENTER)
        self.svc3 = ttk.Button(self.Page, text="Fake TV+", command= lambda: self.filterSvc('Fake TV+')).place(relx=.7, rely=.1, anchor=CENTER)
        self.curService = 'Fakeflix'

        self.sort = StringVar()
        self.sort.set("oid")
        self.SortDropdown = ttk.OptionMenu(self.Page, self.sort, "Sort", "Year(Asc)", "Year(Desc)", "Score(Asc)", "Score(Desc)", command= lambda event: self.sortFunction()).place(relx=.5, rely=.3, anchor=CENTER)
        
        self.mvFrame = ttk.Frame(self.Page)
        self.mvFrame.place(relx=.5, rely=.5, anchor=CENTER)

        self.mv1 = ttk.Button(self.mvFrame,command= lambda: self.previewWindow(self.mv1.cget('text')))
        self.mv1.pack(side= LEFT, padx=5)
        self.mv2 = ttk.Button(self.mvFrame,command= lambda: self.previewWindow(self.mv2.cget('text')))
        self.mv2.pack(side= LEFT, padx=5)
        self.mv3 = ttk.Button(self.mvFrame,command= lambda: self.previewWindow(self.mv3.cget('text')))
        self.mv3.pack(side= LEFT, padx=5)
        self.mv4 = ttk.Button(self.mvFrame,command= lambda: self.previewWindow(self.mv4.cget('text')))
        self.mv4.pack(side= LEFT, padx=5)
        self.mv5 = ttk.Button(self.mvFrame,command= lambda: self.previewWindow(self.mv5.cget('text')))
        self.mv5.pack(side= LEFT, padx=5)
        self.mv6 = ttk.Button(self.mvFrame,command= lambda: self.previewWindow(self.mv6.cget('text')))
        self.mv6.pack(side= LEFT, padx=5)
        self.mv7 = ttk.Button(self.mvFrame,command= lambda: self.previewWindow(self.mv7.cget('text')))
        self.mv7.pack(side= LEFT, padx=5)
        self.Nmv = [self.mv1, self.mv2, self.mv3, self.mv4, self.mv5, self.mv6, self.mv7]

        self.RecommendationButton = ttk.Button(self.Page, text='Get Recommendations', command=self.getRecommendations)
        self.RecommendationButton.place(relx=.5, rely=.8, anchor=CENTER)

        self.search = StringVar()
        self.searchBar = ttk.Entry(self.Page, textvariable=self.search, width=100)
        self.searchBar.place(rely=.9, relx=.5, anchor=CENTER)
        self.searchBar.bind('<Return>', lambda event: self.searchResult(self.search.get()))


    def searchResult(self, Keyword):
        self.Result = tk.Tk()
        self.Keyword = Keyword

        self.Main.windowGeometry(self.Result, 400, 400, self.Keyword)
        
        self.Keyword = ("%" + self.Keyword + "%")
        self.resultsList = []
        self.searchButtons = []
        with self.con:
            self.temp = self.cur.execute("SELECT title FROM content WHERE title LIKE ?", (self.Keyword, ))
            self.temp = self.cur.fetchall()
            self.cur.execute("SELECT title FROM content WHERE title LIKE ?", (self.Keyword, ))
            print('\n\n\n\n\n\n\n', self.temp)
            for x in range(len(self.temp)):
                self.outputPlace = []
                self.outputPlace = self.cur.fetchone()
                self.resultsList.append(self.outputPlace[0])
            for n in range(len(self.resultsList)):
                self.searchButtons.append(ttk.Button(self.Result, text=self.resultsList[n]))
                self.searchButtons[n].config(command= lambda n=n: self.previewWindow(self.searchButtons[n].cget('text')))
                self.searchButtons[n].pack(pady = 10)

    def sortFunction(self):
        option = self.sort.get()
        with self.con:
            match option:
                case "Year(Desc)":
                    contentName = [title[0] for title in self.cur.execute("SELECT title FROM content WHERE service=? ORDER BY year DESC", (self.curService,))]
                    for i in range (0, 7):
                        self.Nmv[i].config(text=contentName[i], style="TButton")
                case "Year(Asc)":
                    contentName = [title[0] for title in self.cur.execute("SELECT title FROM content WHERE service=? ORDER BY year ASC", (self.curService,))]
                    for d in range (0, 7):
                        self.Nmv[d].config(text=contentName[d], style="TButton")
                case "Score(Desc)":
                    contentName = [title[0] for title in self.cur.execute("SELECT title FROM content WHERE service=? ORDER BY score DESC", (self.curService,))]
                    for x in range (0, 7):
                        self.Nmv[x].config(text=contentName[x], style="TButton")
                case "Score(Asc)":
                    contentName = [title[0] for title in self.cur.execute("SELECT title FROM content WHERE service=? ORDER BY score ASC", (self.curService,))]
                    for e in range (0, 7):
                        self.Nmv[e].config(text=contentName[e], style="TButton")
                
    def previewWindow(self, content):
        self.Preview = tk.Tk()
        self.Main.windowGeometry(self.Preview, 400, 400, content)
        self.content_id = ''
        with self.con:
            self.cur.execute("SELECT * FROM content WHERE title = ?", (content,))
            temp = self.cur.fetchone()
            self.content_id = temp[0]
            self.Name = ttk.Label(self.Preview, text=temp[1], font=('Minecraft', 30))
            self.Year = ttk.Label(self.Preview, text=temp[2], font=('Minecraft', 30))
            self.Rating = ttk.Label(self.Preview, text=temp[4], font=('Minecraft', 30))
            self.Genre = ttk.Label(self.Preview, text=temp[5], font=('Minecraft', 30))
            self.Service = ttk.Label(self.Preview, text=temp[6], font=('Minecraft', 30))
            self.Type = ttk.Label(self.Preview, text=temp[7], font=('Minecraft', 30))
        self.Name.pack(pady= 10)
        self.Year.pack(pady= 10)
        self.Rating.pack(pady= 10)
        self.Genre.pack(pady= 10)
        self.Service.pack(pady= 10)
        self.Type.pack(pady= 10)

        self.watchedButton = ttk.Button(self.Preview, text="Watched", command=lambda: self.writeWatched(self.content_id), state=NORMAL)
        self.watchedButton.pack()

        with self.con:
            self.content_watched = []
            self.cur.execute("SELECT content FROM contentWatched WHERE username=?", (self.Main.AccountAccessed,))
            temp = self.cur.fetchall()
            self.cur.execute("SELECT content FROM contentWatched WHERE username=?", (self.Main.AccountAccessed,))
            for i in range(len(temp)):
                temp1 = self.cur.fetchone()
                self.content_watched.append(temp1[0])
                
            if self.content_id in self.content_watched:
                print("\n\n\n", self.content_id)
                self.watchedButton.config(state=DISABLED)
            else:
                print("\n\n\n:)", self.content_id)
                self.watchedButton.config(state=NORMAL)
    
    def writeWatched(self, contentID):
        with self.con:
            self.cur.execute("""INSERT OR IGNORE INTO contentWatched(
            username,
            content
            ) 
            VALUES 
            (?, ?)
            """, 
            (self.Main.AccountAccessed, contentID))
        self.Preview.destroy()
            

    def filterSvc(self, service):
        with self.con:
            self.curService = service
            contentName = [title[0] for title in self.cur.execute("SELECT title FROM content WHERE service=?", (self.curService,))]
            for i in range (0, 7):
                self.Nmv[i].config(text=contentName[i], style="TButton")

    def getRecommendations(self):
        self.Inputs = []
        self.randomOutput = []
        with self.con:
            self.content_watched = []
            self.cur.execute("SELECT content FROM contentWatched WHERE username=?", (self.Main.AccountAccessed,))
            temp = self.cur.fetchall()
            self.cur.execute("SELECT content FROM contentWatched WHERE username=?", (self.Main.AccountAccessed,))
            for i in range(len(temp)):
                temp1 = self.cur.fetchone()
                self.content_watched.append(temp1[0])

            for i in range(len(self.content_watched)):
                self.cur.execute("SELECT title FROM content WHERE content_id=?", (self.content_watched[i],))
                temp = self.cur.fetchone()
                self.Inputs.append(temp[0])

        for i in range(len(self.Inputs)):
            self.Inputs[i] = self.cleanText(self.Inputs[i])

        self.OutputList = self.generate_recommendations(self.Inputs)
        with self.con:
            self.numWatched = self.cur.execute("SELECT content FROM contentwatched WHERE username=?", (self.Main.AccountAccessed, ))
            self.numWatched = len(self.numWatched.fetchall())
            if self.numWatched < 8:
                contentName = [title[0] for title in self.cur.execute("SELECT title FROM content ORDER BY oid")]
                for e in range(0, 7):
                    self.Nmv[e].config(text=contentName[e], style="TButton")
            else:
                while len(self.randomOutput) < 9:
                    x = random.randint(1, (len(self.OutputList) -1))
                    if x not in self.randomOutput:
                        self.randomOutput.append(x)
                for i in range(7):
                    y = self.randomOutput[i]
                    try:
                        self.cur.execute('SELECT title FROM content WHERE content_id=? AND service=?', (self.OutputList[y],self.curService,))
                        temp = self.cur.fetchone()
                        temp = temp[0]
                        self.Nmv[i].config(text=temp, style="TButton")
                    except:
                        self.cur.execute('SELECT title FROM content WHERE content_id=?', (self.OutputList[y],))
                        temp = self.cur.fetchone()
                        temp = temp[0]
                        self.Nmv[i].configure(text=temp, style="Greyed.TButton")

    def cleanText(self, title):
            result = str(title).lower()
            return result.replace(' ', '')
    
    def generate_recommendations(self, inputs, num_recommendations=1):
    
        df = pd.read_csv('content.csv')
        # Clean up data
        df['title'] = df['title'].apply(self.cleanText)
        df['genre'] = df['genre'].str.lower()
        df['year'] = df['year'].astype(str).str.lower()
        df['service'] = df['service'].apply(self.cleanText)
        df['type'] = df['type'].str.lower()
        df['rating'] = df['rating'].str.lower()

        df2 = df.drop(['score'], axis=1)
        df2['data'] = df2[df2.columns[1:]].apply(lambda x: ' '.join(x.dropna().astype(str)), axis=1)

        # Initialize CountVectorizer and transform data
        vectorizer = CountVectorizer()
        vectorized = vectorizer.fit_transform(df2['data'])

        # Calculate Cosine similarity
        similarities = cosine_similarity(vectorized)

        # Create DataFrame with similarities
        similarity_df = pd.DataFrame(similarities, columns=df['title'], index=df['title']).reset_index()

        # Initialize an empty DataFrame for recommendations
        recommendations_df = []
        # print("\n\n\n\n\n\nDataFrame Columns:", similarity_df.columns)
        # For each input add to list recommendations
        for inputContent in inputs:
            recommendations = similarity_df.nlargest(num_recommendations, inputContent)['title']
            recommendationsText = str(recommendations)
            recommendationsText = recommendationsText.split(' ', 1)[0]
            recommendations_df.append(recommendationsText)
        return recommendations_df
    



if __name__ == '__main__':
    start = Controller(LoginPage, registerPage, homePage)
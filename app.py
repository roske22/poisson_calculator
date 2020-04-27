from tkinter import *
from tkinter import ttk
import pandas as pd
import numpy as np
from scipy.stats import poisson
import statsmodels.api as sm
import statsmodels.formula.api as smf
import sqlite3


class MainApp:

    def __init__(self, root):

        self.frame_header = ttk.Frame(root)
        self.frame_header.grid(row=0, column=0)

        # title
        root.title('Titanium')
        root.resizable(False, False)

        self.frame1 = Frame(root)
        self.frame1.grid(row=0, column=0)

        # Image
        self.img = PhotoImage(file='/Users/apple/Desktop/poisson/logo/logo.gif')
        self.logo = Label(self.frame1, image=self.img)
        self.logo.grid(row=0, column=0, rowspan=4, sticky=W + E + N + S, padx=5, pady=5)

        # label 0
        label = ttk.Label(self.frame1, text='Please choose a league')
        label.grid(row=0, column=2)

        # Drop down league
        self.league = StringVar()
        self.leagueCombobox = ttk.Combobox(self.frame1, textvariable=self.league, state='readonly')
        self.leagueCombobox.config(width=19, font=('Helvetica'))
        self.leagueCombobox.grid(row=1, column=2)
        self.leagueCombobox.config(values=self.leagueList())

        # Home team label
        homeLabel = ttk.Label(self.frame1, text='Home team')
        homeLabel.grid(row=1, column=1)
        self.homeTeamCombobox = ttk.Combobox(self.frame1, state='disable')
        self.homeTeamCombobox.config(width=15, font=('Helvetica'))
        self.homeTeamCombobox.grid(row=2, column=1)

        # Away team label
        awayLabel = ttk.Label(self.frame1, text='Away team')
        awayLabel.grid(row=1, column=3)
        self.awayTeamCombobox = ttk.Combobox(self.frame1, state='disable')
        self.awayTeamCombobox.config(width=15, font=('Helvetica'))
        self.awayTeamCombobox.grid(row=2, column=3)

        # submit button
        ttk.Button(self.frame1, width=12, text='Submit', command=self.twoFunction).grid(row=7, column=2)

        self.labelVS = Label(self.frame1, text="VS", relief="groove", width=15)
        self.labelVS.grid(row=2, column=2)

        # Home team odd label
        self.label1 = Label(self.frame1, text="1", relief="groove", width=15)
        self.label1.grid(row=3, column=1)

        # Drawe odd label
        self.labelX = Label(self.frame1, text="X", relief="groove", width=15)
        self.labelX.grid(row=3, column=2)

        # Away team label
        self.label2 = Label(self.frame1, text="2", relief="groove", width=15)
        self.label2.grid(row=3, column=3)

        # Home entry
        self.homeOddEntry = Entry(self.frame1, relief="groove", width=15, justify='center')
        self.homeOddEntry.grid(row=4, column=1)

        # draw entry
        self.drawOddEntry = Entry(self.frame1, relief="groove", width=15, justify='center')
        self.drawOddEntry.grid(row=4, column=2)

        # away entry
        self.awayOddEntry = Entry(self.frame1, relief="groove", width=15, justify='center')
        self.awayOddEntry.grid(row=4, column=3)

        self.homePredictedLabel = Label(self.frame1, text="", width=15)
        self.homePredictedLabel.grid(row=6, column=1)

        self.drawPredictedLabel = Label(self.frame1, text="", width=15)
        self.drawPredictedLabel.grid(row=6, column=2)

        self.awayPredictedLabel = Label(self.frame1, text="", width=15)
        self.awayPredictedLabel.grid(row=6, column=3)

        self.label10 = Label(self.frame1, text="Enter given odds: ", relief="groove", width=15, anchor="e")
        self.label10.grid(row=4, column=0)

        self.label11 = Label(self.frame1, text="No bias odds: ", relief="groove", width=15, anchor="e")
        self.label11.grid(row=5, column=0)

        self.label12 = Label(self.frame1, text="Predicted odds: ", relief="groove", width=15, anchor="e")
        self.label12.grid(row=6, column=0)

        self.homeTrueOdds = Label(self.frame1, text="", width=15)
        self.homeTrueOdds.grid(row=5, column=1)

        self.drawTrueOdds = Label(self.frame1, text="", width=15)
        self.drawTrueOdds.grid(row=5, column=2)

        self.awayTrueOdds = Label(self.frame1, text="", width=15)
        self.awayTrueOdds.grid(row=5, column=3)

        # % label
        self.percentLabel = Label(self.frame1, text="", width=15)
        self.percentLabel.grid(row=7, column=1)

        # Bias label
        self.label17 = Label(self.frame1, text="Bias: ", relief="groove", width=15, anchor="e")
        self.label17.grid(row=7, column=0)

        self.leagueCombobox.bind("<<ComboboxSelected>>", self.getVal)

    # function for showing leagues in combobox
    def leagueList(self):
        conn = sqlite3.connect('league.db')
        c = conn.cursor()
        league = c.execute('SELECT league FROM leagues')
        listLeague = []
        for x in league:
            for y in x:
                listLeague.append(y)
        return listLeague

    # function for predicting real odds
    def trueOdds(self):
        h = self.homeOddEntry.get()
        d = self.drawOddEntry.get()
        a = self.awayOddEntry.get()
        z = round(((1 / float(h)) * 100 + (1 / float(d)) * 100 + (1 / float(a)) * 100) - 100, 2)
        self.homeTrueOdds.config(text=round((z / 100 + 1) * float(h), 3))
        self.drawTrueOdds.config(text=round((z / 100 + 1) * float(d), 3))
        self.awayTrueOdds.config(text=round((z / 100 + 1) * float(a), 3))
        self.percentLabel.config(text='{} %'.format(z))

    # function for calling two function
    def twoFunction(self):
        if len(self.homeOddEntry.get()) == 0 or len(self.drawOddEntry.get()) == 0 or len(self.awayOddEntry.get()) == 0:
            self.poissonCal(self.getLeague(), self.homeTeamCombobox.get(), self.awayTeamCombobox.get())
        else:
            self.trueOdds()
            self.poissonCal(self.getLeague(), self.homeTeamCombobox.get(), self.awayTeamCombobox.get())

    # Function for listing all team from league
    def unique(self):
        conn = sqlite3.connect('league.db')
        c = conn.cursor()
        team = c.execute('SELECT DISTINCT HomeTeam FROM {}'.format(self.getLeague()))
        lista = []
        for x in team:
            for y in x:
                lista.append(y)
        lista.sort()
        return lista

    # Function for putting correct team in drop down menu by league
    def getVal(self, event):
        self.home = StringVar()
        self.away = StringVar()
        self.homeTeamCombobox.config(value=self.unique(), state='readonly', textvariable=self.home)
        self.awayTeamCombobox.config(value=self.unique(), state='readonly', textvariable=self.away)

    # function to return league without space
    def getLeague(self):
        self.x = self.leagueCombobox.get()
        return self.x.replace(' ', '')

    # poisson function
    def poissonCal(self, league, home, away):
        conn = sqlite3.connect('league.db')
        sql_query = pd.read_sql_query('SELECT HomeTeam, AwayTeam, FTHG, FTAG FROM {}'.format(league), conn)
        try:
            epl_1617 = pd.DataFrame(sql_query, columns=['HomeTeam', 'AwayTeam', 'FTHG', 'FTAG'])

            goal_model_data = pd.concat([epl_1617[['HomeTeam', 'AwayTeam', 'FTHG']].assign(home=1).rename(
                columns={'HomeTeam': 'team', 'AwayTeam': 'opponent', 'FTHG': 'goals'}),
                epl_1617[['AwayTeam', 'HomeTeam', 'FTAG']].assign(home=0).rename(
                    columns={'AwayTeam': 'team', 'HomeTeam': 'opponent', 'FTAG': 'goals'})])

            poisson_model = smf.glm(formula="goals ~ home + team + opponent", data=goal_model_data,
                                    family=sm.families.Poisson()).fit()

            # print(poisson_model.summary())

            def simulate_match(foot_model, homeTeam, awayTeam, max_goals=10):
                home_goals_avg = foot_model.predict(pd.DataFrame(data={'team': homeTeam,
                                                                       'opponent': awayTeam, 'home': 1},
                                                                 index=[1])).values[0]
                away_goals_avg = foot_model.predict(pd.DataFrame(data={'team': awayTeam,
                                                                       'opponent': homeTeam, 'home': 0},
                                                                 index=[1])).values[0]
                team_pred = [[poisson.pmf(i, team_avg) for i in range(0, max_goals + 1)] for team_avg in
                             [home_goals_avg, away_goals_avg]]
                return np.outer(np.array(team_pred[0]), np.array(team_pred[1]))

            match = simulate_match(poisson_model, home, away, max_goals=10)
            self.homePredictedLabel.config(text=round(1 / np.sum(np.tril(match, -1)), 2))
            self.drawPredictedLabel.config(text=round(1 / np.sum(np.diag(match)), 2))
            self.awayPredictedLabel.config(text=round(1 / np.sum(np.triu(match, 1)), 2))

            h = self.homeOddEntry.get()
            d = self.drawOddEntry.get()
            a = self.awayOddEntry.get()
            try:
                if float(h) > round(1 / np.sum(np.tril(match, -1)), 2):
                    self.homePredictedLabel.config(bg='green')
                else:
                    self.homePredictedLabel.config(bg='red')

                if float(d) > round(1 / np.sum(np.diag(match)), 2):
                    self.drawPredictedLabel.config(bg='green')
                else:
                    self.drawPredictedLabel.config(bg='red')

                if float(a) > round(1 / np.sum(np.triu(match, 1)), 2):
                    self.awayPredictedLabel.config(bg='green')
                else:
                    self.awayPredictedLabel.config(bg='red')
            except ValueError:
                pass
            conn.commit()
            conn.close()
        except FileNotFoundError:
            pass


def main():
    master = Tk()
    app = MainApp(master)
    master.mainloop()


if __name__ == '__main__': main()

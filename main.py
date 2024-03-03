import requests
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import statsmodels as statsmodels


class CurrencyConverterGUI:
    def __init__(self):
        self.myapp = tk.Tk()
        self.currency_label = tk.Label(text='Wybierz walutę: ')
        self.combobox = ttk.Combobox(self.myapp, textvariable=tk.StringVar())
        self.combobox['values'] = ('bat (Tajlandia)',
                                   'dolar amerykański',
                                   'dolar australijski',
                                   'dolar Hongkongu',
                                   'dolar kanadyjski',
                                   'dolar nowozelandzki',
                                   'dolar singapurski',
                                   'euro')
        self.combobox_dates = ttk.Combobox(self.myapp, textvariable=tk.StringVar())
        self.combobox_dates['values'] = ('THB', 'USD', 'AUD', 'HKD', 'CAD', 'NZD', 'SGD', 'EUR')
        self.combobox_trend = ttk.Combobox(self.myapp, textvariable=tk.StringVar())
        self.combobox_trend['values'] = ('THB', 'USD', 'AUD', 'HKD', 'CAD', 'NZD', 'SGD', 'EUR')
        self.quantity_label = tk.Label(text='Podaj ilość: ')
        self.quantity_entry = tk.Entry(width=15)
        self.code_label = tk.Label(text='Wybierz walutę: ')
        self.startDate_label = tk.Label(text='Podaj datę początkową w formacie RRRR-MM-DD:* ')
        self.startDate_entry = tk.Entry(width=20)
        self.endDate_label = tk.Label(text='Podaj datę końcową w formacie RRRR-MM-DD:** ')
        self.endDate_entry = tk.Entry(width=20)
        self.currency_trend_label = tk.Label(text='Wybierz walutę: ')
        self.rates_number_label = tk.Label(text='Podaj ilość dni:*** ')
        self.rates_number_entry = tk.Entry(width=15)
        self.conditions = tk.Label(text='* Dane dostępne od 2 stycznia 2002 r.')
        self.conditions1 = tk.Label(text='** Maksymalna różnica: 367 dni')
        self.conditions2 = tk.Label(text='*** Maksymalna długość: 255 dni')

        self.currency_label.grid(column=0, row=0, sticky=tk.W, pady=2)
        self.combobox.grid(column=1, row=0, sticky=tk.W, pady=2)
        self.quantity_label.grid(column=0, row=1, sticky=tk.W, pady=2)
        self.quantity_entry.grid(column=1, row=1, sticky=tk.W, pady=2)
        self.code_label.grid(column=2, row=0, sticky=tk.W, pady=2)
        self.combobox_dates.grid(column=3, row=0, sticky=tk.W, pady=2)
        self.startDate_label.grid(column=2, row=1, sticky=tk.W, pady=2)
        self.startDate_entry.grid(column=3, row=1, sticky=tk.W, pady=2)
        self.endDate_label.grid(column=2, row=2, sticky=tk.W, pady=2)
        self.endDate_entry.grid(column=3, row=2, sticky=tk.W, pady=2)
        self.currency_trend_label.grid(column=4, row=0, sticky=tk.W, pady=2)
        self.combobox_trend.grid(column=5, row=0, sticky=tk.W, pady=2)
        self.rates_number_label.grid(column=4, row=1, sticky=tk.W, pady=2)
        self.rates_number_entry.grid(column=5, row=1, sticky=tk.W, pady=2)
        self.conditions.grid(row=4, sticky=tk.W)
        self.conditions1.grid(row=5, sticky=tk.W)
        self.conditions2.grid(row=6, sticky=tk.W)

        self.doing_button = tk.Button(text='Przelicz', command=self.change)
        self.date_button = tk.Button(text='Narysuj wykres', command=self.wykres)
        self.quit_button = tk.Button(text='Zakończ', command=self.myapp.destroy)
        self.trend_button = tk.Button(text='Przedstaw linię trendu.', command=self.linia_trendu)

        self.doing_button.grid(column=0, row=2, sticky=tk.W)
        self.date_button.grid(column=2, row=3, sticky=tk.W)
        self.quit_button.grid(column=5, row=6, sticky=tk.E)
        self.trend_button.grid(column=4, row=2, sticky=tk.W)

        # Wejście do pętli głównej tkinter
        tk.mainloop()

    def change(self):
        body = requests.get('http://api.nbp.pl/api/exchangerates/tables/A/')
        response = body.json()
        currency = self.combobox.get()
        quantity = float(self.quantity_entry.get())
        for rates in response[0]['rates']:
            if currency == rates['currency']:
                result = quantity * float(rates['mid'])
                tk.messagebox.showinfo('Zatem otrzymasz:', str(result))

    def dates2(self):
        dates2_array = []
        code = self.combobox_dates.get()
        start_date = self.startDate_entry.get()
        end_date = self.endDate_entry.get()
        adres_dates2 = f"http://api.nbp.pl/api/exchangerates/rates/A/{code}/{start_date}/{end_date}/"
        body_dates2 = requests.get(adres_dates2)
        response_dates2 = body_dates2.json()
        if code == response_dates2['code']:
            for i in range(len(response_dates2["rates"])):
                date = response_dates2["rates"][i]["effectiveDate"]
                dates2_array.append(date)
        dates2_array = pd.to_datetime(dates2_array, format='%Y-%m-%d')
        return dates2_array

    def values2(self):
        values2_array = []
        code = self.combobox_dates.get()
        start_date = self.startDate_entry.get()
        end_date = self.endDate_entry.get()
        adres_values2 = f"http://api.nbp.pl/api/exchangerates/rates/A/{code}/{start_date}/{end_date}/"
        body_values2 = requests.get(adres_values2)
        response_values2 = body_values2.json()
        if code == response_values2['code']:
            for i in range(len(response_values2["rates"])):
                value2 = response_values2["rates"][i]["mid"]
                values2_array.append(value2)
            return values2_array

    def wykres(self):
        plt.figure()
        plt.xlabel('Daty', fontsize=16)
        plt.plot(self.dates2(), self.values2())
        mng = plt.get_current_fig_manager()
        mng.window.state('zoomed')
        plt.show()

    def linia_trendu(self):
        rates_number = int(self.rates_number_entry.get())
        currency_trend = self.combobox_trend.get()
        dates_array = []
        adresdate = f"http://api.nbp.pl/api/exchangerates/rates/A/{currency_trend}/last/{rates_number}/"
        bodydate = requests.get(adresdate)
        responsedate = bodydate.json()
        if currency_trend == responsedate['code']:
            for i in range(0, rates_number):
                date = responsedate["rates"][i]["effectiveDate"]
                dates_array.append(date)

        values_array = []
        adresvalue = f"http://api.nbp.pl/api/exchangerates/rates/A/{currency_trend}/last/{rates_number}/"
        bodyvalue = requests.get(adresvalue)
        responsevalue = bodyvalue.json()
        if currency_trend == responsevalue['code']:
            for i in range(0, rates_number):
                value = responsevalue["rates"][i]["mid"]
                values_array.append(value)

        time = []
        for i in range(1, rates_number + 1):
            time.append(i)

        df = px.data.tips()
        fig = px.scatter(df, x=time, y=values_array, trendline="lowess", trendline_options=dict(frac=0.1))
        fig.show()


# Utworzenie egzemplarza klasy CurrencyConverterGUI.
currency_conv = CurrencyConverterGUI()

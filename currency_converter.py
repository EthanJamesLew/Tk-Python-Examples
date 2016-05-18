import urllib.request
import sys
import tkinter as tk
from tkinter.ttk import *

class Currency:
    def __init__(self):
        self.rates = {}
        self.updateRates()
    
    def updateRates(self):
        try:
            date = "Unknown"

            fh = urllib.request.urlopen("http://www.bankofcanada.ca/en/markets/csv/exchange_eng.csv")

            for line in fh:
                line = line.rstrip()
                if not line or line.startswith((b'#',b"Closing")):
                    continue

                fields = line.split(b",")
                if line.startswith(b"Date"):
                    date = fields[-1]

                else:
                    try:
                        value = float(fields[-1])
                        self.rates[(fields[0].decode("utf-8"))]= float(value)
                    except ValueError:
                        pass
            return
        except:
            return "Failed to download:\n" , sys.exc_info()[0]

    def getCurrencies(self):
        return sorted([key for key in self.rates])

class Currency_GUI(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.cur = Currency()

        root.wm_title("Converter v1.0")

        labto = tk.Label(root, text="To:")
        labfrom = tk.Label(root, text="From:")
        
        label1 = tk.Label(root, text="Available Currencies")
        
        self.currencies = Combobox(root)
        self.currencies['values'] = self.cur.getCurrencies()

        label2 = tk.Label(root, text="Amount")
        self.amountIn = tk.Entry(root)

        label3 = tk.Label(root, text="Available Currencies")

        self.currenciesOut = Combobox(root)
        self.currenciesOut['values'] = self.cur.getCurrencies()

        label4 = tk.Label(root, text="Amount")
        self.amountOut = tk.Entry(root)

        ##Pack
        labto.grid(row=0, column=0, padx=10)
        label1.grid(row=1, column=0, padx=10)
        self.currencies.grid(row=2, column=0, padx=10)
        label2.grid(row=1, column=1, padx=10)
        self.amountIn.grid(row=2, column=1, padx=10)

        labfrom.grid(row=3, column=0, padx=10)
        label3.grid(row=4, column=0, padx=10)
        self.currenciesOut.grid(row=5, column=0, padx=10)
        label4.grid(row=4, column=1, padx=10)
        self.amountOut.grid(row=5, column=1, padx=10)

        ##Bindings
        self.currencies.bind('<<ComboboxSelected>>', self.updateConversion)
        self.currencies.bind('<FocusIn>', self.updateConversion)
        
        self.currenciesOut.bind('<<ComboboxSelected>>', self.updateConversion)
        self.currenciesOut.bind('<FocusIn>', self.updateConversion)

        self.amountIn.bind('<Key>', self.updateConversion)

        root.bind('<Enter>', self.updateConversion)
        

    def updateConversion(self, event=None):
        try:
            self.amountOut.delete(0,tk.END)
            amount = (self.cur.rates[self.currenciesOut.get()]/self.cur.rates[self.currencies.get()])*float(self.amountIn.get())
            amount = round(amount, 2)
            self.amountOut.insert(tk.END, amount)
        except:
            return
        
if __name__=="__main__":
    cur = Currency()
    root = tk.Tk()
    Currency_GUI(root).grid(row=0, column=0)
    root.mainloop()
                

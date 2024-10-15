from opensky_api import OpenSkyApi
from datetime import datetime, timedelta
import requests
import pandas as pd


api = OpenSkyApi()
start_timestamp = int((datetime.now() - timedelta(hours=2)).timestamp())
end_timestamp = int(datetime.now().timestamp())
#flights = api.get_flights_from_interval(start_timestamp, end_timestamp)
#for flight in flights:
#    print(flight)


#df1 = pd.read_csv('Data/flights.csv')

#df2 = pd.read_csv('Data/aircrafts.csv')

#result = df2[df2['icao24'].isin(df1['icao'])]['model']
#print(result)

if 1 == 2:
    df2['CO2perkm'] = df2['model'].apply(lambda x: 
                                        (1.9 if '737' in x else 
                                        3.5 if '747' in x else
                                        3.5 if 'A330' in x else
                                        4.0 if '777' in x else
                                        2.2 if 'A320' in x else
                                        3.0 if '787' in x else
                                        1.7 if 'A319' in x else
                                        2.1 if 'A321' in x else
                                        2.6 if 'A350' in x else
                                        3.8 if '767' in x else
                                        3.2 if '757' in x else
                                        3) if isinstance(x, str) else 3)
    

#for index, row in df2.iterrows():
#    model_type = row['model']
#    if not isinstance(model_type, str):
#        print(f"Ligne {index}: Type de 'model' = {model_type}")

import tkinter as tk
from tkinter import messagebox
import numpy as np


def get_airlines():
    """Récupérer la liste unique des compagnies aériennes."""
    result = pd.read_csv('Data/aircrafts.csv')
    airlines = result['operator'].unique()
    return airlines

def evaluate_co2_emissions():
    """Évaluer et afficher les émissions de CO2 pour la compagnie sélectionnée."""
    selected_airline = airline_var.get()
    if selected_airline == "Select an airline":
        messagebox.showwarning("Attention", "Select an airline")
        return
    
    total_co2 = np.random.randint(10)
    messagebox.showinfo("CO2 Emissions", f"Total CO2 emissions for {selected_airline}: {total_co2} kg")

def close_application():
    """Fermer l'application."""
    root.quit()

# Interface utilisateur avec Tkinter
root = tk.Tk()
root.title("Airline CO2 Emissions Evaluator")

# Variable pour stocker la compagnie sélectionnée
airline_var = tk.StringVar()
airline_var.set("Select an airline")

# Récupération des compagnies aériennes depuis la base de données
airlines = get_airlines()

# Menu déroulant pour sélectionner la compagnie aérienne
dropdown = tk.OptionMenu(root, airline_var, *airlines)
dropdown.pack(pady=10)

# Bouton pour évaluer les émissions de CO2
evaluate_button = tk.Button(root, text="Evaluate past CO2 emissions", command=evaluate_co2_emissions)
evaluate_button.pack(pady=10)

# Bouton pour quitter l'application
exit_button = tk.Button(root, text="Exit", command=close_application)
exit_button.pack(pady=10)

# Lancement de l'interface
root.mainloop()

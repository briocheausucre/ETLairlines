import tkinter as tk
from tkinter import messagebox
from sqlalchemy import create_engine, text


if __name__ == "__main__":
    db_url = 'postgresql://astel:Lexanahoj1972!@localhost:5432/airlife'
    engine = create_engine(db_url)

    def get_airlines():
        """Récupérer la liste unique des compagnies aériennes."""
        query = "SELECT DISTINCT operator FROM aircrafts"
        with engine.connect() as conn:
            result = conn.execute(text(query)).mappings() 
            airlines = [row['operator'] for row in result]
        return airlines

    def evaluate_co2_emissions():
        """Évaluer et afficher les émissions de CO2 pour la compagnie sélectionnée."""
        selected_airline = airline_var.get()
        if selected_airline == "Select an airline":
            messagebox.showwarning("Attention", "Select an airline")
            return
        
        query = """
            SELECT SUM("kgCO2") as total_co2
            FROM aircrafts a
            JOIN flights f ON a.icao24 = f.icao
            WHERE a.operator = :operator
        """
        
        with engine.connect() as conn:
            result = conn.execute(text(query), {'operator': selected_airline}).mappings().fetchone()
            total_co2 = result['total_co2'] if result['total_co2'] else 0
        
        messagebox.showinfo("CO2 Emissions", f"Total CO2 emissions for {selected_airline}: {total_co2} kg")

    def close_application():
        """Fermer l'application."""
        root.quit()

    root = tk.Tk()
    root.title("Airline CO2 Emissions Evaluator")
    
    airline_var = tk.StringVar()
    airline_var.set("Select an airline")
    airlines = get_airlines()

    dropdown = tk.OptionMenu(root, airline_var, *airlines)
    dropdown.pack(pady=10)

    evaluate_button = tk.Button(root, text="Evaluate past CO2 emissions", command=evaluate_co2_emissions)
    evaluate_button.pack(pady=10)

    exit_button = tk.Button(root, text="Exit", command=close_application)
    exit_button.pack(pady=10)

    root.mainloop()
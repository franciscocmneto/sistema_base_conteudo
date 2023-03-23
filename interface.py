import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from processing import processing

class RecommendationSystemGUI:
    def __init__(self, master):
        self.master = master
        master.title("Sistema de Recomendação de livros")
        master.configure(bg='#f0f0f0')

        input_frame = ttk.Frame(master, padding=20)
        input_frame.pack(fill="both", expand=True)

        result_frame = ttk.Frame(master, padding=20)
        result_frame.pack(fill="both", expand=True)

        input_label = ttk.Label(input_frame, text="Insira seu livro preferido:")
        input_label.pack(pady=5)

        self.entry = ttk.Entry(input_frame)
        self.entry.pack(pady=5)

        submit_button = ttk.Button(input_frame, text="Submeter", command=self.get_recommendation)
        submit_button.pack(pady=5)

        self.clear_button = ttk.Button(input_frame, text="Limpar", command=self.clear_entry)
        self.clear_button.pack(pady=5)

        self.recommendation_label = ttk.Label(result_frame, text="")
        self.recommendation_label.pack()

        self.scrollbar = ttk.Scrollbar(result_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(result_frame, height=10, width=50, yscrollcommand=self.scrollbar.set)
        self.listbox.pack(pady=5)

        self.save_button = ttk.Button(result_frame, text="Salvar em um arquivo", command=self.save_recommendation)
        self.save_button.pack(pady=5)

        self.scrollbar.config(command=self.listbox.yview)

    def get_recommendation(self):
        # Aqui você pode adicionar seu código de recomendação
        preferences = self.entry.get()
        #string de entrada para a chamada de recomendacoes
        
        if preferences == "":
            messagebox.showerror("Error", "Adicione um parametro valido")
            return

        list_recommendation = processing(preferences)

        if list_recommendation == 0:
            messagebox.showerror("Error", "Adicione um parametro valido")
            return
        else:
            recommendation = tuple(list_recommendation)
            
        self.listbox.delete(0, tk.END)

        for item in recommendation:
            self.listbox.insert("end", item)

    def save_recommendation(self):
        file = open("recommendation.txt", "w")
        for item in self.listbox.get(0, tk.END):
            file.write(item + "\n")
        file.close()

        messagebox.showinfo("Informação", "Recomendações salvas com sucessos")

    def clear_entry(self):
        self.entry.delete(0, tk.END)

def recomendation_interface():
    root = tk.Tk()
    app = RecommendationSystemGUI(root)
    root.mainloop()

if __name__ == '__main__':
    recomendation_interface()

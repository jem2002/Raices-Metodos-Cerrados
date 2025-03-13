import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from metodos import bisection, false_position, velocity_function

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class RootFinderApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Métodos Cerrados - Laboratorio 2")
        self.geometry("1000x800")
        self._create_widgets()

    def _create_widgets(self):
        # Frame de entrada
        input_frame = ctk.CTkFrame(self)
        input_frame.pack(pady=10, padx=10, fill="x")

        # Campos de entrada
        self.a_entry = ctk.CTkEntry(input_frame, placeholder_text="a")
        self.a_entry.insert(0, "50")
        self.a_entry.pack(side="left", padx=5)
        self.b_entry = ctk.CTkEntry(input_frame, placeholder_text="b")
        self.b_entry.insert(0, "60")
        self.b_entry.pack(side="left", padx=5)
        self.tol_entry = ctk.CTkEntry(input_frame, placeholder_text="Tolerancia")
        self.tol_entry.insert(0, "0.001")
        self.tol_entry.pack(side="left", padx=5)

        # Selector de método
        self.method = ctk.CTkOptionMenu(input_frame, values=["Bisección", "Falsa Posición"])
        self.method.pack(side="left", padx=5)

        # Botón de cálculo
        self.calculate_btn = ctk.CTkButton(input_frame, text="Calcular", command=self._calculate)
        self.calculate_btn.pack(side="left", padx=5)

        # Resultados
        self.result_text = ctk.CTkTextbox(self, height=100)
        self.result_text.pack(pady=10, padx=10, fill="x")

        # Gráfico
        self.figure = plt.figure(figsize=(8, 6))
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self)
        self.canvas.get_tk_widget().pack(pady=10, padx=10, fill="both", expand=True)

    def _calculate(self):
        self.result_text.delete("1.0", ctk.END)
        self.ax.clear()

        try:
            a = float(self.a_entry.get())
            b = float(self.b_entry.get())
            tol = float(self.tol_entry.get())
        except ValueError:
            self.result_text.insert("1.0", "Error: Valores inválidos.")
            return

        try:
            if self.method.get() == "Bisección":
                root, iterations = bisection(velocity_function, a, b, tol)
            else:
                root, iterations = false_position(velocity_function, a, b, tol)
        except Exception as e:
            self.result_text.insert("1.0", f"Error: {str(e)}")
            return

        # Mostrar resultados
        self.result_text.insert("1.0", f"Raíz: {root:.6f}\nIteraciones: {len(iterations)}")

        # Graficar
        m = [a + (b - a) * i / 100 for i in range(100)]
        v = [velocity_function(x) for x in m]
        self.ax.plot(m, v, label="f(m)")
        self.ax.scatter([step[2] for step in iterations], [0]*len(iterations), color="red", label="Aproximaciones")
        self.ax.axhline(0, color="gray", linestyle="--")
        self.ax.legend()
        self.canvas.draw()

if __name__ == "__main__":
    app = RootFinderApp()
    app.mainloop()
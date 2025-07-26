
import math as mt
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#Funcion DELTA F
def DELTA(Cik, Ckj, Cij):
    deltaF = Cik + Ckj - Cij
    return deltaF

#Apertura de archivo en modo lectura
archivo = open("Datos.txt", "r")

#Declaracion de variables
DistanciaA = 0
DistanciaB = 0
DistanciaC = 0
i = 0
n = 0
Total = 0
Existe = True
AgenteActual = 0
Agente = []
Z = 0
AgentesResultantes = []
Costo = []
DELTA_F = []
SubTour = [] 
SubTourm = []
AgenteResiduo = []
Agente.append(AgenteActual)
#Declaracion de arreglos
Coordenadax, Coordenaday = 2, 10;
CoordenadaCliente = [[0 for x in range(Coordenadax)] for y in range(Coordenaday)] 

Distanciax, Distanciay = 10, 10;
DistanciaCliente = [[0 for x in range(Distanciax)] for y in range(Distanciay)] 

#Lectura de Coordenadas 
for i in range(10):
    STRClienteX = archivo.readline()
    STRClienteY = archivo.readline()
    Cx = int(STRClienteX)
    Cy = int(STRClienteY)
    CoordenadaCliente[i][0] = Cx
    CoordenadaCliente[i][1] = Cy
    
archivo.close()


#Calcular distancia entre clientes
for i in range(10):
    DistanciaA1 = CoordenadaCliente[i][0]
    DistanciaB1 = CoordenadaCliente[i][1]
    for n in range(10):
            DistanciaA = DistanciaA1 - CoordenadaCliente[n][0]
            DistanciaB = DistanciaB1 - CoordenadaCliente[n][1]
            DistanciaC = mt.sqrt(pow(DistanciaA,2)+pow(DistanciaB,2))
            DistanciaCliente[i][n] = round(DistanciaC)




Costo.append(DistanciaCliente[AgenteActual][AgenteActual])
Distancia = DistanciaCliente[AgenteActual][AgenteActual+1]
AgenteObtenido = AgenteActual+1
#Nodo Arbitrario y ruta T
for i in range(10):
    if(i != AgenteActual and DistanciaCliente[AgenteActual][i] > 0):
        for r in range(len(Agente)):
            if(i == Agente[r]):
                Existe = True
                break
            else:
                Existe = False
    else: Existe = True
    if(DistanciaCliente[AgenteActual][i] < Distancia and DistanciaCliente[AgenteActual][i] != 0 and Existe == False):
        Distancia = DistanciaCliente[AgenteActual][i]
        AgenteObtenido = i
Costo.append(Distancia)
Agente.append(AgenteObtenido)
Agente.append(AgenteActual)



while(Z < 11):
    for i in range(10):
        for r in range(len(Agente)):
            if(i == Agente[r]):
                Existe = True
                break
            else:   
                Existe = False
        if(Existe == False):
            AgenteResiduo.append(i)


    for i in range(len(AgenteResiduo)):
        Punto = 0
        for r in range(len(Agente)-1):
            Punto = r + 1
            k = False
            DELTA_F.append(DELTA(DistanciaCliente[Agente[r]][AgenteResiduo[i]],DistanciaCliente[AgenteResiduo[i]][Agente[r+1]],DistanciaCliente[Agente[r]][Agente[r+1]]))
            n = 0
            while(k == False): 
                if(n == Punto):
                    SubTourm.append(AgenteResiduo[i])
                    k = True
                    break
                else:
                    SubTourm.append(Agente[n])
                n = n + 1    

            while(n < len(Agente)):
                SubTourm.append(Agente[n])
                n = n + 1
            SubTour.append(SubTourm.copy())
            SubTourm.clear()
    Distancia = DELTA_F[0]
    Clave = 0 

    for i in range(len(DELTA_F)):
        if(DELTA_F[i] < Distancia):
            Distancia = DELTA_F[i]
            Clave = i
    Agente.clear()
    Agente = SubTour[Clave].copy()
    SubTour.clear()
    DELTA_F.clear()
    AgenteResiduo.clear()
    Costo.append(Distancia)
    Z = len(Agente)

    
for i in range(len(Agente)-1):
    Total = Total + DistanciaCliente[Agente[i]][Agente[i+1]]


# --- VISUALIZACIÓN EN UNA SOLA VENTANA CON PESTAÑAS ---
root = tk.Tk()
root.title("Resultados Computados - Inserción Más Barata")
root.geometry("700x700")

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both")

# Pestaña de la gráfica
frame_grafica = ttk.Frame(notebook)
notebook.add(frame_grafica, text="Gráfica de Ruta")

fig, ax = plt.subplots(figsize=(7, 7))
x_coords = [CoordenadaCliente[i][0] for i in Agente]
y_coords = [CoordenadaCliente[i][1] for i in Agente]
ax.plot(x_coords, y_coords, marker='o', linestyle='-', color='b', label='Ruta')
for idx, (x, y) in enumerate(zip(x_coords, y_coords)):
    ax.scatter(x, y, color='red')
    ax.text(x, y+1, str(Agente[idx]), fontsize=10, ha='center')
ax.set_title('Ruta de Inserción Más Barata')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.grid(True)
ax.legend()
fig.tight_layout()

canvas = FigureCanvasTkAgg(fig, master=frame_grafica)
canvas.draw()
canvas.get_tk_widget().pack(expand=True, fill="both")

# Pestaña de la tabla
frame_tabla = ttk.Frame(notebook)
notebook.add(frame_tabla, text="Tabla de Resultados")

tree = ttk.Treeview(frame_tabla, columns=("#1", "#2"), show="headings")
tree.heading("#1", text="Orden de Visita")
tree.heading("#2", text="Cliente (X, Y)")
for idx, cliente in enumerate(Agente):
    tree.insert("", "end", values=(idx+1, f"({CoordenadaCliente[cliente][0]}, {CoordenadaCliente[cliente][1]})"))
tree.pack(expand=True, fill="both", padx=10, pady=10)

label_total = tk.Label(frame_tabla, text=f"Costo total: {Total}", font=("Arial", 14, "bold"))
label_total.pack(pady=10)

root.mainloop()

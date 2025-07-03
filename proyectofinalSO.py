import matplotlib.pyplot as plt
import random

class process:
    def __init__(self, pid,arrivalTime,bursTime):
        self.pid = pid
        self.arrivalTime = arrivalTime
        self.burstTime = bursTime
        self.waitTime = 0
        self.completionTime = 0
        self.turnaroundTime = 0

    def setWaitTime (self,time):
        self.waitTime += time

    def setCompletionTime (self):
        self.completionTime = self.arrivalTime + self.burstTime + self.waitTime

    def setTurnaroundTime (self):
        self.turnaroundTime = self.completionTime - self.arrivalTime


class sheduler: 
    def __init__(self,processes):
        self.processes = processes
        self.actualTime = 0

    def fifo(self):
        processes = sorted(self.processes, key=lambda p: p.arrivalTime)
        for process in processes:
            process.setWaitTime(self.actualTime-process.arrivalTime)
            process.setCompletionTime()
            process.setTurnaroundTime()
            self.actualTime += process.burstTime

    def sjf(self):
        pendientes = sorted(self.processes, key=lambda p: p.arrivalTime)
        ejecutados = []

        while pendientes:
            llegados = [p for p in pendientes if p.arrivalTime <= self.actualTime]
            
            """if not llegados:
                self.actualTime = pendientes[0].arrivalTime
                llegados = [pendientes[0]]"""
            
            actual = min(llegados, key=lambda p: p.burstTime)
            pendientes.remove(actual)

            actual.setWaitTime(self.actualTime - actual.arrivalTime)
            actual.setCompletionTime()
            actual.setTurnaroundTime()

            self.actualTime = actual.completionTime
            ejecutados.append(actual)

        self.processes = sorted(ejecutados, key=lambda p: p.pid)
           

    def stcf(self):
        print("Logica aqui")

    def priority(self):
        print("Logica aqui")

    def rr(self):
        print("Logica aqui")

    def mlq(self):
        print("Logica aqui")

    def mlq(self):
        print("Logica aqui")

    def mlfq(self):
        print("Logica aqui")

    def showInfoProcesses(self):
        print("INFO PROCESSES\n")
        print("|PID|ARRIVAL|BURST|WAIT|COMPLETION|TURNAROUND|")
        for p in self.processes:
            print(f"|{p.pid:^3}|{p.arrivalTime:^7}|{p.burstTime:^5}|"
                  f"{p.waitTime:^5}|{p.completionTime:^10}|{p.turnaroundTime:^10}|")
            
            

class Infoprocesses:
    def __init__(self,processes):
        self.processes = processes
        self.actualTime = 0
        self.totalTime = sum(p.burstTime for p in processes)
        self.avarageWaitTime = sum(p.waitTime for p in processes)/len(processes)
        self.avarageCompletionTime = sum(p.completionTime for p in processes)/len(processes)
        self.avarageTurnaroundTime= sum(p.turnaroundTime for p in processes)/len(processes)



def createProcessAutomatic(n):
    procesos = []
    for i in range(1,n+1):
        numeroRandom = random.randint(10, 50)
        procesos.append(process(i,0,numeroRandom))
    return procesos

def createProcessesManual(datos):
    procesos = []
    for i, (arrival, burst) in enumerate(datos, start=1):
        procesos.append(process(i, arrival, burst))
    return procesos



def chooseAlgorithmAutomatic(algorithm,nProcess):
    global planificador,procesos
    procesos = createProcessAutomatic(nProcess)
    planificador = sheduler(procesos)
    metodo = getattr(planificador, algorithm)
    metodo() 
    planificador.showInfoProcesses()

def chooseAlgorithmManual(algorithm,processes):
    global planificador,procesos
    procesos = createProcessesManual(processes)
    planificador = sheduler(procesos)
    metodo = getattr(planificador, algorithm)
    metodo() 
    planificador.showInfoProcesses()



#Solo basta con poner el nombre del algoritmo aca
exampleProcesses = [(0,5),(2,3),(4,8),(6,2)] #cada tupla es un proceso (arrivalTime,BurstTime)

chooseAlgorithmManual('sjf',exampleProcesses)


#Creación del Grafico

categorias = ['WT', 'CT', 'TT']
infoAvarageProcess = Infoprocesses(planificador.processes)
valores = [infoAvarageProcess.avarageWaitTime,infoAvarageProcess.avarageCompletionTime , infoAvarageProcess.avarageTurnaroundTime]

plt.figure()
plt.bar(categorias, valores)

#Texto que muestra el valor exacto
for i in range(len(categorias)):
    plt.text(
        x=i, 
        y=valores[i] + 0.2, 
        s=f"{valores[i]:.2f}",  
        ha='center'
    )



# Añadir título y etiquetas
plt.title("Promedio valores obtenidos")
plt.xlabel("Eje X (Propiedades)")
plt.ylabel("Eje Y (valores)")

# Mostrar
plt.show(block=False)



#Grafica2 de como cambia cada propiedad en funcion del tiempo

times = [p.completionTime   for p in procesos]
waits = [p.waitTime         for p in procesos]
comps = [p.completionTime   for p in procesos]
turns = [p.turnaroundTime   for p in procesos]
total = infoAvarageProcess.totalTime

# 2. Prepara la figura
fig, ax = plt.subplots()
ax.set_xlabel("Tiempo")
ax.set_ylabel("Tiempo de proceso")
ax.set_title("Evolución de métricas")

# 3. Listas vacías para acumulación
t_vals, w_vals, c_vals, r_vals = [], [], [], []

# 4. Bucle de animación
for i in range(len(times)):
    t_vals.append(times[i])
    w_vals.append(waits[i])
    c_vals.append(comps[i])
    r_vals.append(turns[i])
    
    ax.cla()  # limpia el eje
    ax.set_xlim(0, total + 20)
    ax.set_ylim(0, max(comps) * 1.1)
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Tiempo de proceso")
    ax.set_title("Evolución de métricas")
    
    ax.plot(t_vals, w_vals, marker='o', label='Wait Time')
    ax.plot(t_vals, c_vals, marker='s', linestyle='--', label='Completion Time')
    ax.plot(t_vals, r_vals, marker='^', linestyle=':', label='Turnaround Time')
    
    # anotaciones de valores
    for x, y in zip(t_vals, w_vals):
        ax.text(x, y + 1, f"{y}", ha='center', va='bottom')
    for x, y in zip(t_vals, c_vals):
        ax.text(x, y + 1, f"{y}", ha='center', va='bottom')
    for x, y in zip(t_vals, r_vals):
        ax.text(x, y + 1, f"{y}", ha='center', va='bottom')
    
    ax.legend()
    plt.pause(1)

plt.show()
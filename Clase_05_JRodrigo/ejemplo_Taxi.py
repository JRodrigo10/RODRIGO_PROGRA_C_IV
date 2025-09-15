import threading
import time
import random

# Lista de taxis disponibles
taxis = ["Taxi-1", "Taxi-2", "Taxi-3"]
lock = threading.Lock()

def pedir_taxi(cliente, operacion):
    print(f"[{cliente}] 🚕 Intentando pedir taxi (operación {operacion})...")
    with lock:  # sección crítica
        print(f"[{cliente}] Entró a la sección crítica.")
        time.sleep(1)  # simulamos tiempo de gestión
        
        if taxis:
            taxi_asignado = taxis.pop(0)  # asigna el primer taxi libre
            print(f"[{cliente}] ✅ Taxi asignado: {taxi_asignado}")
        else:
            print(f"[{cliente}] ❌ No hay taxis disponibles.")
        
        print(f"[{cliente}] Saliendo de la sección crítica.")

def main():
    clientes = [
        threading.Thread(target=pedir_taxi, args=("Cliente1", 1)),
        threading.Thread(target=pedir_taxi, args=("Cliente2", 1)),
        threading.Thread(target=pedir_taxi, args=("Cliente3", 1)),
        threading.Thread(target=pedir_taxi, args=("Cliente4", 1)),
        threading.Thread(target=pedir_taxi, args=("Cliente5", 1)),
    ]

    for c in clientes: 
        c.start()
    for c in clientes: 
        c.join()

    print("\n🚖 Todas las solicitudes de taxi fueron procesadas.")
    print(f"🚕 Taxis restantes: {taxis}")

if __name__ == "__main__":
    main()

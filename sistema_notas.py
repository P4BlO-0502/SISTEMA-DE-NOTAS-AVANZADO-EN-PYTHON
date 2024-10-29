import json
import os

class Nota:
    def __init__(self, contenido, etiquetas=None):
        self.contenido = contenido
        self.etiquetas = etiquetas if etiquetas else []
    
    def agregar_etiqueta(self, etiqueta):
        if etiqueta not in self.etiquetas:
            self.etiquetas.append(etiqueta)
    
    def eliminar_etiqueta(self, etiqueta):
        if etiqueta in self.etiquetas:
            self.etiquetas.remove(etiqueta)
    
    def editar_contenido(self, nuevo_contenido):
        self.contenido = nuevo_contenido

    def to_dict(self):
        return {
            'contenido': self.contenido,
            'etiquetas': self.etiquetas
        }
    
    @staticmethod
    def from_dict(data):
        return Nota(data['contenido'], data['etiquetas'])

    def __str__(self):
        return f"Nota: {self.contenido}\nEtiquetas: {', '.join(self.etiquetas)}"


class SistemaNotas:
    def __init__(self, archivo='notas.json'):
        self.notas = []
        self.archivo = archivo
        self.cargar_notas()

    def agregar_nota(self, contenido, etiquetas=None):
        nueva_nota = Nota(contenido, etiquetas)
        self.notas.append(nueva_nota)
        self.guardar_notas()

    def editar_nota(self, indice, nuevo_contenido, nuevas_etiquetas=None):
        if 0 <= indice < len(self.notas):
            self.notas[indice].editar_contenido(nuevo_contenido)
            if nuevas_etiquetas is not None:
                self.notas[indice].etiquetas = nuevas_etiquetas
            self.guardar_notas()
        else:
            raise IndexError("Índice de nota no válido.")

    def eliminar_nota(self, numero):
        if 1 <= numero <= len(self.notas):
            del self.notas[numero - 1]
            self.guardar_notas()
        else:
            raise ValueError("Número de nota no válido.")

    def buscar_por_etiqueta(self, etiqueta):
        return [nota for nota in self.notas if etiqueta in nota.etiquetas]

    def buscar_por_contenido(self, termino):
        return [nota for nota in self.notas if termino.lower() in nota.contenido.lower()]

    def mostrar_notas(self):
        if not self.notas:
            print("No hay notas disponibles.")
            return
        for i, nota in enumerate(self.notas):
            print(f"{i + 1}. {nota}")
            print("-" * 40)

    def guardar_notas(self):
        with open(self.archivo, 'w') as f:
            json.dump([nota.to_dict() for nota in self.notas], f)

    def cargar_notas(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, 'r') as f:
                datos = json.load(f)
                self.notas = [Nota.from_dict(nota) for nota in datos]

def menu():
    sistema = SistemaNotas()

    while True:
        print("\n--- Sistema de Notas, programado por P4BLO-0502 ---")
        print("1. Agregar Nota")
        print("2. Editar Nota")
        print("3. Eliminar Nota")
        print("4. Mostrar Notas")
        print("5. Buscar por Etiqueta")
        print("6. Buscar por Contenido")
        print("7. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            contenido = input("Contenido de la nota: ")
            etiquetas = input("Etiquetas (separadas por comas): ").split(',')
            etiquetas = [etiqueta.strip() for etiqueta in etiquetas]
            sistema.agregar_nota(contenido, etiquetas)
        
        elif opcion == '2':
            sistema.mostrar_notas()
            numero = int(input("Número de la nota a editar: "))
            nuevo_contenido = input("Nuevo contenido: ")
            nuevas_etiquetas = input("Nuevas etiquetas (separadas por comas): ").split(',')
            nuevas_etiquetas = [etiqueta.strip() for etiqueta in nuevas_etiquetas]
            try:
                sistema.editar_nota(numero - 1, nuevo_contenido, nuevas_etiquetas)
            except IndexError as e:
                print(e)
        
        elif opcion == '3':
            sistema.mostrar_notas()
            numero = int(input("Número de la nota a eliminar: "))
            try:
                sistema.eliminar_nota(numero)
            except ValueError as e:
                print(e)
        
        elif opcion == '4':
            sistema.mostrar_notas()
        
        elif opcion == '5':
            etiqueta = input("Etiqueta a buscar: ")
            notas_encontradas = sistema.buscar_por_etiqueta(etiqueta)
            if notas_encontradas:
                for nota in notas_encontradas:
                    print(nota)
            else:
                print("No se encontraron notas con esa etiqueta.")
        
        elif opcion == '6':
            termino = input("Término a buscar en contenido: ")
            notas_encontradas = sistema.buscar_por_contenido(termino)
            if notas_encontradas:
                for nota in notas_encontradas:
                    print(nota)
            else:
                print("No se encontraron notas con ese contenido.")
        
        elif opcion == '7':
            print("Saliendo del sistema.")
            break
        
        else:
            print("Opción no válida. Intenta de nuevo.")

if __name__ == "__main__":
    menu()

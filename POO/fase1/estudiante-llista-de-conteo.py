productos = ["manzana", "banana", "naranja", "pera"]

print("Productos en la lista:")
for producto in productos:
    print(f"- {producto}")

contador = 0
for producto in productos:
    contador += 1

print(f"\nEl número total de productos es: {contador}")

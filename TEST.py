from enum import Enum

# Definiujemy klasę bazową Owoc
class Owoc:
    def __init__(self, nazwa, i):
        self.nazwa = nazwa
        self.i = i

# Definiujemy klasy dziedziczące po Owoc
class Jablko(Owoc):
    def __init__(self, i):
        super().__init__("Jablko", i)

class Gruszka(Owoc):
    def __init__(self, i):
        super().__init__("Gruszka", i)

class Arbuz(Owoc):
    def __init__(self, i):
        super().__init__("Arbuz", i)

class Malina(Owoc):
    def __init__(self, i):
        super().__init__("Malina", i)

# Enum do mapowania litery na klasę
class OwocEnum(Enum):
    J = Jablko
    G = Gruszka
    A = Arbuz
    M = Malina

# Funkcja wybierająca odpowiednie owoce
def wybierz_owoce_po_literze(litera, lista_owocow):
    klasa_owocu = OwocEnum[litera].value  # Pobieramy klasę na podstawie litery
    print(klasa_owocu)
    return [owoc for owoc in lista_owocow if isinstance(owoc, klasa_owocu)]



# Przykładowa lista owoców
lista_owocow = [Jablko(1), Gruszka(2), Arbuz(3), Malina(5), Jablko(5), Gruszka(6), Jablko(2)]


# Przykład użycia funkcji
for w in lista_owocow:
    print(w.nazwa, w.i)

a = []
for i in range(8):
    row = []
    for j in range(8):
        row.append((i, j))
    a.append(row)

for i in a:
    for j in i:
        print(j, end =" ")
    print()
print()

y, x = 0, 7 # start
field = a[y][x]
go_to_y, go_to_x = 7, 0 # end

sign_y_bishop = -1 if go_to_y - y < 0 else 1
sign_x_bishop = -1 if go_to_x - x < 0 else 1

i, j = y + sign_y_bishop, x + sign_x_bishop
while i != go_to_y and j != go_to_x:
    print(a[i][j])  # Drukujemy aktualną komórkę
    i += sign_y_bishop
    j += sign_x_bishop


p = False
q = False
print( (p and not q) or (not p and q) )
print(not ((p and not q) or (not p and q)))
print( (not p or q) and (p or not q) )
print()


for i in a:
    for j in i:
        print(j, end =" ")
    print()
print()

y, x = 0, 7 # start
field = a[y][x]
go_to_y, go_to_x = 0, 0 # end
sign_y_rook = -1 if (go_to_y - y < 0) else 0 if (go_to_y - y == 0) else 1
sign_x_rook = -1 if (go_to_x - x < 0) else 0 if (go_to_x - x == 0) else 1

i, j = y + sign_y_rook, x + sign_x_rook
print(sign_y_rook, sign_x_rook)

while i * abs(sign_y_rook) != go_to_y * abs(sign_y_rook) or j * abs(sign_x_rook) != go_to_x * abs(sign_x_rook):
    print(a[i][j])  # Drukujemy aktualną komórkę
    i += sign_y_rook
    j += sign_x_rook
import random
import tkinter as tk

class TabuleiroSudoku:
    def __init__(self):
        # Crie um tabuleiro vazio (9x9) inicialmente com zeros
        self.tabuleiro = [[0 for _ in range(9)] for _ in range(9)]

    def verificar_validade(self):
        # Verificar cada linha, coluna e bloco 3x3
        for i in range(9):
            if not self.validar_linha(i) or not self.validar_coluna(i) or not self.validar_bloco(i):
                return False
        return True

    def validar_linha(self, row):
        numeros_presentes = set()
        for col in range(9):
            num = self.tabuleiro[row][col]
            if num != 0:
                if num in numeros_presentes:
                    return False
                numeros_presentes.add(num)
        return True

    def validar_coluna(self, col):
        numeros_presentes = set()
        for row in range(9):
            num = self.tabuleiro[row][col]
            if num != 0:
                if num in numeros_presentes:
                    return False
                numeros_presentes.add(num)
        return True

    def validar_bloco(self, block):
        numeros_presentes = set()
        row_start, col_start = 3 * (block // 3), 3 * (block % 3)
        for i in range(3):
            for j in range(3):
                num = self.tabuleiro[row_start + i][col_start + j]
                if num != 0:
                    if num in numeros_presentes:
                        return False
                    numeros_presentes.add(num)
        return True

    def resolver(self):
        vazio = self.proxima_celula_vazia()
        if not vazio:
            return True

        row, col = vazio

        for num in range(1, 10):
            if self.pode_inserir(row, col, num):
                self.tabuleiro[row][col] = num

                if self.resolver():
                    return True

                self.tabuleiro[row][col] = 0

        return False

    def proxima_celula_vazia(self):
        for i in range(9):
            for j in range(9):
                if self.tabuleiro[i][j] == 0:
                    return (i, j)
        return None

    def pode_inserir(self, row, col, num):
        # Verificar se o número num já está presente na mesma linha
        for i in range(9):
            if self.tabuleiro[row][i] == num:
                return False

        # Verificar se o número num já está presente na mesma coluna
        for i in range(9):
            if self.tabuleiro[i][col] == num:
                return False

        # Verificar se o número num já está presente no mesmo bloco 3x3
        bloco_start_row, bloco_start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.tabuleiro[bloco_start_row + i][bloco_start_col + j] == num:
                    return False

        return True

    def gerar_valido(self):
        for i in range(0, 9, 3):
            self.preencher_bloco(i, i)

    def preencher_bloco(self, row, col):
        numeros = list(range(1, 10))
        random.shuffle(numeros)
        for i in range(3):
            for j in range(3):
                self.tabuleiro[row + i][col + j] = numeros.pop()

    def mostrar_tabuleiro(self):
        for i in range(9):
            if i % 3 == 0 and i != 0:
                print("- - - - - - - - - - -")
            for j in range(9):
                if j % 3 == 0 and j != 0:
                    print("| ", end="")
                print(self.tabuleiro[i][j], " ", end="")
            print()

    def limpar_tabuleiro(self):
        self.tabuleiro = [[0 for _ in range(9)] for _ in range(9)]

    def criar_novo_tabuleiro(self):
        self.limpar_tabuleiro()
        self.gerar_valido()
        print("Tabuleiro válido gerado:")
        self.mostrar_tabuleiro()

        if self.verificar_validade():
            print("\nTabuleiro válido.")
        else:
            print("\nTabuleiro inválido.")

        if self.resolver():
            print("\nTabuleiro resolvido:")
            self.mostrar_tabuleiro()
        else:
            print("\nNão foi possível resolver o Sudoku.")

def criar_tabuleiro_gui():
    tabuleiro = TabuleiroSudoku()
    tabuleiro.gerar_valido()
    return tabuleiro

def mostrar_tabuleiro_gui(tabuleiro):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("- - - - - - - - - - -")
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("| ", end="")
            print(tabuleiro.tabuleiro[i][j], " ", end="")
        print()

def resolver_tabuleiro_gui(tabuleiro, label_status):
    if tabuleiro.resolver():
        label_status.config(text="Tabuleiro resolvido!")
    else:
        label_status.config(text="Não foi possível resolver o Sudoku.")

def criar_novo_tabuleiro_gui(tabuleiro, label_status):
    tabuleiro.limpar_tabuleiro()
    tabuleiro.gerar_valido()
    label_status.config(text="Tabuleiro válido gerado.")

def main():
    root = tk.Tk()
    root.title("Sudoku Solver")

    tabuleiro = criar_tabuleiro_gui()

    label_status = tk.Label(root, text="Tabuleiro gerado. Clique em Resolver para resolver o Sudoku.")
    label_status.pack(pady=10)

    frame_tabuleiro = tk.Frame(root)
    frame_tabuleiro.pack()

    entries = []  # Lista para armazenar as entradas dos campos do tabuleiro

    for i in range(9):
        row_entries = []
        for j in range(9):
            entry = tk.Entry(frame_tabuleiro, width=2, font=('Helvetica', 20))
            entry.grid(row=i, column=j)
            entry.insert(0, str(tabuleiro.tabuleiro[i][j]))
            row_entries.append(entry)
        entries.append(row_entries)

    frame_botoes = tk.Frame(root)
    frame_botoes.pack(pady=10)

    btn_resolver = tk.Button(frame_botoes, text="Resolver", command=lambda: resolver_tabuleiro_gui(tabuleiro, label_status))
    btn_resolver.pack(side=tk.LEFT, padx=5)

    btn_novo_tabuleiro = tk.Button(frame_botoes, text="Novo Tabuleiro", command=lambda: criar_novo_tabuleiro_gui(tabuleiro, label_status))
    btn_novo_tabuleiro.pack(side=tk.LEFT, padx=5)

    root.mainloop()

if __name__ == "__main__":
    main()

#coding=utf-8
# si calcoli la media mobile per una serie di valori in input.
# la lunghezza della finestra sarà data dall'utente e sarà l'unico parametro della classe MovingAverage
# la classe deve essere quindi inizializzata con questa parametro e poi contenere il metodo compute che
# prende in input una lista di valori e ritorni una lista di valori corrispondenti alle medie mobili via via calcolate

# le eccezioni devono essere alzate in caso di input non corretti o casi limite,
# e devono essere istanze di una specifica classe ExamException che andrà quindi definita

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

class ExamException(Exception):
    pass

class MovingAverage:
    def __init__(self, finestra):
        # il valore della finestra deve essere un intero, non sono ammessi float o stringhe
        if not isinstance(finestra, int):
            raise ExamException("Il valore della finestra non è un intero.")
        # la finestra se ha valore intero, questo non può essere negativo
        if finestra <1:
            raise ExamException("La finestra non può aver valori negativi o pari a zero")
        self.finestra = finestra

    def compute(self, lista_input):
        # controllo se parametro è una lista
        if not isinstance(lista_input, list):
            raise ExamException("Il parametro passato non è una lista.")
        # controllo se lista è vuota
        if len(lista_input) == 0:
            raise ExamException("La lista è vuota. non si può calcolare la media mobile")
        # controllo che finestra sia almeno pari a zero o superiore
        if len(lista_input) < self.finestra:
            raise ExamException("Non ci sono abbastanza elementi per sviluppare la media mobile")
        # controllo se i valori nella lista siano tutti numerici, float o interi
        for item in lista_input:
            if not (isinstance(item, int) or isinstance(item, float)):
                raise ExamException("Valori non numerici nella lista")

        # -o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o

        media_mobile = []
        # creo variabile i utile per gli spostamenti della finestra
        i=0
        while i < len(lista_input) - self.finestra + 1:
            # memorizza i gli elementi della finestra attuale in una lista
            window_elem = lista_input[i: i + self.finestra]

            # calcola la attuale media mobile
            window_average = round(sum(window_elem) / self.finestra, 2)

            # memorizza il risultato nella lista delle medie mobili
            media_mobile.append(window_average)

            # trasla la finestra di una posizione incrementando i
            i += 1
        return media_mobile

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# CALCOLARE LA DIFFERENZA DEGLI ELEMENTI DELLA LISTA
# SI PRENDA IN INPUT UNA LISTA DI VALORI NUMERICI ED IN OUTPUT LA LISTA DELLE LORO DIFFERENZE
# SI AGGIUNGA UN PARAMETRO RATIO CHE PERMETTA DI RISCALRE LE DIFFERENZE (VALORE DI DEFAULT = 1)
#
# CLASSE Diff():
#     1)INIZIALIZZATA CON PARAMETRO OPZIONALE RATIO DI VALORE 1
#     2) METODO COMPUTE CHE PRENDE IN INPUT UNA LISTA DI VALORI E RITORNA LA LISTA CON LE DIFFERENZE TRA I SINGOLI VALORI
#
# SI USI ISTANZA DI CLASSE PER LE ECCEZIONI


class Diff():
    def __init__(self, ratio):
        if not isinstance(ratio, int):
            raise ExamException("Ratio non è un valore intero")
        if ratio != 1:
            raise ExamException("Ratio è diverso da 1")
        if ratio == 0:
            raise ExamException("Ratio è zero. Non ammesso perchè si genera una divisione per zero")
        self.ratio = ratio

    def compute(self, lista_input):
        # controllo se parametro è una lista
        if not isinstance(lista_input, list):
            raise ExamException("Il parametro passato non è una lista.")

        # controllo se lista è vuota
        if len(lista_input) == 0:
            raise ExamException("La lista è vuota. Non si può calcolare la differenza")

        # controllo se lista ha meno di due elementi
        if len(lista_input) < 2:
            raise ExamException("La lista ha un solo elemento. Non si può calcolare la differenza")

        # controllo se i valori nella lista siano tutti numerici, float o interi
        for item in lista_input:
            if not (isinstance(item, int) or isinstance(item, float)):
                raise ExamException('Valori non numerici nella lista')

        i = 0
        lista_differenze = []
        while i < len(lista_input) -1:
            lista_differenze.append(float((lista_input[i+1] - lista_input[i])/self.ratio))
            i += 1
        return lista_differenze

        # -o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o





# creo lista vuota
my_list = []
ratio = 1
print("Digita i valori della lista: (Q per uscire)")
# prendo in input i valori da utente e li aggiungo alla lista
user_input = input("")
while(user_input.upper() != "Q"):
    my_list.append(float(user_input))
    user_input = input("")

# creo variabile per la lunghezza della finestra e chiedo all'utente che valore vuole
user_input_2 = input("digita il valore della finestra: ")
lung_finestra = int(user_input_2)

# istanzio la classe della media mobile
moving_average = MovingAverage(lung_finestra)
# variabile = applicazione metodo compute con lista come parametro
result = moving_average.compute(my_list)
# visualizzo in print la lista delle media calcolate
print(result)

# diff = Diff(ratio)
# differenze = diff.compute(my_list)
# print(differenze)
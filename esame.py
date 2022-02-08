# coding=utf-8
from datetime import datetime
info = []
lista_date = []
passengers = []
# ====================================================
#           DEFINIZIONE CLASSE ERRORI
# ====================================================

class ExamException(Exception):
    pass

# ====================================================
#           DEFINIZIONE CLASSE CSV E SUO METODO
# ====================================================

class CSVTimeSeriesFile:
    def __init__(self, name):
        self.name = name
        self.can_read = True
        try:
            my_file = open(self.name, 'r')
            my_file.readline()
        except Exception as e:
            self.can_read = False
            print('Errore in apertura del file: "{}"'.format(e))

    # definizione metodo get_data
    def get_data(self):
        # se non posso aprire il file ritorno errore ed esco
        if not self.can_read:
            print('Errore, file non aperto o illeggibile')
            return None
        else:
            # apro il file
            my_file = open(self.name, 'r')
            range_lines = my_file.readlines()
            # scorro le varie linee del file
            for line in range_lines:
                elements = line.split(',')
                # salto intestazione
                if 'date' in line:
                    continue
                # gestisco i doppioni delle date. con doppioni alzo errore
                if elements[0] in lista_date:
                    raise ExamException("ERRORE. Non si vuole duplicati di date")
                else:
                    lista_date.append(elements[0])

                # INSERIRE CONTROLLO ORDINE CRESCENTE SU TIMESTAMP
                # provo a convertire il valore dei passeggeri ad intero,
                # se non è possibile gestisco errore
                try:
                    elements[-1] = int(elements[-1].strip())
                except:
                    print("Numero non convertibile a intero. Trasformato  in 0")
                    elements[-1] = 0
                if elements[-1] < 0:
                    print("Numero negativo non accettato. Trasformato in 0")
                    elements[-1] = 0
                # inserisco i valori nelle due liste
                passengers.append(elements[-1])
                info.append(elements)
        # chiudo file
        my_file.close()
        return info


# ====================================================================
#           ISTANZIAMENTO CLASSE, CHIAMATA METODO, CHIAMATA FUNZIONE
# ====================================================================


file_name = r"/Users/simoneperessini/Desktop/data.csv"
time_series_file = CSVTimeSeriesFile(name=file_name)
time_series = time_series_file.get_data()
print(time_series)

# LISTE DELLE ANNATE SENZA DUPLICATI
anni = []
lista_anni = []
# inserisco nella lista anni tutti gli anni trovati nella lista info
for x in lista_date:
    if x not in anni:
        anni.append(x[0:4])

# tengo solo gli anni univoci della lista anni
for y in anni:
    if y not in lista_anni:
        lista_anni.append(y)

# ====================================================================
#           DEFINIZIONE FUNZIONE DI CALCOLO MEDIA PASSEGGERI
# ====================================================================

def compute_avg_monthly_difference(time_series, first_year, last_year):
    if (type(first_year) != str) & (type(last_year) != str):
        print("I due estremi intervalli non sono entrambi stringhe")
    elif (first_year not in lista_anni) | (last_year not in lista_anni):
        print("Almeno uno dei due estremi non è un valore contenuto nel file")
    elif (int(first_year) > int(last_year)):
        print("Estremo iniziale intervallo è superiore a estremo finale")
    else:
        incremento_pass = []
        indice_inizio = anni.index(first_year)
        # dal momento voglio incluso anche estremo finale
        # converto in numero last_year, aggiungo 1 per avere posizione corretta
        # lo ripasso a stringa e poi ad index che mi restituisce posizione
        indice_fine = anni.index(str(int(last_year) + 1))
        intervallo = info[indice_inizio: indice_fine]
        delta_anni = int(last_year) - int(first_year)

        i = 0
        diff = 0
        if delta_anni == 0:
            for p in intervallo:
                incremento_pass.append(p[1])

        elif delta_anni == 1:
            while i < 12:
                if (intervallo[i + 12][1] != 0) & (intervallo[i][1] != 0):
                    media = (float(intervallo[i + 12][1]) - float(intervallo[i][1]))
                    diff += media
                    incremento_pass.append(diff)
                    diff = 0
                    i += 1
                else:
                    incremento_pass.append(0)


        elif delta_anni == 2:
            while i < 12:
                n_addizioni = 0
                anno_attuale = n_addizioni * 12 + i
                anno_succ = (n_addizioni + 1) * 12 + i
                if (intervallo[anno_succ][1] != 0) & (intervallo[anno_attuale][1] != 0):
                    while n_addizioni < delta_anni:
                        media = (float(intervallo[(n_addizioni + 1) * 12 + i][1]) - float(
                            intervallo[n_addizioni * 12 + i][1])) / delta_anni
                        n_addizioni += 1
                        diff += media
                    incremento_pass.append(diff)
                    diff = 0
                    i += 1
                else:
                    incremento_pass.append(0)

        elif delta_anni > 2:
            while i < 12:
                misurazioni = 0
                for x in range(0, delta_anni):
                    y = x * 12
                    if intervallo[i + y][1] != 0:
                        misurazioni += 1

                if misurazioni < 2:
                    incremento_pass.append(0)
                else:
                    n_addizioni = 0
                    # anno_attuale = n_addizioni * 12 + i
                    # anno_succ = (n_addizioni + 1) * 12 + i
                    while n_addizioni < delta_anni:
                        media = (float(intervallo[(n_addizioni + 1) * 12 + i][1]) - float(
                            intervallo[n_addizioni * 12 + i][1])) / delta_anni
                        n_addizioni += 1
                        diff += media
                    incremento_pass.append(diff)
                    diff = 0
                i += 1
        return incremento_pass


first_year = "1954"
last_year = "1958"
variazioni_passeggeri = compute_avg_monthly_difference(time_series, first_year, last_year)
print(variazioni_passeggeri)

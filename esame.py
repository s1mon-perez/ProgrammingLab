import datetime

# ======================
# CLASSE ERRORI
# ======================
class ExamException(Exception):
    pass

# ========================= #
#  CSVTIMESERIESFILE CLASS  #
# ========================= #
class CSVTimeSeriesFile():
    def __init__(self, name):
        self.name = name
        if not isinstance(name,str):
            print("ATTENZIONE file non in formato stringa, si prova a convertirlo")
            try:
                self.name = str(name)
            except Exception:
                raise ExamException("Non è stato possibile convertire il file in stringa")

    def get_data(self):
        lista_finale = []
        liste_timestamp = []
        try:
            my_file = open(self.name, 'r')
            #range_lines = my_file.readlines()
        except Exception:
            raise ExamException("Errore in apertura file")
        for line in my_file:
            elements = line.split(',')

            if len(elements)>2:
                raise ExamException("Ci sono valori in eccesso")

            # salto intestazione
            if 'date' in line:
                continue
            anno_mese = elements[0].strip()
            try:
                anno_mese = datetime.datetime.strptime(anno_mese, "%Y-%m")
                liste_timestamp.append(anno_mese)
            except Exception:
                continue
            #

            try:
                elements[1] = int(elements[1].strip())
                
            except IndexError:
                elements[1] = 0
            
            except ValueError:
                continue # float

            if elements[1] < 0:
                continue # negative
           
            

            lista_finale.append(elements)

        # controllo ordinamento timestamps
        for x in range(len(liste_timestamp)-1):
            if liste_timestamp[x] > liste_timestamp[x+1]:
                raise ExamException("I valori temporali non sono in ordine cronologico")

        # per ogni valore appartenente alla lista timestamp,
        # verifico se ce ne sia uno identico che va dalla posizione successiva fino a fondo lista
        for x in range(len(liste_timestamp) - 1):
            for y in range(x + 1, len(liste_timestamp)):
                if liste_timestamp[x] == liste_timestamp[y]:
                    raise ExamException("Ci sono dei valori temporali duplicati nel file")

        return lista_finale

# ================================ #
#  COMPUTE AVG MONTHLY DIFFERENCE  #
# ================================ #
def compute_avg_monthly_difference(time_series, first_year, last_year):
    lista_anni = []
    incremento_pass = []
    for x in time_series:
        lista_anni.append(x[0][0:4])

    # Check if time_series is a list
    if not isinstance(time_series, list):
        raise ExamException('ERRORE, time series non è una lista di liste.')
    else:
        if isinstance(time_series, list):
            if not isinstance(time_series[0], list):
                raise ExamException('ERRORE, time series non è una lista di liste.')

    if not isinstance(first_year, str):
        raise ExamException("Estremo iniziale non è una stringa")
    if not isinstance(last_year, str):
        raise ExamException("estremo finale non è una stringa")
    elif (first_year not in lista_anni) | (last_year not in lista_anni):
        raise ExamException("Almeno uno dei due estremi non è un valore contenuto nel file")
    elif (int(first_year) > int(last_year)):
        raise ExamException("Estremo iniziale intervallo è superiore a estremo finale")
    else:
        # incremento_pass = []
        indice_inizio = lista_anni.index(first_year)
        # dal momento voglio incluso anche estremo finale
        # converto in numero last_year, aggiungo 1 per avere posizione corretta
        # lo ripasso a stringa e poi ad index che mi restituisce posizione

        indice_fine = lista_anni.index(last_year)+12
        intervallo = time_series[indice_inizio: indice_fine]
        print(intervallo)
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
                    while n_addizioni < delta_anni:
                        media = (float(intervallo[(n_addizioni + 1) * 12 + i][1]) - float(
                            intervallo[n_addizioni * 12 + i][1])) / delta_anni
                        n_addizioni += 1
                        diff += media
                    incremento_pass.append(diff)
                    diff = 0
                i += 1
        return incremento_pass

# istanze della classe
#file_name = r"/Users/simoneperessini/Desktop/data.csv"
#time_series_file = CSVTimeSeriesFile(name='data.csv')
#time_series = time_series_file.get_data()

#print(compute_avg_monthly_difference(time_series, '1949', '1951'))
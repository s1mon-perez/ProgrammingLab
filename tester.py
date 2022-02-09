#!/usr/bin/env python3

#==============================
# Test  
#==============================

import datetime
import unittest
import tempfile
import warnings

from esame import CSVTimeSeriesFile, compute_avg_monthly_difference, ExamException

score = 0

class TestAndGrade(unittest.TestCase):

    # Roba per il testing
    def setUp(self):
        warnings.simplefilter("ignore", ResourceWarning)

    #===========================================================
    # Test per il 18: tre ore di dati, tutti i dati presenti.
    #===========================================================

    def test_correctness(self):

        with tempfile.NamedTemporaryFile('w+t') as file:

            file.write('date,passengers\n')

            # First year
            file.write('1949-01,112\n')
            file.write('1949-02,118\n')
            file.write('1949-03,132\n')
            file.write('1949-04,129\n')
            file.write('1949-05,121\n')
            file.write('1949-06,135\n')
            file.write('1949-07,148\n')
            file.write('1949-08,148\n')
            file.write('1949-09,136\n')
            file.write('1949-10,119\n')
            file.write('1949-11,104\n')
            file.write('1949-12,118\n')

            # Second year
            file.write('1950-01,115\n')
            file.write('1950-02,126\n')
            file.write('1950-03,141\n')
            file.write('1950-04,135\n')
            file.write('1950-05,125\n')
            file.write('1950-06,149\n')
            file.write('1950-07,170\n')
            file.write('1950-08,170\n')
            file.write('1950-09,158\n')
            file.write('1950-10,133\n')
            file.write('1950-11,114\n')
            file.write('1950-12,140\n')

            # Third year
            file.write('1951-01,145\n')
            file.write('1951-02,150\n')
            file.write('1951-03,178\n')
            file.write('1951-04,163\n')
            file.write('1951-05,172\n')
            file.write('1951-06,178\n')
            file.write('1951-07,199\n')
            file.write('1951-08,199\n')
            file.write('1951-09,184\n')
            file.write('1951-10,162\n')
            file.write('1951-11,146\n')
            file.write('1951-12,166\n')

            # Needed things 
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            results = compute_avg_monthly_difference(time_series,"1949","1951")

            self.assertTrue(len(results) in range(2,13))
            self.assertEqual(results[0], 16.5)
            self.assertEqual(results[1], 16)

            global score; score += 18 # Increase score

            # Controllo anche sull'ultima ora ed il suo cabio trend calcolato correttamente
            if len(results) == 12:
                if results[2] == 23:
                    score += 1 # Increase score

    #=====================================================
    # Controllo su cambi ora al limite
    #=====================================================

    #def test_correctness_last_day(self):
#
        #with tempfile.NamedTemporaryFile('w+t') as file:
#
            ## Scrivo i contenuti nel file di test
            #file.write('date,passengers\n')
            #epoch=3600
            #for i in range(3):
                #for j in range(6):
                    #if j<3:
                        #data='{},{}\n'.format(epoch, 20+j)
                    #else:
                        #data='{},{}\n'.format(epoch, 26-j)
                    #file.write(data)
                    #epoch+=600
#
            #file.seek(0) # Torno all'inizio del file (necessario per i tmpfile)
#
            #time_series_file = CSVTimeSeriesFile(file.name)
            #time_series = time_series_file.get_data()
            #results = compute_avg_monthly_difference(time_series)
#
            #self.assertEqual(results[0], 1)
            #self.assertEqual(results[1], 2)
            #self.assertEqual(results[2], 2)
#
            #global score; score += 2 # Increase score
#


    #===================================================
    # Due anni uno con valori mancanti 
    #===================================================

    def test_correctness_edge_cases_1(self):
        with tempfile.NamedTemporaryFile('w+t') as file:

            file.write('date,passengers\n')

            # First year
            file.write('1949-01,112\n')
            file.write('1949-02,118\n')
            file.write('1949-04,129\n')
            file.write('1949-05,121\n')
            file.write('1949-06,135\n')
            file.write('1949-08,148\n')
            file.write('1949-09,136\n')
            file.write('1949-10,119\n')
            file.write('1949-11,104\n')
            file.write('1949-12,118\n')

            # Second year
            file.write('1950-01,115\n')
            file.write('1950-02,126\n')
            file.write('1950-04,135\n')
            file.write('1950-05,125\n')
            file.write('1950-06,149\n')
            file.write('1950-07,170\n')
            file.write('1950-08,170\n')
            file.write('1950-10,133\n')
            file.write('1950-11,114\n')
            file.write('1950-12,140\n')

            # Torno all'inizio del file
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()
            results = compute_avg_monthly_difference(time_series, "1949" ,"1950")

            self.assertEqual(results[2], 0)
            self.assertEqual(results[6], 0)
            self.assertEqual(results[8], 0)
            self.assertNotEqual(results[11], 0)

            global score; score += 2 # Increase score

    #===================================================
    #  Test che ci sia la variabile "name" nell'init
    #===================================================

    def test_csv_file_interface(self):

        with tempfile.NamedTemporaryFile('w+t') as file:

            # First year
            file.write('date,passengers\n')
            file.write('1949-01,112\n')
            file.write('1949-02,118\n')
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(name = file.name)
            time_series = time_series_file.get_data()

            # Test su lunghezze
            self.assertTrue(len(time_series) in [1,2])

            global score; score += 0.5 # Increase score

    #===================================================
    #  Test su errori esistenza e tipo del nome del file
    #===================================================

    def test_csv_file_interface_nonexisttent_file(self):

        with self.assertRaises(ExamException):
            time_series_file = CSVTimeSeriesFile(name='file_non_esistente.csv')
            time_series_file.get_data()

        global score; score += 0.5 # Increase score

    def test_csv_file_interface_wrong_type(self):

        with self.assertRaises(ExamException):
            time_series_file = CSVTimeSeriesFile(name=[])
            time_series_file.get_data()

        with self.assertRaises(ExamException):
            time_series_file = CSVTimeSeriesFile(name=None)
            time_series_file.get_data()

        global score; score += 0.5 # Increase score

    def test_csv_file_empty(self):

        with tempfile.NamedTemporaryFile('w+t') as file:

            # Scrivo i contenuti nel file di test
            file.write('date,passengers\n')


            time_series_file = CSVTimeSeriesFile(file.name)

            try:
                time_series = time_series_file.get_data()
            except ExamException:
                pass

            global score; score += 0.5 # Increase score

    #======================================================
    #  Test su varie cose da gestire riguardo ai passeggeri
    #======================================================

    def test_csv_file_passengers_floating_point(self):

        with tempfile.NamedTemporaryFile('w+t') as file:

            # Scrivo i contenuti nel file di test
            file.write('date,passengers\n')

            file.write('1949-01,112.1232\n')  # Epoch floating point
            file.write('1949-02,-1213\n')  # Epoch floating point
            file.write('1949-03, 100\n')  # Epoch floating point
            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()

            # Test su lunghezza ed elementi con passengers arrotondato correttamente
            self.assertTrue(len(time_series), 1)
            self.assertEqual(time_series[0], ['1949-03', 100])

            global score; score += 1 # Increase score

    def test_csv_file_date_unordered(self):

        with tempfile.NamedTemporaryFile('w+t') as file:

            # Scrivo i contenuti nel file di test
            date = datetime.datetime.strptime('1950-01', '%Y-%m')

            file.write('date,passengers\n')

            for i in range(30):
                file.write('{:%Y-%m},{}\n'.format(date, (i+1)))
                date = date + datetime.timedelta(days= 31)
            file.write('1949-03,132\n') # Un timestamp epoch non valido

            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)

            with self.assertRaises(ExamException):
                time_series_file.get_data()

            global score; score += 1 # Increase score

    def test_csv_file_date_duplicates(self):

        with tempfile.NamedTemporaryFile('w+t') as file:

            date = datetime.datetime.strptime('1950-01', '%Y-%m')

            # Scrivo i contenuti nel file di test
            file.write('date,passengers\n')

            for i in range(30):
                file.write('{:%Y-%m},{}\n'.format(date, (i+1)))
                date = date + datetime.timedelta(days= 31)
            file.write('1950-01,12131\n') # Un timestamp epoch non valido

            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)

            with self.assertRaises(ExamException):
                time_series_file.get_data()

            time_series_file = CSVTimeSeriesFile(file.name)

            with self.assertRaises(ExamException):
                time_series_file.get_data()

            global score; score += 1 # Increase score

    #===================================================
    #  Test su vari contenuti del file CSV sporcati
    #===================================================

    def test_csv_file_dirty_1(self):

        with tempfile.NamedTemporaryFile('w+t') as file:

            date = datetime.datetime.strptime('1950-01', '%Y-%m')

            # Scrivo i contenuti nel file di test
            file.write('date,passengers\n')

            for i in range(30):
                file.write('{:%Y-%m},{},HELLOOOOOOOWOOORLDDDDDDDDD\n\n'.format(date, (i+1)))
                date += datetime.timedelta(days=31)

            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()

            date = date + datetime.timedelta(days= -31)
            test = datetime.datetime.strftime(date, "%Y-%m")
            # Test su lunghezza e ultimo elemento
            self.assertEqual(len(time_series), 30)
            self.assertEqual(time_series[29], [test,30])

            global score; score += 0.5 # Increase score

    def test_csv_file_dirty_2(self):

        with tempfile.NamedTemporaryFile('w+t') as file:

            date = datetime.datetime.strptime('1950-01', '%Y-%m')

            # Scrivo i contenuti nel file di test
            file.write('date,passengers\n')

            for i in range(30):
                file.write('{:%Y-%m},{}\n'.format(date, (i+1)))
                file.write('\n') # Righe vuote in mezzo
                file.write('Nel mezzo del cammin di nostra vita\n')  # Righe di testo senza senso in mezzo
                file.write('mi son imbattuto in un test un po\' fastisioso\n')  # Righe di testo senza senso in mezzo (2)
                date = date + datetime.timedelta(days= 31)

            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()

            date = date + datetime.timedelta(days= -31)
            test = datetime.datetime.strftime(date, "%Y-%m")
            # Test su lunghezza e ultimo elemento
            self.assertEqual(len(time_series), 30)
            self.assertEqual(time_series[29], [test,30])

            global score; score += 0.5 # Increase score

    def test_csv_file_dirty_3(self):

        with tempfile.NamedTemporaryFile('w+t') as file:

            date = datetime.datetime.strptime('1950-01', '%Y-%m')

            # Scrivo i contenuti nel file di test
            file.write('date,passengers\n')

            for i in range(30):
                file.write('{:%Y-%m},{}\n'.format(date, (i+1)))
                date = date + datetime.timedelta(days= 31)
                file.write('{:%Y-%m},SonoUnaTemperaturaNonValidaComeNumero\n'.format(date)) # Una temperature non valida
                date = date + datetime.timedelta(days= 31)
            # Non cambio il valore chi se ne frega 

            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()

            date = date + datetime.timedelta(days= -62)
            test = datetime.datetime.strftime(date, "%Y-%m")

            # Test su lunghezza e ultimo elemento
            self.assertEqual(len(time_series), 30)
            self.assertEqual(time_series[29], [test,30])

            global score; score += 0.5 # Increase score


    def test_csv_file_dirty_4(self):

        with tempfile.NamedTemporaryFile('w+t') as file:

            date = datetime.datetime.strptime('1950-01', '%Y-%m')

            # Scrivo i contenuti nel file di test
            file.write('date,passengers\n')

            for i in range(30):
                file.write('{:%Y-%m},{}\n'.format(date, (i+1)))
                file.write('SonoUnaEpochNonValidaComeNumero,134\n') # Un timestamp passengers non valido
                date = date + datetime.timedelta(days= 31)

            file.seek(0)

            time_series_file = CSVTimeSeriesFile(file.name)
            time_series = time_series_file.get_data()

            date = date + datetime.timedelta(days= -31)
            test = datetime.datetime.strftime(date, "%Y-%m")

            self.assertEqual(len(time_series), 30)
            self.assertEqual(time_series[29], [test,30])

            global score; score += 0.5 # Increase score

    # Print the score
    @classmethod
    def tearDownClass(cls):
        global score

        print('\n\n----------------')
        print('| Voto: {}/28 |'.format(score))
        print('----------------\n')

# Run the tests
unittest.main()

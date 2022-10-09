from threading import Thread
import Tables, Setings


tables = [Tables.TableClass(i) for i in range(Setings.nr_of_tables)]
def tables_init():
    for i in range(Setings.nr_of_tables):
        tables[i].start()

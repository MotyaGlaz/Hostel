import pandas as pd
import sqlite3

con = sqlite3.connect('Hostel.sqlite')


def create_Hostel():
    f_damp = open('Hostel.sql', 'r', encoding='utf-8-sig')
    damp = f_damp.read()
    f_damp.close()

    con.executescript(damp)
    con.commit()


# =====____=====
create_Hostel()

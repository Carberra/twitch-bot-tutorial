from sqlite3 import connect
import tetueSrc

try:
    DATABASE = tetueSrc.get_string_element("paths", "database")
    cxn = connect(DATABASE, check_same_thread=False)
except:
    DATABASEGEN = tetueSrc.get_string_element("paths", "database_gen")
    cxn = connect(DATABASEGEN, check_same_thread=False)
cur = cxn.cursor()


def with_commit(func):
    def inner(*args, **kwargs):
        func(*args, **kwargs)
        commit()
    return inner


@with_commit
def build():
    scriptexec("./files/script.sql")


def commit():
    cxn.commit()


def close():
    cxn.close()


def field(command, *values):
    '''Gibt nur das erste Element einer Abfrage für z.B. eines Users zurück.
    Beispiel: "SELECT Warnings, Coins FROM users WHERE CountLogins = ?", 2
    Rückgabe: Warnings <int>'''
    cur.execute(command, tuple(values))
    if (fetch := cur.fetchone()) is not None:
        return fetch[0]


def record(command, *values):
    '''Gibt alle Element einer Abfrage für z.B. eines Users zurück.
    Beispiel: "SELECT Warnings, Coins FROM users WHERE CountLogins = ?", 2
    Rückgabe: Warnings, Coins <tuple>'''
    cur.execute(command, tuple(values))
    return cur.fetchone()


def records(command, *values):
    '''Gibt alle Element einer Abfrage für z.B. alle Users zurück.
    Beispiel: "SELECT Warnings, Coins FROM users WHERE CountLogins = ?", 2
    Rückgabe: [(Warnings, Coins), (Warnings, Coins), ...]'''
    cur.execute(command, tuple(values))
    return cur.fetchall()


def column(command, *values):
    ''' Gibt ein Element einer Abfrage für z.B. alle Users zurück.
    Beispiel: "SELECT Coins FROM users WHERE CountLogins = ?", 2
    Rückgabe: [Coins, Coins, ...]'''
    cur.execute(command, tuple(values))
    return [item[0] for item in cur.fetchall()]


def execute(command, *values):
    cur.execute(command, tuple(values))


def mutliexec(command, valueset):
    cur.executemany(command, valueset)


def scriptexec(filename):
    with open(filename, "r") as script:
        cur.executescript(script.read())
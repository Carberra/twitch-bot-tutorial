from sqlite3 import connect

cxn = connect("./files/database.db", check_same_thread=False)
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
	cur.execute(command, tuple(values))
	if (fetch := cur.fetchone()) is not None:
		return fetch[0]


def record(command, *values):
	cur.execute(command, tuple(values))
	return cur.fetchone()


def records(command, *values):
	cur.execute(command, tuple(values))
	return cur.fetchall()


def column(command, *values):
	cur.execute(command, tuple(values))
	return [item[0] for item in cur.fetchall()]


def execute(command, *values):
	cur.execute(command, tuple(values))


def mutliexec(command, valueset):
	cur.executemany(command, valueset)


def scriptexec(filename):
	with open(filename, "r") as script:
		cur.executescript(script.read())
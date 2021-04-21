CREATE TABLE IF NOT EXISTS users (
	UserID text PRIMARY KEY,
	UserName text,
	MessagesSent integer DEFAULT 0,
	CountLogins integer DEFAULT 1,
	LastLogin text DEFAULT CURRENT_TIMESTAMP,
	LoyaltyPoints integer DEFAULT 0,
	Coins integer DEFAULT 0,
	CoinLock text DEFAULT CURRENT_TIMESTAMP,
	Warnings integer DEFAULT 0,
	LostCounter integer DEFAULT 0,
	Badges text DEFAULT "Tueftlie",
	HenName text,
	KlugCounter integer DEFAULT 0
);

CREATE TABLE IF NOT EXISTS category (
	Category text PRIMARY KEY,
	Wins integer DEFAULT 0,
	Loses integer DEFAULT 0
);

CREATE TABLE IF NOT EXISTS awards (
	UserID text PRIMARY KEY,
	UserName text,
	Sporthuhn integer DEFAULT 0, -- Punkte für: Wie oft zum Sport aufgerufen
	Kampfhuhn integer DEFAULT 0, -- Punkte für: Bits pro game (game != Wissenschaft oder Basteln oder Just Chatting) (Warchicken, battlechicken)
	Tueftelhuhn integer DEFAULT 0, -- Punkte für: Bits pro Wissenschaft
	Goennerhuhn integer DEFAULT 0, -- Punkte für: Meisten Abos auf dem Kanal
	DurchgeknalltesHuhn integer DEFAULT 0, -- Punkte für: Die meisten Nachrichten (VerruecktesHuhn, Quatschhuhn)
	VerlorenesHuhn integer DEFAULT 0 -- Punkte für: die meisten Losts ()
);

CREATE TABLE IF NOT EXISTS quotes (
	Id integer PRIMARY KEY AUTOINCREMENT,
	UserID text,
	UserName text,
	QuoteDate text DEFAULT CURRENT_TIMESTAMP,
	Quote text
);
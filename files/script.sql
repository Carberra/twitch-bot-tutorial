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
	HenName text
);

CREATE TABLE IF NOT EXISTS category (
	Category text PRIMARY KEY,
	Wins integer DEFAULT 0,
	Loses integer DEFAULT 0
);
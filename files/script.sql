CREATE TABLE IF NOT EXISTS users (
	UserID text PRIMARY KEY,
	UserName text,
	MessagesSent integer DEFAULT 0,
	CountLogins integer DEFAULT 1,
	LastLogin text DEFAULT CURRENT_TIMESTAMP,
	Coins integer DEFAULT 0,
	CoinLock text DEFAULT CURRENT_TIMESTAMP,
	Warnings integer DEFAULT 0,
	LostCounter integer DEFAULT 0
);
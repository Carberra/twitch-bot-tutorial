import tetueSrc

def main():
    read_successful, cfg = tetueSrc.get_configuration("bot")
    if read_successful == True:
        print("Konfiguration erfolgreich gelesen.")
    else:
        print("Konfiguration nicht erfolgreich gelesen.")
if __name__ == "__main__":
    main()
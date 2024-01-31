from website import create_app
#importujemo create_app iz __init__.py ,
# jer je website folder python pek
#kada se stavi __init__.py postaje paket

app = create_app()

if __name__ == '__main__':  #Samo ako se runuje, a ne importuje, jer je main.
    app.run(debug=True) #pokreće sajt

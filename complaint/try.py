
if __name__ == "__main__":

    texto = "123."

    if "." in  texto:

        place_point = texto.find(".")
        print(place_point)
        decimal_places = len(texto[place_point:]) -1
        print(decimal_places)
        if decimal_places == 1 or decimal_places == 2:
            print(True) 



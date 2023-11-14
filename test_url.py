from url import create_url

def test_create_url():
    type = "mieszkania"
    city = "krakow"
    rooms = ["2 pokoje"]
    price_to = "3000"

    assert create_url(
        type = type, city = city, rooms = rooms, price_to = price_to
        ) == "https://www.olx.pl/nieruchomosci/mieszkania/krakow/?search[filter_float_price:to]=3000&search[filter_enum_rooms][0]=two"

def test_create_url2():
    type = "domy"
    city = "katowice"
    m_2_from = "10"
    m_2_to = "20"
    subcategory = "sprzedaz"

    assert create_url(
        type = type, city = city, m_2_from = m_2_from, m_2_to = m_2_to, subcategory = subcategory
        ) == "https://www.olx.pl/nieruchomosci/domy/sprzedaz/katowice/?search[filter_float_m:from]=10&search[filter_float_m:to]=20"

def test_create_url3():
    city = "poznan"
    type = "mieszkania"

    assert create_url(
        city = city, type = type
        ) == "https://www.olx.pl/nieruchomosci/mieszkania/poznan/?"

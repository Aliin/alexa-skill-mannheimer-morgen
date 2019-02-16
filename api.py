import requests


def events_api(params):
    host = "https://www2.morgenweb.de/austausch/vk_abfrage.php?out=json"
    host_params = {"ab": params["datum"], "bis": params["datum"], "rubrik": params["rubrik"], "plz": params["plz"], "ort": params["ort"], "suche": params["suche"]}
    for key, value in host_params.items():
        if value is not None:
            host += "&{}={}".format(key, value)

    r = requests.get(host)

    return r.json()["ergebnis"]

def event_detail():
    return None






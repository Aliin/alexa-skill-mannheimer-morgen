from flask import Flask, render_template
from flask_ask import Ask, statement, question, session, request, context
from datetime import datetime
import random

# Custom library
from api import events_api
import article_parser
import mock_search
import suggested_news

app = Flask(__name__)
ask = Ask(app, '/')

intro = "<audio src='soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_intro_01'/>"
outro = "<audio src='soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_outro_01'/>"
neutral_response = "<audio src='soundbank://soundlibrary/ui/gameshow/amzn_ui_sfx_gameshow_neutral_response_01'/>"
background = "https://s3-eu-west-1.amazonaws.com/werbungmoma/mm_logo_upload.png"
werbungen = ["https://s3-eu-west-1.amazonaws.com/werbungmoma/werbung1_alexa.mp3",
             "https://s3-eu-west-1.amazonaws.com/werbungmoma/werbung2_alexa.mp3",
             "https://s3-eu-west-1.amazonaws.com/werbungmoma/werbung3_alexa.mp3"]

@ask.launch
def launched():
    speech = render_template("welcome")
    respeech = render_template("welcome_respeech")
    if context.System.device.supportedInterfaces.Display is None:
        return question(speech).reprompt(respeech)
    else:
        hint = render_template("hint_launched")
        speech = render_template("welcome_display")
        text = {"primaryText": {"type": "RichText", "text": speech}}
        return question(speech).display_render(template="BodyTemplate6", text=text,
                                               background_image_url=background,
                                               hintText=hint)
    return question(speech).reprompt(respeech)

@ask.intent("NewsIntent")
def news(search):
    rubrik_default = render_template("rubrik_default")
    try:
        rubrik = request["intent"]["slots"]["nachrichten_rubrik"]["resolutions"]["resolutionsPerAuthority"][0]["values"][0]["value"]["name"]
    except:
        rubrik = rubrik_default
    try:
        if search:
            news_raw_data = mock_search.MockSearch(search, session.user.userId).mock_result()
        else:
            news_raw_data = article_parser.FeedReader(rubrik, 4).results()
        news = create_string_of(news_raw_data)
        speech = render_template("news", news=news)
        if context.System.device.supportedInterfaces.Display is None:
            return statement(speech)
        else:
            title = render_template("title_news")
            items = get_news_items(news_raw_data)
            return statement(speech).list_display_render(template="ListTemplate1", backButton="HIDDEN", title=title,
                                                         listItems=items)
    except:
        speech = render_template("no_news_found")
        if context.System.device.supportedInterfaces.Display is None:
            return statement(speech)
        else:
            text = {"primaryText": {"type": "RichText", "text": speech}}
            return statement(speech).display_render(template="BodyTemplate6",
                                                    text=text, background_image_url=background)

@ask.intent("EventsIntent")
def events(datum, plz, ort, suche):
    try:
        rubrik = request["intent"]["slots"]["rubrik"]["resolutions"]["resolutionsPerAuthority"][0]["values"][0]["value"]["name"]
    except:
        rubrik = None
    params = {"datum": datum, "rubrik": rubrik, "plz": plz, "ort": ort, "suche": suche}
    try:
        events_raw_data = events_api(params)
        session_create(state="events", params=params, count=4)
        events = iterate(events_raw_data)
        speech = render_template("events", events=events["string"])
        respeech = render_template("events_respeech")
        if context.System.device.supportedInterfaces.Display is None:
            return question(speech).reprompt(respeech)
        else:
            title = render_template("title_events")
            items = get_items(events)
            return question(speech).list_display_render(template="ListTemplate1", backButton="HIDDEN",
                                                        title=title, listItems=items).reprompt(respeech)
    except:
        speech = render_template("no_events_found")
        if context.System.device.supportedInterfaces.Display is None:
            return statement(speech)
        else:
            text = {"primaryText": {"type": "RichText", "text": speech}}
            return statement(speech).display_render(template="BodyTemplate6",
                                                    text=text, background_image_url=background)

@ask.intent("SuggestionIntent")
def suggestion():
    news_raw_data = suggested_news.SuggestedNews(session.user.userId).mock_result()
    if news_raw_data:
        news = create_string_of(news_raw_data)
        speech = render_template("news", news=news)
    else:
        speech = render_template("no_suggestions")
    return statement(speech)

@ask.intent("AMAZON.YesIntent")
def yes():
    try:
        if session.attributes["state"] == "end_of_data":
            speech = render_template("all_entries")
            if context.System.device.supportedInterfaces.Display is None:
                return statement(speech)
            else:
                text = {"primaryText": {"type": "RichText", "text": speech}}
                return statement(speech).display_render(template="BodyTemplate6", text=text,
                                                        background_image_url=background)
        if session.attributes["state"] == "events":
            event_raw_data = events_api(session.attributes["params"])
            for index in range(0, session.attributes['count']):
                try:
                    event_raw_data.pop(0)
                except:
                    session.attributes["state"] = "end_of_data"
            events = iterate(event_raw_data)
            speech = render_template("events", events=events["string"])
            respeech = render_template("events_respeech")
            if session.attributes["state"] == "end_of_data":
                if context.System.device.supportedInterfaces.Display is None:
                    return statement(speech)
                else:
                    title = render_template("title_events")
                    items = get_items(events)
                    return statement(speech).list_display_render(template="ListTemplate1", backButton="HIDDEN",
                                                                 title=title, listItems=items)
            else:
                if context.System.device.supportedInterfaces.Display is None:
                    return question(speech).reprompt(respeech)
                else:
                    title = render_template("title_events")
                    items = get_items(events)
                    return question(speech).list_display_render(template="ListTemplate1", backButton="HIDDEN",
                                                                title=title, listItems=items).reprompt(respeech)
    except:
        speech = render_template("error")
        if context.System.device.supportedInterfaces.Display is None:
            return statement(speech)
        else:
            text = {"primaryText": {"type": "RichText", "text": speech}}
            return statement(speech).display_render(template="BodyTemplate6",
                                                    text=text, background_image_url=background)

@ask.intent("AMAZON.NoIntent")
def no():
    session_delete()
    speech = render_template("bye")
    if context.System.device.supportedInterfaces.Display is None:
        return statement(speech)
    else:
        text = {"primaryText": {"type": "RichText", "text": speech}}
        return statement(speech).display_render(template="BodyTemplate6", text=text, background_image_url=background)

@ask.intent("AMAZON.FallbackIntent")
def fallback():
    speech = render_template("fallback")
    respeech = render_template("fallback_respeech")
    return question(speech).reprompt(respeech)

@ask.intent("AMAZON.CancelIntent")
def cancel():
    speech = render_template("cancel")
    return statement(speech)

@ask.intent("AMAZON.StopIntent")
def stop():
    speech = render_template("stop")
    return statement(speech)

@ask.intent("AMAZON.HelpIntent")
def help():
    speech = render_template("help")
    respeech = render_template("help_respeech")
    return question(speech).reprompt(respeech)

def get_werbung():
    ad = werbungen[random.randint(0, len(werbungen)-1)]
    werbung = "<audio src='{}' />".format(ad)
    return werbung

def get_news_items(news):
    items = []
    for new in news:
        textcontent = {"secondaryText": {"type": "RichText", "text": new["title"]}}
        item = {"textContent": textcontent}
        items.append(item)
    return items

def get_items(events):
    items = []
    for key, event in events["liste"].items():
        beginnt = datetime.strptime(event["beginnt"], '%Y-%m-%d %H:%M:%S')
        if beginnt.minute == 0:
            minute = "00"
        else:
            minute = beginnt.minute
        textcontent = {"primaryText": {"type": "RichText", "text": event["name_titel"]},
                       "secondaryText": {"type": "RichText",
                                         "text": "{} in {} {}, {} {}".format(event["veranstalter"], event["strasse"],
                                                                             event["hausnummer"], event["plz"],
                                                                             event["stadt"])},
                       "tertiaryText": {"type": "RichText", "text": "{}:{}".format(beginnt.hour, minute)}}
        item = {"textContent": textcontent}
        items.append(item)
    return items

def session_create(state, params, count):
    session.attributes['state'] = state
    session.attributes['params'] = params
    session.attributes['count'] = count

def session_delete():
    session.attributes['state'] = ""
    session.attributes['params'] = ""
    session.attributes['count'] = ""

def create_string_of(news_raw_data):
    news = ""
    for index, new in enumerate(news_raw_data):
        if index == 0:
            news = "{} {}<break time='0.3s'/>{}".format(intro, new["title"], new["summary"])
        elif index < 3:
            news = "{} {} {}<break time='0.3s'/>{}".format(news, neutral_response, new["title"], new["summary"])
        else:
            news = "{} {} {}<break time='0.3s'/>{} {}".format(news, neutral_response, new["title"], new["summary"],
                                                              outro)
    return news

def iterate(events):
    event_werbung = get_werbung()
    four_events = {}
    event_str = ""
    for index, event in enumerate(events):
        four_events[index] = event
        if index == 0:
            event_str += "{} <break time='1s'/> Beim Veranstalter {} in {} läuft {}".format(intro,
                                                                                            event["veranstalter"],
                                                                                            event["stadt"],
                                                                                            event["name_titel"])
        elif index < 2:
            event_str += "{} <break time='1s'/> Beim Veranstalter {} in {} läuft {}".format(neutral_response,
                                                                                            event["veranstalter"],
                                                                                            event["stadt"],
                                                                                            event["name_titel"])
        else:
            session.attributes["count"] += 3
            if session.attributes['state'] == "end_of_data":
                event_str += "{} <break time='1s'/> Beim Veranstalter {} in {} läuft {} <break time='0.5s'/> " \
                             "Werbung {} {}".format(neutral_response, event["veranstalter"], event["stadt"],
                                                    event["name_titel"], event_werbung, outro)
                break
            else:
                event_str += "{} <break time='1s'/> Beim Veranstalter {} in {} läuft {} <break time='0.5s'/> " \
                             "Werbung {} {} Möchtest Du noch mehr hören?".format(neutral_response,
                                                                                 event["veranstalter"], event["stadt"],
                                                                                 event["name_titel"], event_werbung,
                                                                                 outro)
                break
    return {"string": event_str, "liste": four_events}

if __name__ == '__main__':
    app.run(debug=True)



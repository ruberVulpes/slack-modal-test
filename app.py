import os
from threading import Thread

from flask import Flask, make_response, request
from slack import WebClient
from slack.web.classes.interactions import SlashCommandInteractiveEvent
from slack.web.classes import views
from slack.web.classes.blocks import InputBlock
from slack.web.classes.elements import PlainTextInputElement, PlainTextObject

slack_client = WebClient(os.environ["SLACK_BOT_TOKEN"])
flask_app = Flask(__name__)


@flask_app.route("/slack/interactions", methods=["POST"])
def interactions():
    # Do nothing with the submission
    return make_response("", 200)


@flask_app.route("/slack/commands/modal", methods=["POST"])
def modal_post():
    command = SlashCommandInteractiveEvent(request.form)
    Thread(target=open_modal, args=(command, )).start()
    return make_response("", 200)


def open_modal(command: SlashCommandInteractiveEvent):
    title = PlainTextObject(text="Color Survey")
    color_input_blocks = [InputBlock(label=PlainTextObject(text="What is your favorite color?"),
                                     element=PlainTextInputElement(placeholder="Green")),
                          InputBlock(label=PlainTextObject(text="Why is that your favorite color?"),
                                     element=PlainTextInputElement(placeholder="It reminds me of my childhood home"),
                                     optional=True)]
    modal = views.View(type="modal", title=title, blocks=color_input_blocks, submit="Submit")
    slack_client.views_open(trigger_id=command.trigger_id, view=modal)


if __name__ == '__main__':
    flask_app.run(port=5000)

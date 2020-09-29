from django.http import HttpResponse


class StripeWH_Handler:
    """handle stripe webhooks """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """ handle any stripe wh events and return recieved http response """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
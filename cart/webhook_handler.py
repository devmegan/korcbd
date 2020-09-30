from django.http import HttpResponse


class StripeWH_Handler:
    """handle stripe webhooks """

    def __init__(self, request):
        self.request = request

    def handle_event(self, event):
        """ handle any generic/unknown stripe wh events """
        return HttpResponse(
            content=f'Unhandled webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """ handle payment_intent.succeeded stripe wh event """
        intent = event.data.object
        print(intent)
        return HttpResponse(
            content=f'Payment successful webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """ handle payment_intent.payment_failed stripe wh event """
        return HttpResponse(
            content=f'Payment failed webhook received: {event["type"]}',
            status=200)

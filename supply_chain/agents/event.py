class Event:
    def __init__(self, event_type, event_time, event_location, event_description,price):
        self.event_type = event_type
        self.event_time = event_time
        self.event_location = event_location
        self.event_description = event_description
        self.price =price

    def __str__(self):
        return f"Event type: {self.event_type}, Time: {self.event_time}, Location: {self.event_location}, Description: {self.event_description}"
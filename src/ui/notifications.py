class NotificationManager:
    def __init__(self, duration=3.0):
        self.notifications = []
        self.default_duration = duration

    def add(self, text, color=(255, 255, 255)):
        self.notifications.append({
            "text": text,
            "timer": self.default_duration,
            "color": color
        })

    def update(self, dt):
        for notif in self.notifications[:]:
            notif["timer"] -= dt
            if notif["timer"] <= 0:
                self.notifications.remove(notif)

    def on_quest_updated(self, data):
        name = data.get("name", "Missão")
        desc = data.get("description", "Objetivo atualizado")
        self.add(f"Atualizado: {name}", color=(0, 255, 255))
        self.add(f"> {desc}", color=(200, 200, 200))

    def on_quest_completed(self, data):
        name = data.get("name", "Missão")
        self.add(f"CONCLUÍDO: {name}!", color=(0, 255, 0))

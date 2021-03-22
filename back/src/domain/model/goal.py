class Goal:
    def __init__(self, id, date, title, category, status, user_id):
        self.id = id
        self.date = date
        self.title = title
        self.category = category
        self.status = bool(status)
        self.user_id = user_id

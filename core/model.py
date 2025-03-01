class Model:
    def __init__(self, **properties):
        self.name = properties["name"]
        self.model = properties["model"]
        self.description = properties["description"]
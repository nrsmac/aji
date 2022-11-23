class Recipe:
    def __init__(self, title, author, servings, description, prep_time, ingredients, url):
        self.title = title
        self.author = author
        self.description = description
        self.servings = servings
        self.prep_time = prep_time
        self.ingredients = ingredients
        self.url = url

    def __str__(self):
        return f"{self.title}\n{self.servings}\n{self.description}\n{self.prep_time}\n{self.ingredients}\n{self.url}"

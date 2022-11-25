import requests
from bs4 import BeautifulSoup

class Recipe:
    def __init__(self, title, author, servings, description, prep_time, ingredients, url):
        self.title = title
        self.author = author
        self.description = description
        self.servings = servings
        self.prep_time = prep_time
        self.ingredients = ingredients
        self.url = url
    
    def __init__(self, url):
        self.url = url
        self._scrape_from_url()

    def _get_ingredients(self, soup):
        #TODO check if it has multiple sub-ingredients. This works, but doesn't if there are NO subingredients in teh case of: https://cooking.nytimes.com/recipes/1022732-ultimate-pumpkin-pie?module=Recipe+of+The+Day&pgType=homepage&action=click
        ingredients_section = soup.select('div[class*="ingredients"]')
        ingredients_group_names = [s.get_text() for s in soup.select('h3[class*="ingredientgroup_name"]')]
        ingredients_groups = [g for g in soup.select('ul[class*="ingredientgroup_subIngredients"]')]
        ingredients_groups = zip(ingredients_group_names, [i for i in ingredients_groups])

        return {name:[i.get_text() for i in ig] for name, ig in ingredients_groups}

    def _scrape_from_url(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")

        self.title = soup.select_one('h1[class*="contenttitle"]').get_text()
        self.author = soup.select_one('div[class*="recipeintro"]').select_one('h2').get_text().removeprefix('By ')
        self.description = soup.select_one('div[class*="cheltBody"]').get_text()
        self.servings = soup.select_one('div[class*="recipeYield"]').get_text()
        self.prep_time = soup.select_one('dl[class*="stats"]').select_one('dd').get_text()
        self.ingredients = self._get_ingredients(soup)


    def __repr__(self):
        return f"{self.title}\n{self.servings}\n{self.description}\n{self.prep_time}\n{self.ingredients}\n{self.url}"

    def __str__(self):
        return f"{self.title}\n{self.servings}\n{self.description}\n{self.prep_time}\n{self.ingredients}\n{self.url}"

if __name__ == "__main__":
    recipe = Recipe("https://cooking.nytimes.com/recipes/1022732-ultimate-pumpkin-pie?module=Recipe+of+The+Day&pgType=homepage&action=click")
    print(recipe)

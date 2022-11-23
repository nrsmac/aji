import requests
from bs4 import BeautifulSoup
from recipe import Recipe

URL = "https://cooking.nytimes.com/recipes/1021963-whole-roasted-cauliflower-with-pistachio-pesto?action=click&module=RecipeBox&pgType=recipebox-page&region=all&rank=0"
page = requests.get(URL)

soup = BeautifulSoup(page.content, "html.parser")

title = soup.select_one('h1[class*="contenttitle"]').get_text()
author = soup.select_one('div[class*="recipeintro"]').select_one('h2').get_text().removeprefix('By ')
description = soup.select_one('div[class*="cheltBody"]').get_text()
servings = soup.select_one('div[class*="recipeYield"]').get_text()
prep_time = soup.select_one('dl[class*="stats"]').select_one('dd').get_text()

#TODO check if it has multiple sub-ingredients. This works, but doesn't if there are NO subingredients in teh case of: https://cooking.nytimes.com/recipes/1022732-ultimate-pumpkin-pie?module=Recipe+of+The+Day&pgType=homepage&action=click
def get_ingredients(soup):
    ingredients_section = soup.select('div[class*="ingredients"]')
    ingredients_group_names = [s.get_text() for s in soup.select('h3[class*="ingredientgroup_name"]')]
    ingredients_groups = [g for g in soup.select('ul[class*="ingredientgroup_subIngredients"]')]
    ingredients_groups = zip(ingredients_group_names, [i for i in ingredients_groups])

    return {name:[i.get_text() for i in ig] for name, ig in ingredients_groups}

ingredients = get_ingredients(soup)

recipe = Recipe(title, author, servings, description, prep_time, ingredients, URL)
print(recipe)


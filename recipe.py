#!/usr/bin/env python
import requests
import markdown
from pprint import pprint
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
        '''
        Returns [] or {} if has multiple sub-ingredients grouped on parts of a dish. 
        '''
        ingredients_group_names = [s.get_text() for s in soup.select('h3[class*="ingredientgroup_name"]')]
        if ingredients_group_names:
            ingredients_groups = [g for g in soup.select('ul[class*="ingredientgroup_subIngredients"]')]
            ingredients_groups = zip(ingredients_group_names, [i for i in ingredients_groups])

            return {name:[i.get_text() for i in ig] for name, ig in ingredients_groups}
        else:
            ingredients_li = [i for i in soup.select('div[class*="ingredients"] ul li')]
            return [i.get_text() for i in ingredients_li] 
        
    def _get_steps(self, soup):
        steps_text = [s.get_text() for s in soup.select('ol[class*="preparation"] li p')]
        return list(zip(range(1, len(steps_text)+1), steps_text)) 
            
    def get_markdown(self):
        # TODO: html output with markdown library

        # Get ingredients string
        if type(self.ingredients) is list:
            ingredients = "* "+"* ".join([f'{i}\n' for i in self.ingredients])
        else:  # Dictionary with sub-ingredients 
            ingredients = ""
            for k, v in self.ingredients.items():
                ingredients += f"{k}:\n* "
                assert type(v) is list
                ingredients += "* ".join([f'{i}\n' for i in v])
                # ingredients += '\n' 
           
        # Get steps string 
        steps = "".join([f'{i}. {s}\n' for i,s in self.steps]) 

        # Populate final string
        recipe = \
            f"""# {self.title}
BY: {self.author}
PREP TIME: {self.prep_time}
{self.servings}
## Ingredients:
{ingredients}
## Directions:
{steps}
"""
        return recipe


    def _scrape_from_url(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, "html.parser")

        self.title = soup.select_one('h1[class*="contenttitle"]').get_text()
        self.author = soup.select_one('div[class*="recipeintro"]').select_one('h2').get_text().removeprefix('By ')
        self.description = soup.select_one('div[class*="cheltBody"]').get_text()
        self.servings = soup.select_one('div[class*="recipeYield"]').get_text()
        self.prep_time = soup.select_one('dl[class*="stats"]').select_one('dd').get_text()
        self.ingredients = self._get_ingredients(soup)
        self.steps = self._get_steps(soup)

    def export(self, outdir, format='md'): 
        with open(f'{outdir}/{self.title}.{format}', 'w') as f:
            if format=='md':
                f.write(self.get_markdown())
            elif format=='html':
                f.write(markdown.markdown(self.get_markdown()))

    def __repr__(self):
        #TODO make prettier
        return f"{self.title}"

    def __str__(self):
        #TODO make prettier
        return f"{self.title}"

if __name__ == "__main__":
    # recipe = Recipe("https://cooking.nytimes.com/recipes/1022732-ultimate-pumpkin-pie?module=Recipe+of+The+Day&pgType=homepage&action=click")
    # recipe = Recipe.from_url("https://cooking.nytimes.com/recipes/1020929-vegan-lasagna")
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="url of NYT Cookint Recipe")
    parser.add_argument("-o", "--output", default='./', help="output directory of HTML")
    parser.add_argument("--format", default="md", help="md or html")
    args = parser.parse_args()

    recipe = Recipe(args.url)

        
     
    recipe.export(f'./{args.output}', format=args.format)

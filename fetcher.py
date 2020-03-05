from bs4 import BeautifulSoup
import requests
from pprint import pprint

from transforms import to_thai_cuisine

class RecipeFetcher:

    search_base_url = 'https://www.allrecipes.com/search/results/?wt=%s&sort=re'

    def search_recipes(self, keywords): 
        search_url = self.search_base_url % (keywords.replace(' ', '+'))

        page_html = requests.get(search_url)
        page_graph = BeautifulSoup(page_html.content)

        return [recipe.a['href'] for recipe in\
               page_graph.find_all('div', {'class':'grid-card-image-container'})]

    def scrape_recipe(self, recipe_url):
        if '/?' in recipe_url:
          i = recipe_url.index('/?')
          recipe_url = recipe_url[:i + 1]
          
        results = {}

        page_html = requests.get(recipe_url)
        page_graph = BeautifulSoup(page_html.content)

        results['ingredients'] = [ingredient.text for ingredient in\
                                  page_graph.find_all('span', {'itemprop':'recipeIngredient'})]

        results['directions'] = [direction.text.strip() for direction in\
                                 page_graph.find_all('span', {'class':'recipe-directions__list--item'})
                                 if direction.text.strip()]

        results['nutrition'] = self.scrape_nutrition_facts(recipe_url)

        return results
    
    def scrape_nutrition_facts(self, recipe_url):
        results = []

        nutrition_facts_url = '%s/fullrecipenutrition' % (recipe_url)

        page_html = requests.get(nutrition_facts_url)
        page_graph = BeautifulSoup(page_html.content)

        for nutrient_row in page_graph.find_all('div', {'class':'nutrition-row'}):
            nutrient = {}

            nutrient_info = nutrient_row.text.split()
            if nutrient_info[-1] == '%':
              dv_len = 2
              if '>' in nutrient_row.text or '<' in nutrient_row.text:
                dv_len = 3
              nutrient['name'] = ' '.join(nutrient_info[:-(dv_len + 1)])[:-1]
              first_index = -1
              for i in range(len(nutrient_info[-(dv_len + 1)])):
                if ord(nutrient_info[-(dv_len + 1)][i]) > 57:
                  first_index = i
                  break
              nutrient['amount'] = nutrient_info[-(dv_len + 1)][:first_index]
              nutrient['unit'] = nutrient_info[-(dv_len + 1)][first_index:]
              nutrient['daily_value'] = ' '.join(nutrient_info[-dv_len:])
            else:
              nutrient['name'] = ' '.join(nutrient_info[:-1])[:-1]
              first_index = -1
              for i in range(len(nutrient_info[-1])):
                if ord(nutrient_info[-1][i]) > 57:
                  first_index = i
                  break
              nutrient['amount'] = nutrient_info[-1][:first_index]
              nutrient['unit'] = nutrient_info[-1][first_index:]
              nutrient['daily_value'] = None

            results.append(nutrient)

        return results

if __name__ == '__main__':
  rf = RecipeFetcher()
  meat_lasagna = rf.search_recipes('meat lasagna')[0]
  recipe_data = rf.scrape_recipe(meat_lasagna)
  
  print(recipe_data)
  
  # pprint(to_thai_cuisine.transform_to_thai(recipe_data))
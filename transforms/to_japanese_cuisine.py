def transform_to_japanese(recipe_data):
    results = {}

    ingredients = []
    for ingredient in recipe_data['ingredients']:
        new_ingredient = dict(ingredient)
        if 'sauce' in new_ingredient['name'] and not 'soy' in new_ingredient['name']:
            new_ingredient['name'] = 'teriyaki sauce'
        elif 'cheese' in new_ingredient['name']:
            new_ingredient['name'] = 'Sakura cheese'
        elif 'mushrooms' in new_ingredient['name']:
            new_ingredient['name'] = 'shiitake mushrooms'
        elif 'wine' in new_ingredient['name'] or 'whisky' in new_ingredient['name'] or 'vodka' in new_ingredient['name']:
            new_ingredient['name'] = 'sake'
        ingredients.append(new_ingredient)
    results['ingredients'] = ingredients

    directions = []
    for direction in recipe_data['directions']:
        new_direction = dict(direction)
        new_ingredients = []
        for ingredient in new_direction['ingredients']:
            if 'sauce' in ingredient and not 'soy' in ingredient:
                new_direction['text'] = new_direction['text'].replace(ingredient, 'teriyaki sauce')
                new_ingredients.append('teriyaki sauce')
            elif 'cheese' in ingredient:
                new_direction['text'] = new_direction['text'].replace(ingredient, 'Sakura cheese')
                new_ingredients.append('Sakura cheese')
            elif 'mushrooms' in ingredient:
                new_direction['text'] = new_direction['text'].replace(ingredient, 'shiitake mushrooms')
                new_ingredients.append('shiitake mushrooms')
            elif 'wine' in ingredient or 'whisky' in new_ingredient['name'] or 'vodka' in new_ingredient['name']:
                new_direction['text'] = new_direction['text'].replace(ingredient, 'sake')
                new_ingredients.append('sake')
            else:
                new_ingredients.append(ingredient)
        new_ingredients = list(set(new_ingredients))
        new_direction['ingredients'] = new_ingredients
        directions.append(new_direction)
    results['directions'] = directions

    results['nutrition'] = recipe_data['nutrition']

    return results


if __name__ == '__main__':    
    example = {
        'ingredients': [
            {'name': 'whole wheat lasagna noodles', 'quantity': 12, 'measurement': None, 'descriptor': None, 'preparation': None},
            {'name': 'ground beef', 'quantity': 1, 'measurement': 'pound', 'descriptor': 'lean', 'preparation': None},
            {'name': 'garlic', 'quantity': 2, 'measurement': 'cloves', 'descriptor': None, 'preparation': 'chopped'},
            {'name': 'garlic powder', 'quantity': 0.5, 'measurement': 'teaspoon', 'descriptor': None, 'preparation': None},
            {'name': 'oregano', 'quantity': 1, 'measurement': 'teaspoon or to taste', 'descriptor': 'dried', 'preparation': None},
            {'name': 'salt and ground black pepper', 'quantity': None, 'measurement': 'to taste', 'descriptor': None, 'preparation': None},
            {'name': 'cottage cheese', 'quantity': 1, 'measurement': '(16 ounce) package', 'descriptor': None, 'preparation': None},
            {'name': 'eggs', 'quantity': 2, 'measurement': None, 'descriptor': None, 'preparation': None},
            {'name': 'Parmesan cheese', 'quantity': 0.5, 'measurement': 'cup', 'descriptor': None, 'preparation': 'shredded'},
            {'name': 'tomato-basil pasta sauce', 'quantity': 1.5, 'measurement': '(25 ounce) jars', 'descriptor': None, 'preparation': None},
            {'name': 'mozzarella cheese', 'quantity': 2, 'measurement': 'cups', 'descriptor': None, 'preparation': 'shredded'}],
        'directions': [
            {'text': 'Preheat oven to 350 degrees F (175 degrees C).', 
             'ingredients': [], 'tools': ['oven'], 'methods': [], 'times': []},
            {'text': 'Fill a large pot with lightly salted water and bring to a rolling boil over high heat. Once the water is boiling, add the lasagna noodles a few at a time, and return to a boil. Cook the pasta uncovered, stirring occasionally, until the pasta has cooked through, but is still firm to the bite, about 10 minutes. Remove the noodles to a plate.', 
             'ingredients': ['lasagna noodles', 'pasta', 'noodles'], 'tools': ['pot', 'plate'], 'methods': ['stirring'], 'times': ['10 minutes']},
            {'text': 'Place the ground beef into a skillet over medium heat, add the garlic, garlic powder, oregano, salt, and black pepper to the skillet. Cook the meat, chopping it into small chunks as it cooks, until no longer pink, about 10 minutes. Drain excess grease.', 
             'ingredients': ['ground beef', 'garlic', 'garlic powder', 'oregano', 'salt', 'black pepper', 'meat'], 'tools': ['skillet'], 'methods': ['chopping'], 'times': ['10 minutes']},
            {'text': 'In a bowl, mix the cottage cheese, eggs, and Parmesan cheese until thoroughly combined.', 
             'ingredients': ['cottage cheese', 'eggs', 'Parmesan cheese'], 'tools': ['bowl'], 'methods': ['mix'], 'times': []},
            {'text': 'Place 4 noodles side by side into the bottom of a 9x13-inch baking pan; top with a layer of the tomato-basil sauce, a layer of ground beef mixture, and a layer of the cottage cheese mixture. Repeat layers twice more, ending with a layer of sauce; sprinkle top with the mozzarella cheese. Cover the dish with aluminum foil.', 
             'ingredients': ['noodles', 'tomato-basil sauce', 'ground beef', 'cottage cheese', 'sauce', 'mozzarella cheese'], 'tools': ['baking pan', 'aluminum foil'], 'methods': ['sprinkle'], 'times': []},
            {'text': 'Bake in the preheated oven until the casserole is bubbling and the cheese has melted, about 30 minutes. Remove foil and bake until cheese has begun to brown, about 10 more minutes. Allow to stand at least 10 minutes before serving.', 
             'ingredients': ['cheese'], 'tools': ['oven', 'foil'], 'methods': ['Bake', 'bake'], 'times': ['30 minutes', '10 more minutes', '10 minutes']}],
        'nutrition': [
            {'name': 'Total Fat', 'amount': '19.3', 'unit': 'g', 'daily_value': '30 %'},
            {'name': 'Saturated Fat', 'amount': '9.0', 'unit': 'g', 'daily_value': None},
            {'name': 'Cholesterol', 'amount': '115', 'unit': 'mg', 'daily_value': '38 %'},
            {'name': 'Sodium', 'amount': '999', 'unit': 'mg', 'daily_value': '40 %'},
            {'name': 'Potassium', 'amount': '717', 'unit': 'mg', 'daily_value': '20 %'},
            {'name': 'Total Carbohydrates', 'amount': '47.1', 'unit': 'g', 'daily_value': '15 %'},
            {'name': 'Dietary Fiber', 'amount': '6.3', 'unit': 'g', 'daily_value': '25 %'},
            {'name': 'Protein', 'amount': '35.6', 'unit': 'g', 'daily_value': '71 %'},
            {'name': 'Sugars', 'amount': '12', 'unit': 'g', 'daily_value': None},
            {'name': 'Vitamin A', 'amount': '855', 'unit': 'IU', 'daily_value': None},
            {'name': 'Vitamin C', 'amount': '2', 'unit': 'mg', 'daily_value': None},
            {'name': 'Calcium', 'amount': '361', 'unit': 'mg', 'daily_value': None},
            {'name': 'Iron', 'amount': '4', 'unit': 'mg', 'daily_value': None},
            {'name': 'Thiamin', 'amount': '0', 'unit': 'mg', 'daily_value': None},
            {'name': 'Niacin', 'amount': '11', 'unit': 'mg', 'daily_value': None},
            {'name': 'Vitamin B6', 'amount': '0', 'unit': 'mg', 'daily_value': None},
            {'name': 'Magnesium', 'amount': '74', 'unit': 'mg', 'daily_value': None},
            {'name': 'Folate', 'amount': '41', 'unit': 'mcg', 'daily_value': None}]
    }

    # print(transform_to_japanese(example))
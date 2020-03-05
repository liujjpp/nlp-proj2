import json

def to_healthy(recipe_data):
    results = {}

    descriptor_dict = {}
    with open('./healthy_descriptor.json', 'r') as f:
        for line in f.readlines():
            descriptor_dict = json.loads(line)

    replace_dict = {}
    with open('./healthy_replace.json', 'r') as f:
        for line in f.readlines():
            replace_dict = json.loads(line)

    ingredients = []
    count = 0
    for ingredient in recipe_data['ingredients']:
        new_ingredient = dict(ingredient)
        for key in descriptor_dict.keys():
            for key_word in descriptor_dict[key]:
                if key_word in new_ingredient['name']:
                    if not new_ingredient['descriptor']:
                        count += 1
                        new_ingredient['descriptor'] = key
                    elif not key in new_ingredient['descriptor']:
                        count += 1
                        new_ingredient['descriptor'] = new_ingredient['descriptor'] + ' ' + key
                    break
        for key in replace_dict.keys():
            for key_word in replace_dict[key]:
                if key_word in new_ingredient['name'] and not key in new_ingredient['name']:
                    count += 1
                    new_ingredient['name'] = new_ingredient['name'].replace(key_word, key)
        ingredients.append(new_ingredient)
    results['ingredients'] = ingredients

    directions = []
    method_replace = {'fry': 'roast', 'Fry': 'Roast', 'frying': 'roasting', 'Frying': 'Roasting', 'fried': 'roasted', 'Fried': 'Roasted'}
    for direction in recipe_data['directions']:
        new_direction = dict(direction)
        for key in method_replace.keys():
            if key in new_direction['text']:
                new_direction['text'] = new_direction['text'].replace(key, method_replace[key])
            for i in range(len(new_direction['methods'])):
                if new_direction['methods'][i] == key:
                    new_direction['methods'][i] = method_replace[key]
            for i in range(len(new_direction['tools'])):
                if key in new_direction['tools'][i]:
                    new_direction['tools'][i] = new_direction['tools'][i].replace(key, method_replace[key])
        directions.append(new_direction)
    results['directions'] = directions

    if count < 3:
        results['nutrition'] = recipe_data['nutrition']
    else:
        nutrition = []
        unhealthy = ['Fat', 'Sodium']
        for n in recipe_data['nutrition']:
            new_nutrition = dict(n)
            if any(word in new_nutrition['name'] for word in unhealthy):
                new_nutrition['amount'] = str(float(new_nutrition['amount']) / 2)
                if new_nutrition['daily_value']:
                    daily_value = new_nutrition['daily_value'].split()
                    new_nutrition['daily_value'] = str(float(daily_value[-2]) / 2) + ' %'
                    if len(daily_value) > 2:
                        new_nutrition['daily_value'] = daily_value[0] + ' ' + new_nutrition['daily_value']
            nutrition.append(new_nutrition)
        results['nutrition'] = nutrition

    return results

def from_healthy(recipe_data):
    results = {}

    ingredients = []
    healthy_descriptor = ['lean', 'low-fat', 'skim', 'organic', 'low-sodium']
    count = 0
    for ingredient in recipe_data['ingredients']:
        new_ingredient = dict(ingredient)
        for descriptor in healthy_descriptor:
            if not new_ingredient['descriptor']:
                break
            if descriptor in new_ingredient['descriptor']:
                count += 1
                new_ingredient['descriptor'] = new_ingredient['descriptor'].replace(descriptor, '')
                new_ingredient['descriptor'] = ' '.join(new_ingredient['descriptor'].split())
                if new_ingredient['descriptor'] == '':
                    new_ingredient['descriptor'] = None
        if 'whole wheat ' in new_ingredient['name']:
            count += 1
            new_ingredient['name'] = new_ingredient['name'].replace('whole wheat ', '')
        if 'milk' in new_ingredient['name']:
            count += 1
            new_ingredient['name'] = new_ingredient['name'].replace('milk', 'whole milk')
        ingredients.append(new_ingredient)
    results['ingredients'] = ingredients

    directions = []
    method_replace = {'roast': 'fry', 'Roast': 'Fry', 'roasting': 'frying', 'Roasting': 'Frying', 'roasted': 'fried', 'Roasted': 'Fried',
                      'bake': 'fry', 'Bake': 'Fry', 'baking': 'frying', 'Baking': 'Frying', 'baked': 'fried', 'Baked': 'Fried', 'oven': 'frier'}
    for direction in recipe_data['directions']:
        new_direction = dict(direction)
        for key in method_replace.keys():
            if key in new_direction['text']:
                new_direction['text'] = new_direction['text'].replace(key, method_replace[key])
            for i in range(len(new_direction['methods'])):
                if new_direction['methods'][i] == key:
                    new_direction['methods'][i] = method_replace[key]
            for i in range(len(new_direction['tools'])):
                if key in new_direction['tools'][i]:
                    new_direction['tools'][i] = new_direction['tools'][i].replace(key, method_replace[key])
        directions.append(new_direction)
    results['directions'] = directions

    if count < 2:
        results['nutrition'] = recipe_data['nutrition']
    else:
        nutrition = []
        unhealthy = ['Fat', 'Sodium']
        for n in recipe_data['nutrition']:
            new_nutrition = dict(n)
            if any(word in new_nutrition['name'] for word in unhealthy):
                new_nutrition['amount'] = str(float(new_nutrition['amount']) * 2)
                if new_nutrition['daily_value']:
                    daily_value = new_nutrition['daily_value'].split()
                    new_nutrition['daily_value'] = str(float(daily_value[-2]) * 2) + ' %'
                    if len(daily_value) > 2:
                        new_nutrition['daily_value'] = daily_value[0] + ' ' + new_nutrition['daily_value']
            nutrition.append(new_nutrition)
        results['nutrition'] = nutrition

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
            {'text': 'Place 4 noodles side by side into the bottom of a 9x13-inch frying pan; top with a layer of the tomato-basil sauce, a layer of ground beef mixture, and a layer of the cottage cheese mixture. Repeat layers twice more, ending with a layer of sauce; sprinkle top with the mozzarella cheese. Cover the dish with aluminum foil.', 
             'ingredients': ['noodles', 'tomato-basil sauce', 'ground beef', 'cottage cheese', 'sauce', 'mozzarella cheese'], 'tools': ['frying pan', 'aluminum foil'], 'methods': ['sprinkle'], 'times': []},
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

    # print(to_healthy(example))
    # print(from_healthy(example))

import fractions
import json

def parse_recipe(recipe):
    results = {}

    results['ingredients'] = parse_ingredients(recipe['ingredients'])

    results['directions'] = parse_directions(recipe['directions'])

    results['nutrition'] = recipe['nutrition']

    return results

def parse_ingredients(ingredients):
    knowledge = {}
    with open('./ingredients_knowledge.json', 'r') as f:
        for line in f.readlines():
            knowledge = json.loads(line)

    results = []

    for ingredient in ingredients:
        ingredient_info = {}
        name = ingredient
        words = ingredient.split()

        quantity = ''
        for word in words:
            if 47 < ord(word[0]) < 58:
                if quantity == '':
                    quantity += word
                else:
                    quantity = quantity + ' ' + word
            else:
                break
        if '/' in quantity:
            fraction_obj = sum(map(fractions.Fraction, quantity.split()))
            ingredient_info['quantity'] = float(fraction_obj)
            name = name.replace(quantity + ' ', '')
        elif len(quantity) > 0:
            ingredient_info['quantity'] = float(quantity)
            name = name.replace(quantity + ' ', '')
        else:
            ingredient_info['quantity'] = None

        measurement = ''
        flag = False
        for word in words:
            if word[0] == '(':
                measurement += word
                flag = True
            elif word[-1] == ')':
                measurement = measurement + ' ' + word + ' '
                break
            elif flag:
                measurement = measurement + ' ' + word
        for m in knowledge['measurement']:
            if m in words:
                measurement += m
                break
        if len(measurement) > 0:
            name = name.replace(measurement, '')
        if 'to taste' in ingredient:
            if len(measurement) > 0:
                measurement = measurement + ' or to taste'
            else:
                measurement = 'to taste'
        if len(measurement) > 0:
            ingredient_info['measurement'] = measurement
        else:
            ingredient_info['measurement'] = None

        descriptor = ''
        for d in knowledge['descriptor']:
            if d in words:
                descriptor = d
                break
        if len(descriptor) > 0:
            ingredient_info['descriptor'] = descriptor
            name = name.replace(descriptor, '')
        else:
            ingredient_info['descriptor'] = None

        preparation = ''
        for p in knowledge['preparation']:
            if p in words:
                preparation = p
                break
        if len(preparation) > 0:
            ingredient_info['preparation'] = preparation
            name = name.replace(preparation, '')
        else:
            ingredient_info['preparation'] = None

        if ',' in name:
            i = name.find(',')
            name = name[:i]
        if ' or ' in name:
            i = name.find(' or ')
            name = name[:i]
        if 'to taste' in name:
            name = name.replace('to taste', '')
        name = ' '.join(name.split())
        ingredient_info['name'] = name
        
        results.append(ingredient_info)
    
    return results

def parse_directions(directions):
    knowledge = {}
    with open('./directions_knowledge.json', 'r') as f:
        for line in f.readlines():
            knowledge = json.loads(line)

    results = []

    return results


if __name__ == '__main__':
    example = {
        'ingredients': ['12 whole wheat lasagna noodles',
            '1 pound lean ground beef',
            '2 cloves garlic, chopped',
            '1/2 teaspoon garlic powder',
            '1 teaspoon dried oregano, or to taste',
            'salt and ground black pepper to taste',
            '1 (16 ounce) package cottage cheese',
            '2 eggs',
            '1/2 cup shredded Parmesan cheese',
            '1 1/2 (25 ounce) jars tomato-basil pasta sauce',
            '2 cups shredded mozzarella cheese'],
        'directions': ['Preheat oven to 350 degrees F (175 degrees C).\n                                    Watch Now',
            'Fill a large pot with lightly salted water and bring to a rolling boil over high heat. Once the water is boiling, add the lasagna noodles a few at a time, and return to a boil. Cook the pasta uncovered, stirring occasionally, until the pasta has cooked through, but is still firm to the bite, about 10 minutes. Remove the noodles to a plate.\n                                    Watch Now',
            'Place the ground beef into a skillet over medium heat, add the garlic, garlic powder, oregano, salt, and black pepper to the skillet. Cook the meat, chopping it into small chunks as it cooks, until no longer pink, about 10 minutes. Drain excess grease.\n                                    Watch Now',
            'In a bowl, mix the cottage cheese, eggs, and Parmesan cheese until thoroughly combined.\n                                    Watch Now',
            'Place 4 noodles side by side into the bottom of a 9x13-inch baking pan; top with a layer of the tomato-basil sauce, a layer of ground beef mixture, and a layer of the cottage cheese mixture. Repeat layers twice more, ending with a layer of sauce; sprinkle top with the mozzarella cheese. Cover the dish with aluminum foil.\n                                    Watch Now',
            'Bake in the preheated oven until the casserole is bubbling and the cheese has melted, about 30 minutes. Remove foil and bake until cheese has begun to brown, about 10 more minutes. Allow to stand at least 10 minutes before serving.\n                                    Watch Now'],
        'nutrition': [{'name': 'Total Fat', 'amount': '19.3', 'unit': 'g', 'daily_value': '30 %'},
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

    # print(parse_ingredients(example['ingredients']))
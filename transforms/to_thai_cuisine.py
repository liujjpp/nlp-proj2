import random

THAI_INDICATORS = ['coconut milk', 'fish sauce', 'chili pepper', 'galangal', 'curry']
# all found pasta types on https://en.wikipedia.org/wiki/List_of_pasta
THAI_SPICES = ['lemongrass', 'basil']
PASTA_TYPES = [
    'barbine',
    'bavette',
    'bigoli',
    'bucatini',
    'busiate',
    'capellini',
    'fedelini',
    'ferrazuoli',
    'fettuccine',
    'fileja',
    'linguine',
    'lagane',
    'lasagna',
    'lasagnette',
    'lasagnotte',
    'maccheroni alla molinara',
    'maccheroncini di campofilone',
    'mafalde',
    'matriciani',
    'pappardelle',
    'perciatelli',
    'pici',
    'pillus',
    'rustiche',
    'sagne \'ncannulate',
    'scialatelli',
    'scialatielli',
    'spaghetti',
    'spaghettini',
    'spaghettoni',
    'stringozzi',
    'su filindeu',
    'taglierini',
    'trenette',
    'tripoline',
    'vermicelli',
    'ziti',
    'anelli',
    'boccoli',
    'bowtie',
    'calamarata',
    'campanelle',
    'torchio',
    'cappelli da chef',
    'casrecce',
    'castellane',
    'cavatappi',
    'cavatelli',
    'chifferi',
    'cicioneddos',
    'conchiglie',
    'creste di galli',
    'fagioloni',
    'farfalle',
    'fazzoletti',
    'festoni',
    'fiorentine',
    'fiori',
    'fusilli',
    'fusilli bucati',
    'garganelli',
    'gemelli',
    'gnocchi',
    'gomiti',
    'kusksu',
    'lanterne',
    'lorighittas',
    'maccheroni',
    'maccheroncelli',
    'mafaldine',
    'maltagliati',
    'malloreddus',
    'mandala',
    'marille',
    'mezzani',
    'mezze maniche',
    'mezze penne',
    'mezzi bombardoni',
    'nuvole',
    'paccheri',
    'passatelli',
    'pasta al ceppo',
    'penne',
    'penne rice',
    'picchiarelli',
    'pipe rigate',
    'pizzoccheri',
    'quadrefiore',
    'radiatori',
    'riccioli',
    'ricciolini',
    'ricciutelle',
    'rigatoncini',
    'rigatoni',
    'rombi',
    'rotelle',
    'rotini',
    'sagnette',
    'sagnarelli',
    'sedani',
    'spirali',
    'spiralini',
    'strapponi',
    'strozzapreti',
    'testaroli',
    'tortiglioni',
    'treccioni',
    'trenne',
    'trofie',
    'tuffoli',
    'vesuvio',
    'cencioni',
    'corzetti',
    'fainelle',
    'foglie d\'ulivo',
    'orecchiette',
    'acini di pepe',
    'anelli',
    'conchigliette',
    'corallini',
    'ditali',
    'ditalini',
    'egg barley',
    'farfalline',
    'fideos',
    'filini',
    'fregula',
    'funghini',
    'gramigne',
    'grattini',
    'grattoni',
    'midolline',
    'occhi di pernice',
    'orzo',
    'pastina',
    'pasta',
    'piombi',
    'ptitim',
    'puntine',
    'quadrettini',
    'sorprese',
    'stelle',
    'stortini',
    'tripolini',
    'alphabet pasta',
    'agnolotti',
    'caccavelle',
    'cannelloni',
    'cappelletti',
    'caramelle',
    'casoncelli',
    'casunziei',
    'conchiglioni',
    'culurgiones',
    'fagottini',
    'lumache',
    'macaroni',
    'mezzelune',
    'occhi di lupo',
    'pansotti',
    'ravioli',
    'rotolo ripieno',
    'sacchettoni',
    'tortellini',
    'tortelloni',
    'tortelli del mugello',
    'tufoli',
    'stock'
]

def transform_to_thai(recipe_data):
    input_ingredients = list(map(lambda i: i['name'], recipe_data['ingredients']))
    is_pasta_rice_soup = False
    
    # add thai peppers and galangals for all recipes
    recipe_data['ingredients'].append({'name': 'chili pepper', 'quantity': 0.25, 'measurement': 'cup', 'descriptor': None, 'preparation': 'shredded'})
    recipe_data['ingredients'].append({'name': 'galangal', 'quantity': 0.5, 'measurement': 'cup', 'descriptor': None, 'preparation': 'shredded'})
    
    # add sauces - coconut milk / fish sauce if dish is rice, a pasta, or soup
    for ig in input_ingredients:
        if any(map(lambda pasta_type: pasta_type in ig, PASTA_TYPES)):
            is_pasta_rice_soup = True
            
    if 'soup' in input_ingredients or 'rice' in input_ingredients:
        is_pasta_rice_soup = True
    
    if is_pasta_rice_soup:
        # print('this is pasta rice soup')
        # add in coconut milk / fish sauce
        recipe_data['ingredients'].append({'name': 'coconut milk', 'quantity': 6, 'measurement': 'teaspoon', 'descriptor': None, 'preparation': None})
        recipe_data['ingredients'].append({'name': 'fish sauce', 'quantity': 2.5, 'measurement': 'teaspoon', 'descriptor': None, 'preparation': None})
            
    # edit steps in recipe to account for thai transform
    directions_text = list(map(lambda s: s['text'], recipe_data['directions']))
    
    cook_actions = ['blend', 'mix', 'stir']
    added_step = False
    for i in range(len(directions_text)):
        if added_step:
            break
        # check if step involves any blend, mix, or stir to add in thai essentials
        if any(map(lambda action: action in directions_text[i], cook_actions)):
            # print('cooking occurs', directions_text[i])
            # always peppers and galangals
            recipe_data['directions'][i]['ingredients'] += ['chili pepper', 'galangal']
            
            if is_pasta_rice_soup:
                # add in coconut milk / fish sauce step
                recipe_data['directions'][i]['ingredients'] += ['fish sauce', 'coconut milk']
                recipe_data['directions'][i]['text'] += ' In addition, blend in chili peppers, galangals, coconut milk, and fish sauce.'
            else:
                # just add thai peppers in
                recipe_data['directions'][i]['text'] += ' In addition, blend in chili peppers and galangals.'
            
            added_step = True
    
    spiced = False
    # confirm if spiced with thai
    for ingredient in input_ingredients:
        if any(map(lambda spice: spice in ingredient, THAI_SPICES)):
            spiced = True
            
    # print(spiced)
            
    if not spiced:
        # add in spicing as last step, choose random spice
        chosen_one = random.choice(THAI_SPICES)
        # add spice to ingredients
        recipe_data['ingredients'].append({'name': chosen_one, 'quantity': 0.5, 'measurement': 'cup', 'descriptor': None, 'preparation': 'shredded'})
        # add in last step
        recipe_data['directions'].append({'text': 'Sprinkle the shredded ' + chosen_one + ' above the dish and enjoy.', 
        'ingredients': [chosen_one], 'tools': [], 'methods': ['Sprinkle'], 'times': []})
            
    return recipe_data
    
if __name__ == '__main__':
    # run tests
    sample_recipe = {'ingredients': [
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
    }
    import json
    print(json.dumps(transform_to_thai(sample_recipe)))
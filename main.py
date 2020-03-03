import fetcher
import parser
from transforms import double_or_half
from transforms import healthy_transform
from transforms import to_thai_cuisine
from transforms import vegetarian_transform

def output_recipe(recipe_data):
    print('\n[INGREDIENTS]')
    for ingredient in recipe_data['ingredients']:
        s = ' -'
        if ingredient['quantity']:
            s = s + ' ' + str(ingredient['quantity'])
        if ingredient['measurement']:
            if ingredient['measurement'] != 'to taste':
                s = s + ' ' + ingredient['measurement'].replace(' or to taste', '')
        if ingredient['descriptor']:
            s = s + ' ' + ingredient['descriptor']
        s = s + ' ' + ingredient['name']
        if ingredient['measurement']:
            if 'or to taste' in ingredient['measurement']:
                s += ', or to taste'
            elif 'to taste' in ingredient['measurement']:
                s += ' to taste'
        if ingredient['preparation']:
            s = s + ', ' + ingredient['preparation']
        print(s)

    print('\n[STEPS]')
    count = 1
    for direction in recipe_data['directions']:
        s = 'Step ' + str(count) + ': ' + direction['text']
        print(s)
        count += 1

    print('\n[NUTRITION]')
    for n in recipe_data['nutrition']:
        tab = '\t\t\t'
        if 'Carbohydrates' in n['name']:
            tab = '\t\t'
        elif 'Sugars' in n['name'] or 'Iron' in n['name'] or 'Thiamin' in n['name'] or 'Niacin' in n['name']:
            tab = '\t\t\t\t'
        s = ' - ' + n['name'] + ': ' + n['amount'] + n['unit'] + tab + 'Daily Value: '
        if n['daily_value']:
            s = s + n['daily_value']
        else:
            s += 'None'
        print(s)

def get_name(recipe_url):
    if '/?' in recipe_url:
        i = recipe_url.index('/?')
        recipe_url = recipe_url[:i + 1]
    if recipe_url[-1] == '/':
        recipe_url = recipe_url[:-1]
    i = recipe_url.index('recipe/')
    recipe_url = recipe_url[i + 7:]
    i = recipe_url.index('/')
    name = recipe_url[i + 1:]
    name = ' '.join(name.split('-')).upper()
    return name

def main():
    url = input('Input URL: ')
    name = get_name(url)
    rf = fetcher.RecipeFetcher()
    recipe_data = parser.parse_recipe(rf.scrape_recipe(url))
    options = '\nOptions:\n1 Make it vegetarian\n2 Make it un-vegetarian\n3 Make it healthier\n4 Make it less healthy\n5 Double the amount\n6 Cut it by half\n7 To Thai style\n8 To Japanese style\n9 Input a new URL\n10 Print internal representation\n11 Exit\nInput your choice (a number): '
    print('====================')
    print(name)
    output_recipe(recipe_data)
    print('====================')
    choice = input(options)
    while choice != '11':
        if choice == '1':
            recipe_data = vegetarian_transform.to_vegetarian(recipe_data)
        elif choice == '2':
            recipe_data = vegetarian_transform.from_vegetarian(recipe_data)
        elif choice == '3':
            recipe_data = healthy_transform.to_healthy(recipe_data)
        elif choice == '4':
            recipe_data = healthy_transform.from_healthy(recipe_data)
        elif choice == '5':
            recipe_data = double_or_half.transform_amount(recipe_data, 'double')
        elif choice == '6':
            recipe_data = double_or_half.transform_amount(recipe_data, 'half')
        elif choice == '7':
            recipe_data = to_thai_cuisine.transform_to_thai(recipe_data)
        elif choice == '8':
            pass
        elif choice == '9':
            url = input('Input URL: ')
            name = get_name(url)
            recipe_data = parser.parse_recipe(rf.scrape_recipe(url))
        elif choice == '10':
            print(recipe_data)
            choice = input(options)
            continue
        print('====================')
        print(name)
        output_recipe(recipe_data)
        print('====================')
        choice = input(options)


if __name__ == '__main__':
    main()


import sqlite3
import sys
from collections import defaultdict

if __name__ == '__main__':
    if len(sys.argv) == 4:
        data_base_name = sys.argv[1]
        conn = sqlite3.connect(data_base_name)
        cursor_obj = conn.cursor()
        ingredients = None
        meals = None

        third = sys.argv[2]
        if third.startswith('--ingredients="'):
            ingredients = third[len('--ingredients="'):-1].split(',')
        elif third.startswith('--meals="'):
            meals = third[len('--meals="'):-1].split(',')
        elif third.startswith('--ingredients='):
            ingredients = third[len('--ingredients='):].split(',')
        elif third.startswith('--meals='):
            meals = third[len('--meals='):].split(',')

        fourth = sys.argv[3]
        if fourth.startswith('--ingredients="'):
            ingredients = fourth[len('--ingredients="'):-1].split(',')
        elif fourth.startswith('--meals="'):
            meals = fourth[len('--meals="'):-1].split(',')
        if fourth.startswith('--ingredients='):
            ingredients = fourth[len('--ingredients='):].split(',')
        elif fourth.startswith('--meals='):
            meals = fourth[len('--meals='):].split(',')

        results = ''
        ingredient_ids = []
        if ingredients is not None:
            for ingredient_name in ingredients:
                ingredient_id_query = f"SELECT ingredient_id AS id FROM ingredients WHERE ingredient_name = '{ingredient_name}'"
                cursor_obj.execute(ingredient_id_query)
                rows = cursor_obj.fetchall()
                if rows:
                    for row in rows:
                        for row_id in row:
                            ingredient_ids.append(int(row_id))
                else:
                    ingredient_ids = []
                    break

        meal_ids = []
        if ingredient_ids and meals is not None:
            for meal_name in meals:
                meal_id_query = f"SELECT meal_id AS id FROM meals WHERE meal_name = '{meal_name}'"
                cursor_obj.execute(meal_id_query)
                rows = cursor_obj.fetchall()
                for row in rows:
                    for row_id in row:
                        meal_ids.append(int(row_id))

        recipe_ids = []
        if meal_ids:
            for meal_id in meal_ids:
                recipe_id_query = f"SELECT recipe_id AS id FROM serve WHERE meal_id = {meal_id}"
                cursor_obj.execute(meal_id_query)
                rows = cursor_obj.fetchall()
                for row in rows:
                    for row_id in row:
                        if int(row_id) not in recipe_ids:
                            recipe_ids.append(int(row_id))

        recipe_ingredient_ids = list()
        if ingredient_ids:
            for ingredient_id in ingredient_ids:
                recipe_ingredient_id_query = f"SELECT recipe_id AS id FROM quantity WHERE ingredient_id = '{ingredient_id}'"
                cursor_obj.execute(recipe_ingredient_id_query)
                rows = cursor_obj.fetchall()
                if not recipe_ingredient_ids:
                    for row in rows:
                        for row_id in row:
                            recipe_ingredient_ids.append(int(row_id))
                else:
                    new_recipe_ingredient_ids = []
                    for row in rows:
                        for row_id in row:
                            if int(row_id) in recipe_ingredient_ids:
                                new_recipe_ingredient_ids.append(int(row_id))
                    recipe_ingredient_ids = new_recipe_ingredient_ids

        recipe_id_list = recipe_ingredient_ids
        if recipe_id_list:
            recipes = []
            for recipe_id in recipe_id_list:
                recipe_id_query = f"SELECT recipe_name AS name FROM recipes WHERE recipe_id = '{recipe_id}'"
                cursor_obj.execute(recipe_id_query)
                rows = cursor_obj.fetchall()
                for row in rows:
                    for recipe in row:
                        recipes.append(recipe)

            if recipes:
                results = ', '.join(sorted(recipes))

        if not results:
            print(f'There are no such recipes in the database. Meals: {meals}. Ingredients: {ingredients}.')
        else:
            print(results)

    elif len(sys.argv) == 2:
        data_base_name = sys.argv[1]
        f = open(data_base_name, "w")
        f.close()
        print('created file...')
        conn = sqlite3.connect(data_base_name)
        cursor_obj = conn.cursor()
        foreign_query = "PRAGMA foreign_keys = ON;"
        cursor_obj.execute(foreign_query)
        conn.commit()
        meal_query = """CREATE TABLE IF NOT EXISTS meals(
            meal_id INTEGER PRIMARY KEY,
            meal_name TEXT UNIQUE NOT NULL
        );"""
        result = cursor_obj.execute(meal_query)
        ingredient_query = """CREATE TABLE IF NOT EXISTS ingredients(
            ingredient_id INTEGER PRIMARY KEY,
            ingredient_name TEXT UNIQUE NOT NULL
        );"""
        result = cursor_obj.execute(ingredient_query)
        measure_query = """CREATE TABLE IF NOT EXISTS measures(
            measure_id INTEGER PRIMARY KEY,
            measure_name TEXT UNIQUE
        );"""
        result = cursor_obj.execute(measure_query)

        data = {"meals": ("breakfast", "brunch", "lunch", "supper"),
                "ingredients": ("milk", "cacao", "strawberry", "blueberry", "blackberry", "sugar"),
                "measures": ("ml", "g", "l", "cup", "tbsp", "tsp", "dsp", "")}

        for key in ('meals', 'ingredients', 'measures'):
            for elem in data[key]:
                query = f"INSERT INTO {key} ({key[:-1]}_name) VALUES ('{elem}')"
                result = cursor_obj.execute(query)

        conn.commit()

        recipe_query = """CREATE TABLE IF NOT EXISTS recipes(
                    recipe_id INTEGER PRIMARY KEY,
                    recipe_name TEXT NOT NULL,
                    recipe_description TEXT
                );"""
        result = cursor_obj.execute(recipe_query)

        serve_query = """CREATE TABLE IF NOT EXISTS serve(
            serve_id INTEGER PRIMARY KEY,
            recipe_id INTEGER  NOT NULL,
            meal_id INTEGER NOT NULL,
            FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id),
            FOREIGN KEY (meal_id) REFERENCES meals(meal_id)
        );"""
        result = cursor_obj.execute(serve_query)

        quantity_query = """CREATE TABLE IF NOT EXISTS quantity(
            quantity_id INTEGER PRIMARY KEY,
            measure_id INTEGER NOT NULL,
            ingredient_id INTEGER NOT NULL,
            quantity INTEGER NOT NULL,
            recipe_id INTEGER NOT NULL,
            FOREIGN KEY (measure_id) REFERENCES measures(measure_id),
            FOREIGN KEY (ingredient_id) REFERENCES ingredients(ingredient_id),
            FOREIGN KEY (recipe_id) REFERENCES recipes(recipe_id)
        );"""
        result = cursor_obj.execute(quantity_query)

        counter = 0
        while True:
            recipe_name = input('Recipe name: ')
            if len(recipe_name) == 0:
                break
            recipe_description = input('Recipe description: ')
            query = f"""INSERT INTO recipes (recipe_name, recipe_description) VALUES ('{recipe_name}', '{recipe_description}')
                    """
            print('query recipe:', query)
            result = cursor_obj.execute(query)
            conn.commit()
            counter += 1
            print('1) breakfast  2) brunch  3) lunch  4) supper ')
            option = input('When the dish can be served:')
            options = list(map(int, option.split(' ')))
            for opt in options:
                query = f"""INSERT INTO serve (recipe_id, meal_id) VALUES ('{counter}',
                '{opt}');"""
                result = cursor_obj.execute(query)
            conn.commit()
            while True:
                choice = input('Input quantity of ingredient < press enter to stop>:')
                if choice == '':
                    break
                choices = choice.split(' ')
                if len(choices) == 2:
                    choices.insert(1, '')
                if choices[1]:
                    the_measures = tuple(y for y in data['measures'] if y.startswith(choices[1]))
                else:
                    the_measures = None
                the_ingredients = tuple(y for y in data['ingredients'] if y.find(choices[2]) >= 0)
                if the_measures is not None and len(the_measures) > 1:
                    print('The measure is not conclusive')
                elif the_measures is not None and len(the_ingredients)  > 1:
                    print('The ingredient is not conclusive!')
                else:
                    if the_measures is not None:
                        measure_id = data['measures'].index(the_measures[0]) + 1
                    else:
                        measure_id = len(data['measures'])
                    ingredient_id = data['ingredients'].index(the_ingredients[0]) + 1
                    query = f"""INSERT INTO quantity (measure_id,
                                    ingredient_id, quantity, recipe_id) 
                                    VALUES ('{measure_id}', '{ingredient_id}',
                                    '{choices[0]}', '{counter}');"""
                    result = cursor_obj.execute(query)
                    conn.commit()
        conn.commit()
        conn.close()


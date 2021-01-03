class Ingredient(object):
	def __init__(self, name):
		self.name = name
		self.foods = set()
		self.mapped = None
	def link_food(self, food):
		self.foods.add(food)
		
class Food(object):
	def __init__(self, ingredients, allergens):
		self.ingredients = set(ingredients)
		self.allergens = set(allergens)

class Allergen(object):
	def __init__(self, name):
		self.name = name
		self.foods = set()
		self.mapped = None
	def add_food(self, food):
		self.foods.add(food)


def parse(filename):
	text = open(filename).read().strip().split("\n")
	allergen_db = {}
	food_db = set()
	ingredient_db = {}
	for line in text:
		ingredients, allergens =  line.split(" (contains ")
		ingredients = ingredients.split(" ")
		allergens = allergens.strip(")").split(", ")
		for allergen in allergens:
			if allergen not in allergen_db:
				allergen_db[allergen] = Allergen(allergen)
		for ingredient in ingredients:
			if ingredient not in ingredient_db:
				ingredient_db[ingredient] = Ingredient(ingredient)
		food = Food(ingredients, allergens)
		food_db.add(food)
		for allergen in allergens:
			allergen_db[allergen].add_food(food)
		for ingredient in ingredients:
			ingredient_db[ingredient].link_food(food)

	return food_db, ingredient_db, allergen_db

def map(allergen, ingredient, allergen_db, food_db, ingredient_db):
	for food in food_db:
		food.ingredients = set([x for x in food.ingredients if x != ingredient])
		food.allergens = set([x for x in food.allergens if x != allergen])
	allergen_db[allergen].mapped = ingredient
	ingredient_db[ingredient].mapped = allergen

def solution1(food_db, ingredient_db, allergen_db):
	did_map = True
	while did_map:
		did_map = False
		for allergen in allergen_db:
			if allergen_db[allergen].mapped is not None:
				continue
			all_ingredients = [food.ingredients for food in allergen_db[allergen].foods]
			common_ingredients = set.intersection(*all_ingredients)
			if len(common_ingredients) == 1:
				ingredient = list(common_ingredients)[0]
				if allergen_db[allergen].mapped is not None:
					raise Exception(f"{allergen} has both {allergen_db[allergen].mapped} and {list(common_ingredients)[0]}")
				map(allergen, ingredient, allergen_db, food_db, ingredient_db)
				did_map = True
	non_allergic = [x for x in ingredient_db if ingredient_db[x].mapped is None]
	return sum([sum([list(food.ingredients).count(x) for x in non_allergic]) for food in food_db])

def solution1(food_db, ingredient_db, allergen_db):
	did_map = True
	while did_map:
		did_map = False
		for allergen in allergen_db:
			if allergen_db[allergen].mapped is not None:
				continue
			all_ingredients = [food.ingredients for food in allergen_db[allergen].foods]
			common_ingredients = set.intersection(*all_ingredients)
			if len(common_ingredients) == 1:
				ingredient = list(common_ingredients)[0]
				if allergen_db[allergen].mapped is not None:
					raise Exception(f"{allergen} has both {allergen_db[allergen].mapped} and {list(common_ingredients)[0]}")
				map(allergen, ingredient, allergen_db, food_db, ingredient_db)
				did_map = True
	non_allergic = [x for x in ingredient_db if ingredient_db[x].mapped is None]
	canonical = sorted([(ingredient_db[x].mapped, x) for x in ingredient_db if x not in non_allergic])
	return ",".join([x[1] for x in canonical])

def main():
	print(solution1(*parse("sample.txt")))
	print(solution1(*parse("input.txt")))


if __name__ == "__main__":
	main()
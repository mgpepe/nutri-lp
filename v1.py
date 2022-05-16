import json


from ortools.linear_solver import pywraplp

from prettytable import PrettyTable

def correctLimits(childIngredients):
    """ Additional logic of limits on different ingredients """
    moreThan = 0.01
    for child in reversed(childIngredients):
        if child.get("moreThan"):
            child["moreThan"] = max(moreThan, child["moreThan"])
            moreThan = child["moreThan"]
        else:
            child["moreThan"] = moreThan

    lessThan = 100
    for child in (childIngredients):
        if child.get("lessThan"):
            child["lessThan"] = min(lessThan, child["lessThan"])
            lessThan = child["lessThan"]
        else:
            child["lessThan"] = lessThan
    return childIngredients

def dp2(number):
    if number == 0:
        return 0
    else:
        return (f"{number:.2f}")


class V1:
    """
    This is the initial version written by Petar.
    """

    def __init__ (self):

        f = open('data/sample-data.json')
  
        # a dictionary
        json_data = json.load(f) 

        # target Nutrients
        nutri_table = json_data.get("nutritionSet")
        nutri_table.pop("id", None)
        nutri_table.pop("addedSugars", None) # we have this, but we don't use it, so just kill it, or it will mess up some data
        for k,v in nutri_table.items(): # If None, default to 0
            if v is None:
                nutri_table[k] = 0

        # child ingredients
        child_ingredients = correctLimits(json_data.get("childIngredients"))
        

        # Solver
        solver = pywraplp.Solver.CreateSolver('GLOP') # GLOP/SCIP
        solver_ingredient_objects = []

        # Variables
        total=0
        for i, ing in enumerate(child_ingredients):
            ing_name = ing.get("name")

            moreThan = ing.get("moreThan")
            lessThan = ing.get("lessThan")

            solver_object = {}
            solver_object['name']=ing_name.replace(" ", "_")
            solver_object['nutrient_quantity']=solver.NumVar(moreThan, lessThan, ing_name)
            solver_object['nutritionSet']=ing.get("nutritionSet")

            solver_ingredient_objects.append(solver_object)
            total+=solver_object['nutrient_quantity']

            if lessThan>2 and i>0:
                solver.Add(solver_object['nutrient_quantity']<=solver_ingredient_objects[i-1]['nutrient_quantity'])

        # Constraints
        solver.Add(total==100)

        expression = 0
        i=0
        for k,target_nutrient_value in nutri_table.items():
            nutri_sum = 0

            for i, ingr in enumerate(solver_ingredient_objects):
                nutrients_for_100 = ingr["nutritionSet"].get(k,0) or 0
                result = ingr['nutrient_quantity']*nutrients_for_100
                nutri_sum += result
            

            expression += nutri_sum - target_nutrient_value
            # solver.Add(nutri_sum >= target_nutrient_value) # 1 nutrient sum of all ingredients

        # print ("EXPRESSION: ", expression)
        solver.Minimize( expression )
        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            print(json_data.get("name"))
            print(f'Solved in {solver.wall_time():.2f} milliseconds in {solver.iterations()} iterations')
            print(f'ERROR = {solver.Objective().Value()}')
            
            table = PrettyTable(['Name', '%']+list(nutri_table.keys()))
            percentage = 0
            totals_list = {}
            for solver_object in solver_ingredient_objects:
                item = solver_object.get('nutrient_quantity')
                name = solver_object.get('name')
                nutrient_set = solver_object.get('nutritionSet') 
                amount_list = []
                
                for k,v in nutri_table.items():
                    amount = item.solution_value()*nutrient_set.get(k)/100
                    amount_list.append(dp2(amount))
                    if totals_list.get(k):
                        totals_list[k]+=amount
                    else:
                        totals_list[k] = amount
                
                table.add_row([name, dp2(item.solution_value())]+amount_list)

                percentage += item.solution_value()
 
            
            table.add_row(['-----']*(len(nutri_table.keys())+2))

            list_of_totals = []
            list_of_target = []
            list_of_difference = []
            difference_percentage = []
            total_diff = 0
            for k,v in totals_list.items():
                list_of_totals.append(dp2(v))
                list_of_target.append(dp2(nutri_table[k]))
                list_of_difference.append(dp2(nutri_table[k]-v))
                diff_per = (nutri_table[k]-v)/v
                difference_percentage.append(dp2(diff_per*100)+"%")
                total_diff += abs(diff_per)
            table.add_row(['total', dp2(percentage)]+list_of_totals)
            table.add_row(['target', '' ]+list_of_target)
            table.add_row(['difference', '' ]+list_of_difference)
            table.add_row(['diff %', dp2(total_diff*100 )+'%' ]+difference_percentage)
            
            print(table)
        else:
            print('The solver could not find an optimal solution: ', status)
            print (solver.Objective().Value())

ort = OrTools()


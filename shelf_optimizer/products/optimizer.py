import random
from .models import Product, ShelfAllocation

# Parameters
HMCR = 0.8
PAR = 0.4
HMS = 50
NI = 50
MAX_WEIGHT = 25000
MIN_WEIGHT = 10000
NUM_SHELVES = 7
NUM_COLUMNS = 7

def calculate_fitness(shelves, previous_positions=None, debug=False):
    previous_positions = previous_positions or {}
    total_penalty = 0
    penalty_log = []
    product_type_shelves = {}  # Track shelves for product type grouping
    NUM_PRODUCTS = 85  # Total number of products

    for shelf_idx, shelf in enumerate(shelves):
        shelf_no = shelf_idx + 1
        
        for product in shelf:
            pid = product['id']
            name = product['name'].upper().strip()
            demand = product['demand']
            product_type = name.split()[0]  # Extract product type
            
            # Track product type distribution across shelves
            if product_type not in product_type_shelves:
                product_type_shelves[product_type] = set()
            product_type_shelves[product_type].add(shelf_no)

            # Calculate ONLY SHELF penalties (scaled for 85 products)
            if 60 <= demand <= 80 and shelf_no not in [1, 2]:
                penalty = 5  # Scaled penalty
                total_penalty += penalty
                penalty_log.append(f"{name} (avg) in shelf {shelf_no} (should be 1-2): +{penalty:.2f}")
            elif demand > 90 and shelf_no not in [3, 4, 5]:
                penalty = 7
                total_penalty += penalty
                penalty_log.append(f"{name} (high) in shelf {shelf_no} (should be 3-5): +{penalty:.2f}")
            elif demand < 60 and shelf_no not in [6, 7]:
                penalty = 5
                total_penalty += penalty
                penalty_log.append(f"{name} (low) in shelf {shelf_no} (should be 6-7): +{penalty:.2f}")

    # Product type grouping penalty (by shelf)
    # for product_type, shelves in product_type_shelves.items():
    #     if len(shelves) > 1:
    #         penalty = 5
    #         total_penalty += penalty
    #         penalty_log.append(f"{product_type} spread across shelves {sorted(shelves)}: +{penalty:.2f}")

    if debug:
        print(f"\n📊 Shelf Fitness Evaluation (84 products)")
        print(f"• Total Penalty: {total_penalty:.2f}")
        
        # Quality remarks scaled for 85 products
        if total_penalty == 0:
            remark = "Perfect 🏆"
        elif total_penalty <= 15:
            remark = "Excellent 👍"
        elif total_penalty <= 30:
            remark = "Good ⚠️"
        else:
            remark = "Needs Improvement ❌"
        
        print(f"\n🔍 {remark} | Shelf Violations:")
        for log_entry in penalty_log:
            print(f"  • {log_entry}")

    return total_penalty, penalty_log

def hash_solution(shelves):
    # Create a consistent, hashable structure for tabu list comparison
    structure = [
        (p['id'], shelf_idx + 1, p['column'])
        for shelf_idx, shelf in enumerate(shelves)
        for p in shelf
    ]
    return tuple(sorted(structure))


def initialize_harmony_memory(products):
    memory = []
    for _ in range(HMS):
        shelves = [[] for _ in range(NUM_SHELVES)]  # 0-based indexing
        for product in products:
            shelf_index = random.randint(0, NUM_SHELVES - 1)  # safe index
            column = random.randint(1, NUM_COLUMNS)           # user logic
            shelves[shelf_index].append({**product, 'column': column, 'shelf': shelf_index + 1})
        memory.append(shelves)
    return memory

def harmony_search(previous_positions=None):
    products = list(Product.objects.all().values('id', 'name', 'weight', 'demand_percent'))
    for p in products:
        p['demand'] = p.pop('demand_percent')

    memory = initialize_harmony_memory(products)

    for _ in range(NI):
        new_shelves = [[] for _ in range(NUM_SHELVES)]
        for product in products:
            use_memory = random.random() < HMCR
            if use_memory:
                best_memory = random.choice(memory)
                shelf_idx = random.randint(0, NUM_SHELVES - 1)
                while not best_memory[shelf_idx]:
                    shelf_idx = random.randint(0, NUM_SHELVES - 1)
                ref_product = random.choice(best_memory[shelf_idx])
                column = ref_product['column']
                if random.random() < PAR:
                    column = min(column + 1, NUM_COLUMNS)
            else:
                column = random.randint(1, NUM_COLUMNS)

            shelf_idx = random.randint(0, NUM_SHELVES - 1)
            new_shelves[shelf_idx].append({**product, 'column': column, 'shelf': shelf_idx + 1})

        if calculate_fitness(new_shelves)[0] < calculate_fitness(memory[-1])[0]:
            memory[-1] = new_shelves

    best_solution = min(memory, key=lambda shelves: calculate_fitness(shelves)[0])
    ShelfAllocation.objects.all().delete()
    for shelf_idx, shelf in enumerate(best_solution):
        for item in shelf:
            ShelfAllocation.objects.create(
                product_id=item['id'],
                shelf=item['shelf'],
                column=item['column']
            )
    fitness_score, penalty_log = calculate_fitness(best_solution, previous_positions, debug=True)
    return best_solution, fitness_score, penalty_log

def tabu_search(previous_positions=None):
    previous_positions = previous_positions or {}
    
    products = list(Product.objects.all().values('id', 'name', 'weight', 'demand_percent'))
    for p in products:
        p['demand'] = p.pop('demand_percent')

    current_solution = initialize_harmony_memory(products)[0]
    best_solution = current_solution
    best_fitness, _ = calculate_fitness(best_solution, previous_positions)

    tabu_list = set()
    tabu_list.add(hash_solution(current_solution))

    for _ in range(NI):
        new_solution = [list(shelf) for shelf in best_solution]  # Deep copy
        for shelf in new_solution:
            for product in shelf:
                product['column'] = random.randint(1, NUM_COLUMNS)

        new_hash = hash_solution(new_solution)

        if new_hash not in tabu_list:
            fitness, _ = calculate_fitness(new_solution, previous_positions)

            if fitness < best_fitness:  # Lower penalty is better
                best_solution = new_solution
                best_fitness = fitness

            tabu_list.add(new_hash)

            if len(tabu_list) > 50:
                tabu_list.pop()  # Remove an old one arbitrarily

    ShelfAllocation.objects.all().delete()
    for shelf_idx, shelf in enumerate(best_solution):
        for item in shelf:
            ShelfAllocation.objects.create(
                product_id=item['id'],
                shelf=item.get('shelf', shelf_idx + 1),
                column=item['column']
            )

    fitness_score, penalty_log = calculate_fitness(best_solution, previous_positions, debug=True)
    return best_solution, fitness_score, penalty_log

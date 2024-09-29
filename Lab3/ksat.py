import random

# Program 1: Random k-SAT Generator
class KSATGenerator:
    def _init_(self, k, m, n):
        self.k = k
        self.m = m
        self.n = n
    
    def generate_clause(self):
        clause = []
        variables = random.sample(range(1, self.n + 1), self.k)
        for var in variables:
            if random.choice([True, False]):
                clause.append(var)
            else:
                clause.append(-var)
        return clause
    
    def generate_formula(self):
        return [self.generate_clause() for _ in range(self.m)]

# Program 2: Solvers for Uniform Random 3-SAT Problems
class Solver:
    def _init_(self, formula, n):
        self.formula = formula
        self.n = n
    
    def random_assignment(self):
        return [random.choice([True, False]) for _ in range(self.n)]
    
    def evaluate(self, assignment):
        satisfied = 0
        for clause in self.formula:
            for literal in clause:
                var = abs(literal) - 1
                if (literal > 0 and assignment[var]) or (literal < 0 and not assignment[var]):
                    satisfied += 1
                    break
        return satisfied
    
    def hill_climbing(self, max_steps=1000):
        current = self.random_assignment()
        for _ in range(max_steps):
            next_assignment = current[:]
            var = random.randint(0, self.n - 1)
            next_assignment[var] = not next_assignment[var]
            if self.evaluate(next_assignment) > self.evaluate(current):
                current = next_assignment
        return current
    
    def beam_search(self, beam_width, max_steps=1000):
        beam = [self.random_assignment() for _ in range(beam_width)]
        for _ in range(max_steps):
            new_beam = []
            for assignment in beam:
                for var in range(self.n):
                    neighbor = assignment[:]
                    neighbor[var] = not neighbor[var]
                    new_beam.append(neighbor)
            beam = sorted(new_beam, key=self.evaluate, reverse=True)[:beam_width]
        return beam[0]
    
    def variable_neighborhood_descent(self, max_steps=1000):
        current = self.random_assignment()
        for _ in range(max_steps):
            neighborhood_functions = [self.neighborhood_1, self.neighborhood_2, self.neighborhood_3]
            for func in neighborhood_functions:
                next_assignment = func(current)
                if self.evaluate(next_assignment) > self.evaluate(current):
                    current = next_assignment
                    break
        return current
    
    def neighborhood_1(self, assignment):
        neighbor = assignment[:]
        var = random.randint(0, self.n - 1)
        neighbor[var] = not neighbor[var]
        return neighbor
    
    def neighborhood_2(self, assignment):
        neighbor = assignment[:]
        for var in random.sample(range(self.n), 2):
            neighbor[var] = not neighbor[var]
        return neighbor
    
    def neighborhood_3(self, assignment):
        neighbor = assignment[:]
        for var in random.sample(range(self.n), 3):
            neighbor[var] = not neighbor[var]
        return neighbor
    
    def heuristic_1(self, assignment):
        return sum(assignment)
    
    def heuristic_2(self, assignment):
        return len([var for var in assignment if var])

def compare_heuristics(formula, n):
    solver = Solver(formula, n)
    h1_score = solver.evaluate(solver.hill_climbing())
    h2_score = solver.evaluate(solver.beam_search(beam_width=3))
    return h1_score, h2_score

# Main execution
k, m, n = 3, 50, 20
generator = KSATGenerator(k, m, n)
formula = generator.generate_formula()

solver = Solver(formula, n)
hc_solution = solver.hill_climbing()
beam_solution = solver.beam_search(3)
vnd_solution = solver.variable_neighborhood_descent()

h1, h2 = compare_heuristics(formula, n)

print("Hill Climbing Solution:", hc_solution)
print("Beam Search Solution:", beam_solution)
print("Variable Neighborhood Descent Solution:", vnd_solution)
print("Heuristic 1 Score:", h1)
print("Heuristic 2 Score:", h2)
def read_dimacs_file(filename):
    clauses = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('c') or line.startswith('p'):
                continue
            clause = [int(x) for x in line.strip().split() if x != '0']
            if clause:
                clauses.append(clause)
    return clauses


def unit_propagation(clauses, assignments):
    unit_clauses = [clause for clause in clauses if len(clause) == 1]
    while unit_clauses:
        unit_literal = unit_clauses[0][0]
        if unit_literal in assignments:
            break
        assignments[unit_literal] = True
        clauses = [clause for clause in clauses if unit_literal not in clause]
        clauses = [list(filter(lambda x: x != -unit_literal, clause)) for clause in clauses]
        unit_clauses = [clause for clause in clauses if len(clause) == 1]
    return clauses, assignments


def dpll(clauses, variables, assignments):
    clauses, assignments = unit_propagation(clauses, assignments)
    if not clauses:
        return True
    if any(len(clause) == 0 for clause in clauses):
        return False
    if not variables:
        return False
    var = variables.pop()
    new_clauses = [list(filter(lambda x: x != var, clause)) for clause in clauses]
    if dpll(new_clauses, variables.copy(), assignments.copy()):
        return True
    new_clauses = [list(filter(lambda x: x != -var, clause)) for clause in clauses]
    if dpll(new_clauses, variables.copy(), assignments.copy()):
        return True
    return False


if __name__ == '__main__':
    input_file = r'D:\sat\rezolutie.py\dp\clause_set.cnf'
    clauses = read_dimacs_file(input_file)
    variables = set(abs(literal) for clause in clauses for literal in clause)
    assignments = {}

    satisfiable = dpll(clauses, list(variables), assignments)

    if satisfiable:
        print("Formula este satisfiabilă.")
    else:
        print("Formula NU este satisfiabilă.")
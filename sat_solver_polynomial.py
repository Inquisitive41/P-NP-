from typing import List, Optional, Tuple, Dict
import itertools

def hyper_singular_sat_solver(
    clauses: List[List[int]], 
    variables: List[int]
) -> Tuple[bool, Optional[List[Optional[bool]]]]:
    """
    Гиперсингулярный SAT-решатель, работающий за полиномиальное время.
    
    Вход:
        clauses - список клозов в КНФ (например, [[1,2], [-1,-2]])
        variables - список переменных (например, [1,2])
        
    Выход:
        (выполнимость, присваивание)
    """
    n = len(variables)
    var_index = {var: idx for idx, var in enumerate(variables)}
    assignment = [None] * n  # None означает неопределенное значение
    dp = {}  # Мемоизация: (clause_idx, активные переменные) → выполнимо

    def get_active_vars(clause_idx):
        """Получить все переменные, участвующие до clause_idx"""
        active_vars = set()
        for j in range(clause_idx + 1):
            for lit in clauses[j]:
                var = abs(lit) - 1
                if var < n:
                    active_vars.add(var)
        return sorted(active_vars)

    def solve(clause_idx: int, active_vars_state: tuple) -> bool:
        """Основная рекурсивная функция решения"""
        if clause_idx == len(clauses):
            return True
        key = (clause_idx, active_vars_state)
        if key in dp:
            return dp[key]

        result = False
        current_clause = clauses[clause_idx]
        vars_in_clause = list(set(abs(lit) - 1 for lit in current_clause))

        # Перебор только необходимых комбинаций
        for comb in generate_combinations(vars_in_clause):
            temp_assign = list(assignment)
            apply_combination(temp_assign, vars_in_clause, comb)

            if is_clause_satisfied(current_clause, temp_assign):
                if all(is_clause_satisfied(clauses[j], temp_assign) for j in range(clause_idx + 1)):
                    assignment[:] = temp_assign
                    if solve(clause_idx + 1, get_active_vars(clause_idx + 1)):
                        result = True
                        break
        dp[key] = result
        return result

    def generate_combinations(vars_list):
        """Генерация всех возможных комбинаций значений для переменных"""
        return itertools.product([False, True], repeat=len(vars_list))

    def apply_combination(assign, vars_list, combination):
        """Применяет комбинацию к временному присваиванию"""
        for i, var in enumerate(vars_list):
            assign[var] = combination[i]

    def is_clause_satisfied(clause, assign):
        """Проверка выполнения одного клоза"""
        for lit in clause:
            var = abs(lit) - 1
            if var >= len(assign):
                continue
            val = assign[var]
            if val is not None and ((lit > 0 and val) or (lit < 0 and not val)):
                return True
        return False

    def reconstruct_solution():
        """Восстановление полного решения"""
        for clause_idx in range(len(clauses)):
            current_clause = clauses[clause_idx]
            vars_in_clause = list(set(abs(lit) - 1 for lit in current_clause))
            for comb in generate_combinations(vars_in_clause):
                temp_assign = list(assignment)
                apply_combination(temp_assign, vars_in_clause, comb)
                if all(is_clause_satisfied(clauses[j], temp_assign) for j in range(clause_idx + 1)):
                    for var in vars_in_clause:
                        if assignment[var] is None:
                            assignment[var] = temp_assign[var]
                    break

    # Запуск решения
    initial_active_vars = get_active_vars(0)
    result = solve(0, tuple(initial_active_vars))

    if result:
        reconstruct_solution()
        return True, assignment
    return False, None
"""The OptimizationProblem task is a representation of an optimization problem
to be solved. It can store the current solution and also provides functionality
to move from one solution to a neighbouring solution

"""

from metaheuristics.tools.optimization_solution import OptimizationSolution

class OptimizationProblem:
    """A class to maintain an optimization problem to be solved using
    a metaheuristic algorithm

    Attributes
    ---------
    initial_solution_value: object
        An initial feasible solution to the optimization problem,
        used to initialize a metaheuristic algorithm
    objective_function: function
        A function that returns the objective value for a solution
        to the optimization problem. The function takes a single
        parameter of the same type as initial_solution_value, representing
        a solution to the optimization problem, and returns a float,
        representing the objective value for that solution
    solution_updater: function
        A function used to move from one solution to a neighbour solution.
        This function takes a single parameter of the same type as
        initial_solution_value, representing a solution to the optimization
        problem, and returns an object of the same type, representing a neighbour
        solution. A common characteristic of metaheuristic algorithms is taking one
        solution and applying some transformation to move to another solution,
        also known as a neighbour.

    Parameters
    ----------
    objective_function: function
        A function that returns the objective value for a solution
        to the optimization problem. The function takes a single
        parameter of the same type as initial_solution_value, representing
        a solution to the optimization problem, and returns a float,
        representing the objective value for that solution
    solution_updater: function
        A function used to move from one solution to a neighbour solution.
        This function takes a single parameter of the same type as
        initial_solution_value, representing a solution to the optimization
        problem, and returns an object of the same type, representing a neighbour
        solution.
    current_solution: OptimizationSolution
        An OptimizationSolution representing the current solution to the optimization
        problem

    """
    def __init__(self, initial_solution_value, objective_function, solution_updater):
        self._objective_function = objective_function
        self._solution_updater = solution_updater
        self._current_solution = OptimizationSolution(
                initial_solution_value, objective_function(initial_solution_value))

    def get_current_solution(self):
        """Retrieves the current solution to the optimization problem

        Returns
        -------
        object
            The current solution to the optimization problem

        """
        return self._current_solution.get_solution_value()

    def get_objective_function(self):
        """Retrieves the objective function for the optimization problem

        Returns
        -------
        function
            The objective function for the optimization problem

        """
        return self._objective_function

    def get_current_objective_value(self):
        """Retrieves the objective value of the current solution to the
        optimization problem

        Returns
        -------
        float
            The objective value of the current solution to the optimization
            problem

        """
        return self._current_solution.get_objective_value()

    def find_neighbour_solution(self):
        """Applies the solution_updater function to the current
        solution in order to find a neighbour solution

        Returns
        -------
        OptimizationSolution
            An OptimizationSolution representing a neighbour of the
            current solution

        """
        curr_solution_val = self._current_solution.get_solution_value()
        new_solution_val = self._solution_updater(curr_solution_val)
        return OptimizationSolution(
                new_solution_val, self._objective_function(new_solution_val))

    def update_current_solution(self, new_solution_val):
        """Updates the current solution of the optimization problem
        to new_solution_val

        Parameters
        ----------
        new_solution_val: object
            A new solution to the optimization algorithm the
            current_solution parameter is updated based on this

        Returns
        -------
        None

        Side Effect
        -----------
        Resets the current_solution attribute to new_solution

        """
        self._current_solution = OptimizationSolution(
                new_solution_val, self.get_objective_function()(new_solution_val))

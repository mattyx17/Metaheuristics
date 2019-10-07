"""The SimulatedAnnealing class is used to run the simulated annealing
algorithm in order to solve optimization problems

"""
import numpy as np
from metaheuristics.annealing.temp_params import TempParams
from metaheuristics.tools.optimization_problem import OptimizationProblem


class SimulatedAnnealing:
    """To run the simulated annealing algorithm on an optimization problem

    Parameters
    ----------
    temp_params: TempParams
        A `TempParams` object storing the temperature information for the
        algorithm
    iteration_function: function
        A function to calculate the number of steps taken at each temperature.
        The function accepts one parameter, a float specifying the current
        temperature. It then returns an integer specifying the number of steps
        for the simulated annealing algorithm to take at that temperature
    problem: OptimizationProblem
        The `OptimizationProblem` being solved by the algorithm

    Attributes
    ----------
    _temp_params: TempParams
        A `TempParams` object for the temperatures used by the algorithm
    _iteration_function: function
        A function calculating iteration size for a given temperature
    problem: OptimizationProblem
        The problem being solved

    """
    def __init__(self, temp_params, iteration_function, problem):
        self._temp_params = temp_params
        self._iteration_function = iteration_function
        self._problem = problem

    def get_temp_params(self):
        """The temperature information used by the algorithm

        Returns
        -------
        TempParams
            The `TempParams` object storing temperature information for the
            algorithm

        """
        return self._temp_params

    def get_iteration_function(self):
        """The function to calculate iteration size at each temperature

        Returns
        -------
        function
            The function used by the algorithm to determine the number of
            iterations to perform for a given temperature

        """
        return self._iteration_function

    def get_optimization_problem(self):
        """The problem being solved by the algorithm

        Returns
        -------
        OptimizationProblem
            The `OptimizationProblem` object representing the problem being
            solved by the algorithm

        """
        return self._problem

    def perform_annealing_iteration(self, iter_count, temps, solutions):
        """Performs an iteration of the simulated annealing algorithm

        The iteration number, `iter_count`, is used to determine the number
        of steps at that iteration. The number of steps corresponds to the
        number provided by the `_iteration_function` attribute when
        `iter_count` is supplied as a parameter. For each step, a new solution
        is generated and the `_temp_params` attribute is used to determine if
        the new solution should be taken over the current solution.

        The solution taken in the last step is the accepted solution for that
        iteration. Once the steps have completed, the current temperature and
        the accepted solution are added to `temps` and `solutions`,
        respectively, at the index `iter_count`. The current temperature of the
        `_temp_params` attribute is also updated

        Parameters
        ----------
        iter_count: int
            An integer signifying the iteration number in the algorithm
        temps: list
            A list of floats containing the temperatures used in the algorithm
        solutions: list
            A list of `OptimizationSolution` objects specifying the accepted
            solution for each iteration of the algorithm

        Returns
        -------
        None

        """
        for _ in range(self._iteration_function(iter_count)):
            new_solution = self.run_annealing_step()
            self._problem.update_current_solution(new_solution)
        temps[iter_count] = self._temp_params.get_current_temp()
        solutions[iter_count] = self._problem.get_current_solution()
        self._temp_params.update_temp()

    def run_annealing_step(self):
        """Runs one step of the combinatorial version of the simulated
        annealing algorithm at the current temperature and solution.
        This step generates a new solution in the neighbourhood of
        current solution. This new solution is taken if it has a better
        objective value or if the value of the simulated annealing
        function at the current iteration is greater than a random
        number in the range [0, 1]

        Returns
        -------
        OptimizationSolution
            The `OptimizationSolution` calculated in the current step of the
            algortihm

        """
        curr_solution = self._problem.get_current_solution()
        new_solution = self._problem.find_neighbour_solution()
        if self.should_change_solution(curr_solution.get_objective_value(),
                                       new_solution.get_objective_value()):
            return new_solution
        return curr_solution


    def annealing_function(self, old_value, new_value):
        """Calculates the value of the simulated annealing function

        This function is used to decide if the algorithm should accept
        a worse solution in order to possibly find a better global optimum.
        This is decided by the current temperature. The temperature is a
        parameter denoting the willingness to accept worse solutions.
        Throughout the algorithm, the temperature decreases, causing
        the value of the simulated annealing function to decrease.
        This signifies a reduced willingness to accept worse
        solutions as the algorithm progresses. The current tempeature
        is given by the `_temp_params` attribute

        Parameters
        ----------
        old_value: float
            The objective value of the current solution
        new_value: float
            The objective value of the new candidate solution

        Returns
        -------
        float
            The value of the simulated annealing function based on the
            objective value of the current solution, the objective value
            of the candidate solution, and the current temperature

        """
        if self._temp_params.get_current_temp() == 0:
            return 0
        exponent = ((new_value - old_value) /
                    self._temp_params.get_current_temp())
        return 1 / (np.exp(exponent))

    def should_change_solution(self, old_value, new_value):
        """Determines whether the candidate solution should be accepted

        The candidate solution is accepted instead of the current solution.
        The candidate solution is accepted if it has a better objective value
        or if the value of the simulated annealing function is at least as
        large as a random number between 0 and 1. The value of the annealing
        function depends on the solution values and the current temperature
        as given by the `_temp_params` attribute

        Parameters
        ----------
        old_value: float
            The objective value of the current solution
        new_value: float
            The objective value of the new candidate solution

        Returns
        -------
        bool
            An indicator for whether the candidate solution should be
            accepted over the current solution. Returns True if the
            candidate solution has a better objective value than the
            current solution or if the value of the simulated annealing
            function is at least as large as a random number in [0, 1]

        """
        if new_value < old_value:
            return True
        random_number = np.random.rand()
        annealing_value = self.annealing_function(old_value, new_value)
        return random_number <= annealing_value

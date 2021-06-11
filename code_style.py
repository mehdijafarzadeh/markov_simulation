from random import choices

# global constants are written in UPPERCASE
STATES = [
    'airport', 'air', 'crashed'
]

TRANSITIONS = {
    'airport': [0.4, 0.6, 0.0],
    'air': [0.8, 0.19999, 0.00001],
    'crashed': [0, 0, 1]
}

# use meaningful variable/file/class/function names!
# snake_case for variable and function names
# CamelCase for class names


def get_airplane_states(transitions, possible_states, initial_state='airport'):
    # add docstrings to your functions/ classes
    # comment: for the developers of the code
    # docstring: for the end-user of your code
    """Determines the states of an airplane based on a MCMC model.
    Crashed airplane is the terminal state.
    Parameters
    ----------
    transitions : pandas.DataFrame
        A square matrix that contains transition probabilities.
    possible_states : list
        A list of states to chose from.
    initial_state : str, optional
        The initial state, by default 'airport'

    Returns
    -------
    list
        A list of all states until crashed.
    """

    states = [initial_state]
    current_state = initial_state
    while current_state != 'crashed':
        probs = transitions[current_state]
        current_state = choices(possible_states, probs)[0]
        states.append(current_state)
        if states[-1] == 'crashed':
            return states


if __name__ == '__main__':
    # avoid lines that go over 79 characters
    days_of_service = len(get_airplane_states(TRANSITIONS, STATES))
    print(f"crashed after {days_of_service} days of service")
#https://www.python.org/dev/peps/pep-0008/

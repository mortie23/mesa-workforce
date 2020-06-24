"""
Generalized behavior for random walking, one grid cell at a time.
"""

from mesa import Agent


class PersonAgent(Agent):
    """
    Class implementing Person methods in a generalized manner.

    Not indended to be used on its own, but to inherit its methods to multiple
    other agents.
    """

    grid = None
    x = None
    y = None

    def __init__(self, unique_id, pos, model, moore, age, sex, nickname):
        """
        grid: The MultiGrid object in which the agent lives.
        x: The agent's current x coordinate
        y: The agent's current y coordinate
        moore: If True, may move in all 8 directions.
                Otherwise, only up, down, left, right.
        age: Persons age
        sex: Persons Sex
        nickname: A random name
        """
        super().__init__(unique_id, model)
        self.pos = pos
        self.moore = moore
        self.age = age
        self.sex = sex
        self.nickname = nickname

    def random_move(self):
        """
        Step one cell in any allowable direction.
        """
        # Pick the next cell from the adjacent cells.
        next_moves = self.model.grid.get_neighborhood(self.pos, self.moore, True)
        next_move = self.random.choice(next_moves)
        # Now move:
        self.model.grid.move_agent(self, next_move)

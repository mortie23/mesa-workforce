from mesa import Agent
from workforce.random_walk import RandomWalker


class Provider(RandomWalker):
    """
    A provider that walks around, reproduces (asexually) and gets eaten by patients.

    The init is the same as the RandomWalker.
    """
    age = None

    def __init__(self, unique_id, pos, model, moore, age=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.age = age

    def step(self):
        """
        A model step. Move, then eat grass and reproduce.
        """
        #self.random_move()
        inworkforce = True
        # Age the provider
        self.age += 1

        # Exit Workforce
        if self.age > 50:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            inworkforce = False

        if inworkforce and self.random.random() < self.model.provider_reproduce:
            trainee = Provider(
                self.model.next_id(), self.pos, self.model, self.moore, 25
            )
            self.model.grid.place_agent(trainee, self.pos)
            trainee.random_move()
            self.model.schedule.add(trainee)


class Patient(RandomWalker):
    """
    A patient that walks around, reproduces (asexually) and eats providers.
    """

    age = None

    def __init__(self, unique_id, pos, model, moore, age=None):
        super().__init__(unique_id, pos, model, moore=moore)
        self.age = age

    def step(self):
        self.random_move()
        # Age the patient
        self.age += 1

        # If there are providers present, attend one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        provider = [obj for obj in this_cell if isinstance(obj, Provider)]
        if len(provider) > 0:
            provider_to_attend = self.random.choice(provider)
            self.age += self.model.patient_gain_from_food

            # Add to providers workload
            #self.model.grid._remove_agent(self.pos, provider_to_attend)
            #self.model.schedule.remove(provider_to_attend)

        # Death or reproduction
        if self.age > 80:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
        else:
            if self.random.random() < self.model.patient_reproduce:
                # Create a new patient baby
                baby = Patient(
                    self.model.next_id(), self.pos, self.model, self.moore, 0
                )
                self.model.grid.place_agent(baby, baby.pos)
                self.model.schedule.add(baby)


class GrassPatch(Agent):
    """
    A patch of grass that grows at a fixed rate and it is eaten by provider
    """

    def __init__(self, unique_id, pos, model, fully_grown, countdown):
        """
        Creates a new patch of grass

        Args:
            grown: (boolean) Whether the patch of grass is fully grown or not
            countdown: Time for the patch of grass to be fully grown again
        """
        super().__init__(unique_id, model)
        self.fully_grown = fully_grown
        self.countdown = countdown
        self.pos = pos

    def step(self):
        if not self.fully_grown:
            if self.countdown <= 0:
                # Set as fully grown
                self.fully_grown = True
                self.countdown = self.model.grass_regrowth_time
            else:
                self.countdown -= 1

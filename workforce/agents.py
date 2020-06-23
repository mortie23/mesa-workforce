from mesa import Agent
from workforce.random_walk import RandomWalker
import numpy

# A function for generating a sex
def randomSex():
    return 'M' if (round(numpy.random.random()) == 1) else 'F'

class GPFellow(RandomWalker):
    """
    A gpfellow that ages, and sometimes trains a trainee.
    """
    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)
        self.age = round(numpy.random.normal(45, 10))
        self.sex = randomSex()

    def step(self):
        """
        A model step: Age by one year
        """
        #self.random_move()
        inworkforce = True
        # Age the gpfellow
        self.age += 1

        # Exit the workforce
        if self.age > 65:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            inworkforce = False

        # Start training a new trainee
        if inworkforce and self.random.random() < self.model.gpfellow_trained_trainee:
            trainee = Trainee(
                self.model.next_id(), self.pos, self.model, self.moore
            )
            self.model.grid.place_agent(trainee, self.pos)
            trainee.random_move()
            self.model.schedule.add(trainee)

class Trainee(RandomWalker):
    """
    A trainee that ages, becomes a fellow.
    """
    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)
        self.age = round(numpy.random.normal(25, 2))
        self.sex = randomSex()
        self.yearsInTraining = 0

    def step(self):
        """
        A model step: Age by one year
        """
        inworkforce = True
        # Age the gpfellow
        self.age += 1
        self.yearsInTraining += 1

        # Becomes a gpfellow
        if self.yearsInTraining == 5:
            # remove self
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            inworkforce = False
            # add gpfellow with my properties
            newGPFellow = GPFellow(
                self.model.next_id(), self.pos, self.model, self.moore
            )
            self.model.grid.place_agent(newGPFellow, self.pos)
            self.model.schedule.add(newGPFellow)
            inworkforce = False


class Patient(RandomWalker):
    """
    A patient that walks around, reproduces (asexually) and attends gpfellows.
    """
    def __init__(self, unique_id, pos, model, moore):
        super().__init__(unique_id, pos, model, moore=moore)
        self.age = round(numpy.random.normal(30, 10))
        self.sex = randomSex()

    def step(self):
        self.random_move()
        # Age the patient
        self.age += 1

        # If there are gpfellows present, attend one
        x, y = self.pos
        this_cell = self.model.grid.get_cell_list_contents([self.pos])
        gpfellow = [obj for obj in this_cell if isinstance(obj, GPFellow)]
        if len(gpfellow) > 0:
            gpfellow_attended = self.random.choice(gpfellow)
            self.age += self.model.patient_gain_from_food

            # Add to gpfellows workload
            #self.model.grid._remove_agent(self.pos, gpfellow_attended)
            #self.model.schedule.remove(gpfellow_attended)

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

from mesa import Agent
from workforce.person_agent import PersonAgent
from workforce.person_properties import calcAge, calcSex, calcName
import numpy
import logging

# Create a logger for debugging
logger = logging.getLogger('agent')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('workforce.log')
fh.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.info('Running agent.py')

# A function for generating a time in training
def calcYearsInTraining(steps):
    yearsInTraining = 0 if steps > 0 else round(numpy.random.random() * 5)
    return yearsInTraining
def calcYearsOutTraining(age):
    yearsOutTraining = age - 25
    return yearsOutTraining

class GPFellow(PersonAgent):
    """
    A gpfellow that ages, and sometimes trains a trainee.
    """
    def __init__(self, unique_id, pos, model, moore, age, sex, nickname):
        super().__init__(unique_id, pos, model, moore, age, sex, nickname)
        self.yearsOutTraining = calcYearsOutTraining(self.age)

    def step(self):
        """
        A model step: Age by one year
        """
        #self.random_move()
        inworkforce = True
        # Age the gpfellow
        self.age += 1
        self.yearsOutTraining += 1

        # Exit the workforce
        #logger.info('self.model.gpfellow_retirement_age: '+str(self.model.gpfellow_retirement_age))
        if self.age > self.model.gpfellow_retirement_age:
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            inworkforce = False

        # Start training a new trainee
        if inworkforce and self.random.random() < self.model.gpfellow_trained_trainee:
            age = calcAge(25,2)
            sex = calcSex()
            nickname = calcName(sex)
            trainee = Trainee(
                self.model.next_id(), self.pos, self.model, self.moore, age, sex, nickname
            )
            self.model.grid.place_agent(trainee, self.pos)
            trainee.random_move()
            self.model.schedule.add(trainee)

class Trainee(PersonAgent):
    """
    A trainee that ages, becomes a fellow.
    """
    def __init__(self, unique_id, pos, model, moore, age, sex, nickname):
        super().__init__(unique_id, pos, model, moore, age, sex, nickname)
        #logger.info(self.model.schedule.steps)
        self.yearsInTraining = calcYearsInTraining(self.model.schedule.steps)

    def step(self):
        """
        A model step: Age by one year
        """
        inworkforce = True
        # Age the gpfellow
        self.age += 1
        self.yearsInTraining += 1

        # Becomes a gpfellow
        if self.yearsInTraining >= self.model.trainee_train_period:
            # remove self
            self.model.grid._remove_agent(self.pos, self)
            self.model.schedule.remove(self)
            inworkforce = False
            # add gpfellow with my properties
            newGPFellow = GPFellow(
                self.model.next_id(), self.pos, self.model, self.moore, self.age, self.sex, self.nickname
            )
            self.model.grid.place_agent(newGPFellow, self.pos)
            self.model.schedule.add(newGPFellow)
            inworkforce = False


class Patient(PersonAgent):
    """
    A patient that walks around, reproduces (asexually) and attends gpfellows.
    """
    def __init__(self, unique_id, pos, model, moore, age, sex, nickname):
        super().__init__(unique_id, pos, model, moore, age, sex, nickname)
        self.attendance_count = 0

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
            self.attendance_count += 1
            
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
                age = 0
                sex = calcSex()
                nickname = calcName(sex)
                baby = Patient(
                    self.model.next_id(), self.pos, self.model, self.moore, age, sex, nickname 
                )
                self.model.grid.place_agent(baby, baby.pos)
                self.model.schedule.add(baby)

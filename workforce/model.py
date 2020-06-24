"""
Patient-GPFellow workforce model
"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from workforce.agents import GPFellow, Patient, Trainee
from workforce.schedule import RandomActivationByBreed
from workforce.person_properties import calcAge, calcSex, calcName

import numpy
import logging
import names

# Create a logger for debugging
logger = logging.getLogger('model')
logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('workforce.log')
fh.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)
logger.info('Running model.py')

class PatientGPFellow(Model):
    """
    Patient-GPFellow Model
    """

    height = 30
    width = 30

    initial_gpfellows = 50
    initial_trainees = 5
    initial_patients = 0

    patient_reproduce = 0.05
    gpfellow_trained_trainee = 0.05
    gpfellow_retirement_age = 65
    trainee_train_period = 5

    verbose = False  # Print-monitoring

    description = (
        "A model for simulating patient and gpfellow workforce ecosystem modelling."
    )
    # initialise with parameters (non positional) with defaults
    def __init__(
        self,
        height=20,
        width=20,
        initial_gpfellows=50,
        initial_trainees=5,
        initial_patients=0,
        patient_reproduce=0.0,
        gpfellow_trained_trainee=0.05,
        gpfellow_retirement_age=65,
        trainee_train_period=5,
    ):
        """
        Create a new Patient-GPFellow model with the given parameters.

        Args:
            initial_gpfellows: Number of gpfellow to start with
            initial_patients: Number of wolves to start with
            patient_reproduce: Probability of each patient reproducing each step
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_gpfellows = initial_gpfellows
        self.initial_patients = initial_patients
        self.initial_trainees = initial_trainees
        self.patient_reproduce = patient_reproduce
        self.gpfellow_retirement_age = gpfellow_retirement_age
        self.trainee_train_period = trainee_train_period

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Patients": lambda m: m.schedule.get_breed_count(Patient),
                "GPFellows": lambda m: m.schedule.get_breed_count(GPFellow),
                "Trainees": lambda m: m.schedule.get_breed_count(Trainee),
            }
        )

        # Initialise by creating gpfellows:
        for i in range(self.initial_gpfellows):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            age = calcAge(45,5)
            sex = calcSex()
            nickname = calcName(sex)
            gpfellow = GPFellow(self.next_id(), (x, y), self, True, age, sex, nickname)
            self.grid.place_agent(gpfellow, (x, y))
            self.schedule.add(gpfellow)

        # Initialise by creating trainees:
        for i in range(self.initial_trainees):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            age = calcAge(25, 2)
            sex = calcSex()
            nickname = calcName(sex)
            trainee = Trainee(self.next_id(), (x, y), self, True, age, sex, nickname)
            self.grid.place_agent(trainee, (x, y))
            self.schedule.add(trainee)

        # Initialise by creating patients:
        for i in range(self.initial_patients):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            age = calcAge(25, 2)
            sex = calcSex()
            nickname = calcName(sex)
            patient = Patient(self.next_id(), (x, y), self, True, age, sex, nickname)
            self.grid.place_agent(patient, (x, y))
            self.schedule.add(patient)

        self.running = True
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        # collect data
        self.datacollector.collect(self)
        if self.verbose:
            print(
                [
                    self.schedule.time,
                    self.schedule.get_breed_count(Patient),
                    self.schedule.get_breed_count(GPFellow),
                    self.schedule.get_breed_count(Trainees),
                ]
            )

    def run_model(self, step_count=200):

        if self.verbose:
            print("Initial number patients: ", self.schedule.get_breed_count(Patient))
            print("Initial number gpfellows: ", self.schedule.get_breed_count(GPFellow))
            print("Initial number trainees: ", self.schedule.get_breed_count(Trainees))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print("Final number patients: ", self.schedule.get_breed_count(Patient))
            print("Final number gpfellows: ", self.schedule.get_breed_count(GPFellow))
            print("Final number trainees: ", self.schedule.get_breed_count(Trainees))

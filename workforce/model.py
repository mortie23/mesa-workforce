"""
Patient-Provider workforce model
"""

from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from workforce.agents import Provider, Patient, GrassPatch
from workforce.schedule import RandomActivationByBreed


class PatientProvider(Model):
    """
    Patient-Provider Model
    """

    height = 30
    width = 30

    initial_providers = 100
    initial_patients = 0

    provider_reproduce = 0.04
    patient_reproduce = 0.0

    patient_gain_from_food = 0

    grass = False
    grass_regrowth_time = 0
    provider_gain_from_food = 4

    verbose = False  # Print-monitoring

    description = (
        "A model for simulating patient and provider workforce ecosystem modelling."
    )

    def __init__(
        self,
        height=20,
        width=20,
        initial_providers=100,
        initial_patients=0,
        provider_reproduce=0.04,
        patient_reproduce=0.0,
        patient_gain_from_food=0,
        grass=False,
        grass_regrowth_time=0,
        provider_gain_from_food=4,
    ):
        """
        Create a new Patient-Provider model with the given parameters.

        Args:
            initial_providers: Number of provider to start with
            initial_patients: Number of wolves to start with
            provider_reproduce: Probability of each provider reproducing each step
            patient_reproduce: Probability of each patient reproducing each step
            patient_gain_from_food: age a patient gains from eating a provider
            grass: Whether to have the provider eat grass for age
            grass_regrowth_time: How long it takes for a grass patch to regrow
                                 once it is eaten
            provider_gain_from_food: age provider gain from grass, if enabled.
        """
        super().__init__()
        # Set parameters
        self.height = height
        self.width = width
        self.initial_providers = initial_providers
        self.initial_patients = initial_patients
        self.provider_reproduce = provider_reproduce
        self.patient_reproduce = patient_reproduce
        self.patient_gain_from_food = patient_gain_from_food
        self.grass = grass
        self.grass_regrowth_time = grass_regrowth_time
        self.provider_gain_from_food = provider_gain_from_food

        self.schedule = RandomActivationByBreed(self)
        self.grid = MultiGrid(self.height, self.width, torus=True)
        self.datacollector = DataCollector(
            {
                "Patients": lambda m: m.schedule.get_breed_count(Patient),
                "Providers": lambda m: m.schedule.get_breed_count(Provider),
            }
        )

        # Create provider:
        for i in range(self.initial_providers):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            age = self.random.randrange(2 * self.provider_gain_from_food)
            provider = Provider(self.next_id(), (x, y), self, True, age)
            self.grid.place_agent(provider, (x, y))
            self.schedule.add(provider)

        # Create wolves
        for i in range(self.initial_patients):
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            age = self.random.randrange(2 * self.patient_gain_from_food)
            patient = Patient(self.next_id(), (x, y), self, True, age)
            self.grid.place_agent(patient, (x, y))
            self.schedule.add(patient)

        # Create grass patches
        if self.grass:
            for agent, x, y in self.grid.coord_iter():

                fully_grown = self.random.choice([True, False])

                if fully_grown:
                    countdown = self.grass_regrowth_time
                else:
                    countdown = self.random.randrange(self.grass_regrowth_time)

                patch = GrassPatch(self.next_id(), (x, y), self, fully_grown, countdown)
                self.grid.place_agent(patch, (x, y))
                self.schedule.add(patch)

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
                    self.schedule.get_breed_count(Provider),
                ]
            )

    def run_model(self, step_count=200):

        if self.verbose:
            print("Initial number wolves: ", self.schedule.get_breed_count(Patient))
            print("Initial number provider: ", self.schedule.get_breed_count(Provider))

        for i in range(step_count):
            self.step()

        if self.verbose:
            print("")
            print("Final number wolves: ", self.schedule.get_breed_count(Patient))
            print("Final number provider: ", self.schedule.get_breed_count(Provider))

from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from workforce.agents import Patient, GPFellow, Trainee
from workforce.model import PatientGPFellow


def workforce_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is GPFellow:
        portrayal["Shape"] = "workforce/resources/dr.png"
        portrayal["Layer"] = 1
        portrayal["Age"] = agent.age
        portrayal["Sex"] = agent.sex

    if type(agent) is Trainee:
        portrayal["Shape"] = "workforce/resources/trainee.png"
        portrayal["Layer"] = 1
        portrayal["Age"] = agent.age
        portrayal["Sex"] = agent.sex

    elif type(agent) is Patient:
        portrayal["Shape"] = "workforce/resources/patient.png"
        portrayal["Layer"] = 1
        portrayal["Age"] = agent.age

    return portrayal


canvas_element = CanvasGrid(workforce_portrayal, 20, 20, 500, 500)

# Define the Line chart elements
chart_element = ChartModule(
    [{"Label": "Patients", "Color": "#AA0000"}
    , {"Label": "GPFellows", "Color": "#666666"}
    , {"Label": "Trainees", "Color": "#32a885"}
    ]
)

model_params = {
    "initial_gpfellows": UserSettableParameter(
        "slider", "Initial GPFellow Population", 100, 10, 300
    ),
    "initial_patients": UserSettableParameter(
        "slider", "Initial Patient Population", 50, 10, 300
    ),
    "patient_reproduce": UserSettableParameter(
        "slider",
        "Patient Reproduction Rate",
        0.05,
        0.01,
        1.0,
        0.01,
        description="The rate at which patient agents reproduce.",
    ),
    "gpfellow_trained_trainee": UserSettableParameter(
        "slider", "Trainee enters", 
        0.05,
        0.01,
        1.0,
        0.01,
        description="The rate at which trainees start with a GP Fellow",
    ),
}

# Server instance
server = ModularServer(
    PatientGPFellow, [canvas_element, chart_element]
    , "Patient GPFellow Workforce"
    , model_params
)
server.port = 8521

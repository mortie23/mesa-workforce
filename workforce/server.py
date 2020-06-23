from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.modules import CanvasGrid, ChartModule
from mesa.visualization.UserParam import UserSettableParameter

from workforce.agents import Patient, Provider, GrassPatch
from workforce.model import PatientProvider


def workforce_portrayal(agent):
    if agent is None:
        return

    portrayal = {}

    if type(agent) is Provider:
        portrayal["Shape"] = "workforce/resources/dr.png"
        # https://icons8.com/web-app/433/provider
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["Age"] = round(agent.age, 1)

    elif type(agent) is Patient:
        portrayal["Shape"] = "workforce/resources/patient.png"
        # https://icons8.com/web-app/36821/German-Shepherd
        portrayal["scale"] = 0.9
        portrayal["Layer"] = 2
        portrayal["Age"] = round(agent.age, 1)

    elif type(agent) is GrassPatch:
        if agent.fully_grown:
            portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
        else:
            portrayal["Color"] = ["#84e184", "#adebad", "#d6f5d6"]
        portrayal["Shape"] = "rect"
        portrayal["Filled"] = "true"
        portrayal["Layer"] = 0
        portrayal["w"] = 1
        portrayal["h"] = 1

    return portrayal


canvas_element = CanvasGrid(workforce_portrayal, 20, 20, 500, 500)
chart_element = ChartModule(
    [{"Label": "Patients", "Color": "#AA0000"}, {"Label": "Providers", "Color": "#666666"}]
)

model_params = {
    "grass": UserSettableParameter("checkbox", "Grass Enabled", False),
    "grass_regrowth_time": UserSettableParameter(
        "slider", "Grass Regrowth Time", 20, 1, 50
    ),
    "initial_providers": UserSettableParameter(
        "slider", "Initial Provider Population", 100, 10, 300
    ),
    "provider_reproduce": UserSettableParameter(
        "slider", "Provider Reproduction Rate", 0.04, 0.01, 1.0, 0.01
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
    "patient_gain_from_food": UserSettableParameter(
        "slider", "Patient Gain From Food Rate", 20, 1, 50
    ),
    "provider_gain_from_food": UserSettableParameter(
        "slider", "Provider Gain From Food", 4, 1, 10
    ),
}

server = ModularServer(
    PatientProvider, [canvas_element, chart_element], "Patient Provider Workforce", model_params
)
server.port = 8521

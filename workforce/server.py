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
        portrayal["I'm a"] = 'GP Fellow'
        portrayal["Layer"] = 1
        portrayal["Age"] = agent.age
        portrayal["Sex"] = agent.sex
        portrayal["Nickname"] = agent.nickname

    if type(agent) is Trainee:
        portrayal["Shape"] = "workforce/resources/trainee.png"
        portrayal["I'm a"] = 'Trainee'
        portrayal["Layer"] = 1
        portrayal["Age"] = agent.age
        portrayal["Sex"] = agent.sex
        portrayal["Nickname"] = agent.nickname
        portrayal["Years In Training"] = agent.yearsInTraining


    elif type(agent) is Patient:
        portrayal["Shape"] = "workforce/resources/patient.png"
        portrayal["I'm a"] = 'Patient'
        portrayal["Layer"] = 1
        portrayal["Age"] = agent.age
        portrayal["Sex"] = agent.sex
        portrayal["Nickname"] = agent.nickname
        portrayal["Attendances"] = agent.attendance_count

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
        "slider", "Initial GPFellow Population (Headcount)", 5, 1, 300, 1,
        description="Number of initial GP Fellows",
    ),
    "initial_trainees": UserSettableParameter(
        "slider", "Initial Trainee Population (Headcount)", 1, 1, 300, 1,
        description="Number of initial Trainees",
    ),
    "initial_patients": UserSettableParameter(
        "slider", "Initial Patient Population (Headcount)", 10, 0, 1000, 1,
        description="Number of initial patients",
    ),
    "patient_reproduce": UserSettableParameter(
        "slider",
        "Patient Reproduction Rate (Probability)", 0.02, 0.01, 0.1, 0.01,
        description="The rate at which patient agents reproduce.",
    ),
    "gpfellow_trained_trainee": UserSettableParameter(
        "slider", "Trainee enters (Probability)",  0.0001, 0.0001, 0.0002, 0.00005,
        description="The rate at which trainees start with a GP Fellow",
    ),
    "gpfellow_retirement_age": UserSettableParameter(
        "slider", "GP Retirement Age (Yrs)",65, 40, 85, 1,
        description="",
    ),
    "trainee_train_period": UserSettableParameter(
        "slider", "Trainee Train Period (Yrs)", 5, 1, 15, 1,
        description="",
    ),
}

# Server instance
server = ModularServer(
    PatientGPFellow, [canvas_element, chart_element]
    , "Patient GPFellow Workforce"
    , model_params
)
server.port = 8521

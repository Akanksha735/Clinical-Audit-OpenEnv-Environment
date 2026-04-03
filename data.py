from models import Patient, Decision

# Each case = patient + doctor decision + correct audit
DATASET = [

    {
        "patient": Patient(
            symptoms=["fever", "cough"],
            history=["no chronic disease"]
        ),
        "decision": Decision(
            text="Prescribed antibiotics"
        ),
        "ground_truth": {
            "missing": ["lab test"],
            "error": "antibiotics unnecessary",
            "risk": "antibiotic resistance"
        }
    },

    {
        "patient": Patient(
            symptoms=["chest pain"],
            history=["diabetes"]
        ),
        "decision": Decision(
            text="Discharged without ECG"
        ),
        "ground_truth": {
            "missing": ["ECG test"],
            "error": "serious condition ignored",
            "risk": "heart attack risk"
        }
    },

    {
        "patient": Patient(
            symptoms=["headache"],
            history=["migraine"]
        ),
        "decision": Decision(
            text="Prescribed painkillers"
        ),
        "ground_truth": {
            "missing": ["severity assessment"],
            "error": "no major error",
            "risk": "low risk"
        }
    },

    {
        "patient": Patient(
            symptoms=["weight loss", "fatigue"],
            history=["smoker"]
        ),
        "decision": Decision(
            text="Advised rest only"
        ),
        "ground_truth": {
            "missing": ["cancer screening"],
            "error": "serious symptoms ignored",
            "risk": "late diagnosis"
        }
    },

    {
        "patient": Patient(
            symptoms=["high fever", "rash"],
            history=["recent travel"]
        ),
        "decision": Decision(
            text="Prescribed paracetamol"
        ),
        "ground_truth": {
            "missing": ["infection test"],
            "error": "possible infectious disease ignored",
            "risk": "disease spread"
        }
    }

]
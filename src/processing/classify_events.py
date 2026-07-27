"""Classification order: rules → manual review → TF-IDF/logistic regression → optional transformer."""
from dataclasses import dataclass
@dataclass
class ClassificationResult:
    category_code:str|None
    confidence:float|None
    method:str
    needs_review:bool
    explanation:str

def rule_based_classify(title:str,body_text:str)->ClassificationResult:
    # TODO: normalize Turkish text, count taxonomy evidence, abstain when unclear.
    raise NotImplementedError

def train_baseline_classifier(reviewed_events):
    # TODO: chronological split, TF-IDF, logistic regression, per-class F1, calibration, model_versions.
    raise NotImplementedError

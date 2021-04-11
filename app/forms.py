from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, RadioField, validators
from wtforms.validators import DataRequired


class DemographicsForm(Form):
    age = RadioField(
        "age",
        [validators.Optional()],
        choices=[
            ("0-19", "0-19"),
            ("20-29", "20-29"),
            ("30-39", "30-39"),
            ("40+", "40+"),
        ],
    )
    gender = RadioField(
        "gender",
        [validators.Optional()],
        choices=[("Male", "Male"), ("Female", "Female")],
    )
    degree = StringField("degree", [validators.Length(max=25), validators.required()])
    vision = RadioField(
        "vision", [validators.Required()], choices=[("1", "Yes"), ("0", "No")]
    )


class IntroductionForm(Form):
    familiar = RadioField(
        "familiar",
        [validators.Required()],
        choices=[
            ("0", "This topic is completely new to me."),
            ("1", "I know a little bit about this topic."),
            ("2", "I have approximate knowledge about this topic."),
            ("3", "I know a considerable amount about this topic"),
            ("4", "This topic is my field of expertise."),
        ],
    )


class StressForm(Form):
    stress = RadioField(
        "stress",
        [validators.Required()],
        choices=[
            ("0", "I am much less stressed or anxious than usual."),
            ("1", "I am slightly less stressed or anxious than usual."),
            ("2", "I am no more stressed or anxious than usual"),
            ("3", "I am slightly more stressed or anxious than usual."),
            ("4", "I am much more stressed and/or anxious than usual."),
        ],
    )


class DocumentsForm(Form):
    confidence = RadioField(
        "confidence",
        [validators.Optional()],
        choices=[("0", "Low"), ("1", "Average"), ("2", "High")],
        default="1",
    )
    selection = RadioField(
        "selection",
        [validators.Optional()],
        choices=[("1", "Yes, this relates to "), ("0", "No, this does not relate to ")],
    )

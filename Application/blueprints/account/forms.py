from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileSize, FileAllowed

class CompanyFinancialForm(FlaskForm):
    csv_file = FileField("Upload CSV", validators=[DataRequired(), FileAllowed(('csv',), "Only CSVs are allowed!"), FileSize(max_size=100000, message="File must be within 100kb size!")])

    
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField

class RegistrationFormClass(FlaskForm):
    fname=StringField('First Name')
    lname = StringField('Last Name')
    address = StringField('Address')
    city = StringField('City')
    zip=StringField('Zip')
    state = StringField('State')
    age = StringField('Age')
    experience=StringField('Experience')
    income=StringField('Income')
    Married_choices = [('married', 'Yes'), ('single', 'No')]
    marriedyn = SelectField(u'Married', choices=Married_choices)
    #profession_choices = [('Python', 'Yes'), ('IT', 'No')]
    profession_choices =[('Air_traffic_controller', 'Air_traffic_controller'), ('Analyst', 'Analyst'),('Architect', 'Architect'),('Army_officer', 'Army_officer'),('Artist', 'Artist'),('Aviator', 'Aviator'),('Biomedical_Engineer', 'Biomedical_Engineer'),('Chartered_Accountant', 'Chartered_Accountant'),('Chef', 'Chef'),('Chemical_engineer', 'Chemical_engineer'),('Civil_engineer', 'Civil_engineer'),('Civil_servant', 'Civil_servant'),('Comedian', 'Comedian'),('Computer_hardware_engineer', 'Computer_hardware_engineer'),('Computer_operator', 'Computer_operator'),('Consultant', 'Consultant'),('Dentist', 'Dentist'),('Design_Engineer', 'Design_Engineer'),('Designer', 'Designer'),('Drafter', 'Drafter'),('Economist', 'Economist'),('Engineer', 'Engineer'),('Fashion_Designer', 'Fashion_Designer'),('Financial_Analyst', 'Financial_Analyst'),('Firefighter', 'Firefighter'),('Flight_attendant', 'Flight_attendant'),('Geologist', 'Geologist'),('Graphic_Designer', 'Graphic_Designer'),('Hotel_Manager', 'Hotel_Manager'),('Industrial_Engineer', 'Industrial_Engineer'),('Lawyer', 'Lawyer'),('Librarian', 'Librarian'),('Magistrate', 'Magistrate'),('Mechanical_engineer', 'Mechanical_engineer'),('Microbiologist', 'Microbiologist'),('Official', 'Official'),('Petroleum_Engineer', 'Petroleum_Engineer'),('Physician', 'Physician'),('Police_officer', 'Police_officer'),('Politician', 'Politician'),('Psychologist', 'Psychologist'),('Scientist', 'Scientist'),('Secretary', 'Secretary'),('Software_Developer', 'Software_Developer'),('Statistician', 'Statistician'),('Surgeon', 'Surgeon'),('Surveyor', 'Surveyor'),('Technical_writer', 'Technical_writer'),('Technician', 'Technician'),('Technology_specialist', 'Technology_specialist'),('Web_designer', 'Web_designer')]
    profession = SelectField(u'Profession', choices=profession_choices)
    house_choices = [('rented', 'Rented'), ('owned', 'owned'),('norent_noown','norent_noown')]
    houseownership = SelectField(u'House Ownership', choices=house_choices)
    car_choices = [(True, 'Yes'), (False, 'No')]
    carownership = SelectField(u'Car Ownership', choices=car_choices)
    currentjobyrs=StringField('Current Job Years')
    currenthouseyrs = StringField('Current Residence Years')
    #amount = StringField('Amount')
    #installment_rate = StringField('Installment Rate')
    #telephone=StringField('telephone')
    submit = SubmitField('Get Approval')


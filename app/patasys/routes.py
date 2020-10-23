# -*- coding: utf-8 -*- 
# import random
from app.calendar.cal_setup import get_calendar_service
from config import Config
from app.auth.routes import login
from flask import render_template, redirect, flash, request
from flask.helpers import url_for
from flask_login import login_required
from werkzeug.utils import redirect
from app.patasys import bp
from flask_login import current_user
from app.patasys.forms import AddPatientForm, AddDoctorForm, AddServiceForm, AddVisitForm
from app.models import Patient, Doctor, Service, Visit
from app import db
from datetime import datetime
from datetime import timedelta
import time
from config import Config


@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('patasys/index.html', title='Home')

@bp.app_template_filter('ctime')
def timectime(s):
    value = datetime.fromtimestamp(int(s))
    return value.strftime(Config.DATETIME_FORMAT)

# @login_required
# @bp.route('/add_dannie')
# def add_dannie():
#     names = [
#         'Ева',
#         'Марина',
#         'Мальвина',
#         'Надежда',
#         'Галина',
#         'Виолетта',
#         'Варвара',
#         'Амина',
#         'Алина',
#         'Алёна',
#         'Дарья',
#         'Джоан',
#         'Анастасия',
#         'Нонна',
#         'Кристина',
#         'Ксения',
#         'Корнелия',
#         'Лариса',
#     ]
#     families = [
#         'Акимова',
#         'Матвеева',
#         'Воробьёва',
#         'Дьякова',
#         'Воронцова',
#         'Голубева',
#         'Гришина',
#         'Дедова',
#         'Винокурова',
#         'Исаева',
#         'Соболева',
#         'Смирнова',
#         'Казакова',
#     ]
#     patronymics = [
#         'Ивановна',
#         'Петровна',
#         'Данииловна',
#         'Михайловна',
#         'Семёновна',
#         'Максимовна',
#         'Алишеровна',
#         'Мухаммедовна',
#         'Владиславовна',
#         'Артуровна',
#         'Лаврентьевна',
#         'Гордеевна',
#     ]
#     ages = [15,17,19,25,28,35,22,29,33,51]
#     phone_number = 89855552233

#     for i in range(2000):
#         n = random.randint(0,len(names)-1)
#         f = random.randint(0,len(families)-1)
#         p = random.randint(0,len(patronymics)-1)
#         a = random.randint(0,len(ages)-1)
#         pat = Patient(
#             first_name=names[n],
#             second_name=families[f],
#             patronymic=patronymics[p],
#             phone_number=phone_number,
#             age=ages[a],
#         )
#         db.session.add(pat)
    
#     db.session.commit()
#     flash('Done!')
#     return redirect(url_for('patasys.index'))


@login_required
@bp.route('/add_patient', methods=['GET', 'POST'])
def add_patient():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.index'))
    form = AddPatientForm()
    if form.validate_on_submit():
        patient = Patient(first_name=form.first_name.data, 
            second_name=form.second_name.data,
            phone_number=form.phone_number.data,
            patronymic=form.patronymic.data,
            medic=form.doctors.data,
            age=form.age.data,
        )
        db.session.add(patient)
        db.session.commit()
        flash('Новый пациент добавлен')
        return redirect(url_for('patasys.index'))
    return render_template('patasys/add_patient.html', title='Add Patient', form=form)

@login_required
@bp.route('/add_doctor', methods=['GET', 'POST'])
def add_doctor():
    # if current_user.is_authenticated:
    #     return redirect(url_for('main.index'))
    form = AddDoctorForm()
    if form.validate_on_submit():
        doctor = Doctor(
            first_name=form.first_name.data, 
            second_name=form.second_name.data,
            phone_number=form.phone_number.data,
            patronymic=form.patronymic.data,        
        )
        db.session.add(doctor)
        db.session.commit()
        flash('Новый доктор добавлен')
        return redirect(url_for('patasys.index'))
    return render_template('patasys/add_doctor.html', title='Add doctor', form=form)


@bp.route('/all_patients', methods=['GET', 'POST'])
@bp.route('/all_patients/<int:page>', methods=['GET', 'POST'])
@bp.route('/all_patients/<string:search>/<int:page>', methods=['GET', 'POST'])
@login_required
def all_patients(search=None, page=1):
    sort = ''
    # if request.method == 'POST':
    #     txt = request.form.get('txt')
    #     txt = txt.capitalize()
    #     if len(txt.split(' ')) > 1:
    #         flash('Пока что умею искать только по одному слову')
    #         return redirect(url_for('patasys.all_patients'))
    #     qwe = Patient.query.filter(
    #         (Patient.first_name.like(txt)) | (Patient.second_name.like(txt)) | (Patient.patronymic.like(txt))
    #     ).paginate(1, 1000, False)
    #     context = {
    #         'patients': qwe,
    #         'sort': sort
    #     }
    #     return render_template('patasys/all_patients.html', **context)
    
    args = request.args
    if "search" in args:
        txt = args.get('search')
        if len(txt.split(' ')) > 1:
            flash('Пока что умею искать только по одному слову')
            return redirect(url_for('patasys.all_patients'))
        search = txt.capitalize()
        qwe = Patient.query.filter(
                (Patient.first_name.like(search)) | (Patient.second_name.like(search)) | (Patient.patronymic.like(search))
            ).paginate(page, 5, False)
        context = {
            'patients': qwe,
            'sort': sort
        }
        return redirect(url_for('patasys.all_patients', search=txt, page=1))

    if search is not None:
        if len(search.split(' ')) > 1:
            flash('Пока что умею искать только по одному слову')
            return redirect(url_for('patasys.all_patients'))
        search = search.capitalize()
        qwe = Patient.query.filter(
                (Patient.first_name.like(search)) | (Patient.second_name.like(search)) | (Patient.patronymic.like(search))
            ).paginate(page, 5, False)
        context = {
            'patients': qwe,
            'sort': sort,
            'search': search,
            'page': page,
        }
        print(search)
        return render_template('patasys/all_patients.html', **context)

    
    # patients = Patient.query.order_by(Patient.second_name).all()
    if "name" in args:
        patients = Patient.query.order_by(Patient.first_name).paginate(page, Config.PATIENTS_PER_PAGE, False)
        sort='name'
    elif "second" in args:
        patients = Patient.query.order_by(Patient.second_name).paginate(page, Config.PATIENTS_PER_PAGE, False)
        sort='second'
    elif "patronymic" in args:
        patients = Patient.query.order_by(Patient.patronymic).paginate(page, Config.PATIENTS_PER_PAGE, False)
        sort='patronymic'
    else:
        patients = Patient.query.order_by(Patient.second_name).paginate(page, Config.PATIENTS_PER_PAGE, False)
        sort='second'

    
    context = {
        'patients': patients,
        'sort': sort,
        'page': page,
    }
    return render_template('patasys/all_patients.html', **context)


@login_required
@bp.route('/patient/<int:patient_id>/<int:funcc>', methods=['GET', 'POST'])
def view_patient(patient_id, funcc):
    # print(request.method)
    if request.method == "POST" and funcc==2:
        doc_id = request.form.get('doctor')
        # print(doc_id)
        doctor = Doctor.query.filter_by(id=doc_id).first()
        if doctor:
            patient = Patient.query.filter_by(id=patient_id).first()
            # print(patient)
            if patient.doctor_id == None:
                patient.doctor_id = doc_id
                db.session.add(patient)
                db.session.commit()
                flash('success')
                return redirect(url_for('patasys.view_patient',
                    patient_id=patient.id, funcc=1, 
                ))
            elif int(patient.doctor_id) != int(doc_id):
                patient.doctor_id = doc_id
                db.session.add(patient)
                db.session.commit()
                flash('success2')
                return redirect(url_for('patasys.view_patient',
                    patient_id=patient.id, funcc=1, 
                ))
            else:
                flash('У этого пациента уже назначен этот врач')
                return redirect(url_for('patasys.view_patient',
                    patient_id=patient.id, funcc=1, 
                ))
        else:
            flash('Такого врача нет')
            return redirect(url_for('patasys.index'))
    patient = Patient.query.filter_by(id=patient_id).first()
    doctor = Doctor.query.filter_by(id=patient.doctor_id).first()
    doctors = ''
    form = ''
    if (funcc == 2):
        doctors = Doctor.query.all()
    elif (funcc == 3):
        form = AddVisitForm()
        if form.validate_on_submit():
            tim = time.strptime(form.visit_time.data, Config.DATETIME_FORMAT)
            visit = Visit(
                visit_time = time.mktime(tim),
                patient_id = patient_id,
            )
            db.session.add(visit)

            
            service = get_calendar_service()
            start_time = datetime.fromtimestamp(time.mktime(tim))
            end_time = start_time+timedelta(hours=1)
            sum = patient.second_name + " " + patient.first_name
            description = f"""
ФИО пациента: {patient.second_name} {patient.first_name} {patient.patronymic}
Номер телефона: {patient.phone_number}
http://127.0.0.1:5000/patient/{str(patient.id)}/1
            """
            event_result = service.events().insert(calendarId=Config.CALENDAR_ID,
                body={
                    "summary": sum,
                    "description": description,
                    "start": {"dateTime": start_time.isoformat(), "timeZone": 'Europe/Moscow'},
                    "end": {"dateTime": end_time.isoformat(), "timeZone": 'Europe/Moscow'},
                    "colorId": 2,
                }
            ).execute()
            print("created event")
            db.session.commit()
            flash('Время успешно записано')
            return redirect(url_for('patasys.view_patient',
                patient_id=patient.id, funcc=1, 
            ))
        
    current_time = time.time()
    context = {
        'patient': patient,
        'doctor': doctor,
        'doctors': doctors,
        'current_time': current_time,
    }
    return render_template('patasys/view_patient.html', **context, form=form) 


@login_required
@bp.route('/add_service', methods=['GET', 'POST'])
def add_service():
    form = AddServiceForm()
    if form.validate_on_submit():
        service = Service(
            name=form.name.data,
            cost=form.cost.data,
            code=form.code.data,
        )
        db.session.add(service)
        db.session.commit()
        flash('Услуга добавлена')
        return redirect(url_for('patasys.index'))
    return render_template('patasys/add_service.html', title='add service', form=form)


@login_required
@bp.route('/schedule')
def schedule():
    # hours = int(datetime.today().strftime("%H"))
    # minutes = int(datetime.today().strftime("%M"))
    # # visits = Visit.query.filter(
    # #     Visit.visit_time>=(int(time.time())-(hours*3600-minutes*60)),
    # #     Visit.visit_time<=(int(time.time())+((24-hours)*3600-minutes*60)),
           
    # # )
    # visits = Visit.query.all()
    # pats = {}
    # for v in visits:
    #     pa = Patient.query.filter_by(id=v.patient_id)
    #     q = {v.patient_id:pa}
    #     pats.update(q)
    service = get_calendar_service()
    now = (datetime.utcnow()-timedelta(days=1)).isoformat() + 'Z'
    now_end = (datetime.utcnow()+timedelta(days=30)).isoformat() + 'Z'
    # now = datetime.datetime.now().date()
    # start = datetime.datetime(2020, 10, 23, 18).isoformat()
    # end = datetime.datetime(2020, 10, 23, 19).isoformat()

    events_result = service.events().list(calendarId=Config.CALENDAR_ID, timeMin=now,
                                        timeMax=now_end, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    return render_template('patasys/schedule.html', events=events)
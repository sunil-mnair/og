from app import db
from datetime import *
from pytz import timezone
localtz = timezone('GMT+0')

from flask_login import UserMixin,current_user,login_user,logout_user
from flask_admin import Admin,AdminIndexView,BaseView,expose
from flask_admin.contrib.sqla import ModelView

from flask import url_for,redirect,request

class User(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return self.username

class RoomMaster(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roomName = db.Column(db.String(100), unique=True)
    roomType = db.Column(db.String(10))
    maxRevenue = db.Column(db.Integer)

    created_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(localtz))
    modified_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(localtz))

    def __repr__(self):
        return str(self.roomName)

class RoomOccupancy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    roomNumber = db.Column(db.Integer,db.ForeignKey('room_master.id'))

    checkIn = db.Column(db.DateTime)
    checkOut = db.Column(db.DateTime)

    mainGuestName = db.Column(db.String(100))
    guests = db.Column(db.Integer)
  
    amount = db.Column(db.Integer)

    created_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(localtz))
    modified_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(localtz))

    room_master = db.relationship('RoomMaster', backref=db.backref('room_occupancy', lazy='dynamic'))

    def __repr__(self):
        return f'{self.id}-{self.checkIn}'


class OperatingCosts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)
    costType = db.Column(db.String(100))
    costDescription = db.Column(db.Text)
    amount = db.Column(db.Integer)

    created_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(localtz))
    modified_dt = db.Column(db.DateTime, nullable = True,
    default = datetime.now(localtz))

    def __repr__(self):
        return str(self.id)

class AllModelView(ModelView):
    can_delete = False
    page_size = 5
    can_create = False
    can_edit = False
    can_delete = False
    
    column_list = ['username']
    
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'),next=request.url)


class RoomMasterView(ModelView):

    can_delete = False
    can_edit = True
    page_size = 7
    column_searchable_list = ['id','roomName']
    column_filters = ['id','roomName']
    column_hide_backrefs = False

    column_list = ['id','roomName','roomType','maxRevenue']

    column_labels = {
    'roomName': 'Room Name',
    'roomType': 'Room Type',
    'maxRevenue': 'Daily Max Revenue (£)'
    }
    
    form_excluded_columns = ['created_dt', 'modified_dt']

    # With Model View, it does not show Rich Text Editor
    create_modal = True
    edit_modal = True

    form_args = {
    'roomName': {
        'label': 'Room Name'
    },
    'roomType': {
        'label': 'Room Type'
    },
    'maxRevenue': {
        'label': 'Daily Max Revenue (£)'
    }
    }

    def is_accessible(self):
        return current_user.is_authenticated
        
    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'))

class RoomOccupancyView(ModelView):

    can_delete = True
    can_export = True

    page_size = 25
    column_searchable_list = ['mainGuestName','amount']
    column_filters = ['id','roomNumber','checkIn','checkOut','mainGuestName','amount']
    column_hide_backrefs = False

    # 'room' used because thats the name of the backref
    column_list = ['id','room_master','checkIn','checkOut','amount','guests','mainGuestName']

    column_labels = {
    'id': 'ID',
    'room_master': 'Room',
    'amount': 'Revenue (£)',
    'mainGuestName': 'Main Guest Name'
    }
    
    form_excluded_columns = ['created_dt', 'modified_dt']

    # With Model View, it does not show Rich Text Editor
    create_modal = True
    edit_modal = True

    form_args = {
    'roomNumber': {
        'label': 'Room'
    }
    }

#     form_ajax_refs = {
#     'room_master': {
#         'fields': ['roomName'],
#         'page_size': 10
#     }
# }


    def is_accessible(self):
        return current_user.is_authenticated
        
    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'))

class OperatingCostsView(ModelView):

    can_delete = True
    page_size = 25
    column_searchable_list = ['id','costType']
    column_filters = ['id','costType']
    column_hide_backrefs = False

    column_list = ['id','costType','costDescription','amount']

    column_labels = {
    'id': 'No.',
    'costType': 'Cost Type',
    'costDescription': 'Cost Description',
    'amount': 'Amount (£)'
    }
    
    form_excluded_columns = ['created_dt', 'modified_dt']

    # With Model View, it does not show Rich Text Editor
    # create_modal = True
    # edit_modal = True


    def is_accessible(self):
        return current_user.is_authenticated
        
    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'))

class CustomView(BaseView):
    @expose('/')
    def index(self):
        return self.render('dashboard.html')



class MainAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return current_user.is_authenticated
    
    def inaccessible_callback(self,name,**kwargs):
        return redirect(url_for('login'),next=request.url)
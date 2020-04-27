from app import db

from flask import current_app
registrations=db.Table('registrations',db.Column('user_id',db.Integer,db.ForeignKey('users.id')),db.Column('cult_id',db.Integer,db.ForeignKey('cults.id')))
from werkzeug.security import generate_password_hash,check_password_hash
from itsdangerous import URLSafeTimedSerializer,SignatureExpired,Serializer


class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String(64),index=True)
    user_landmark=db.Column(db.UnicodeText)
    user_city=db.Column(db.Unicode,index=True)
    user_state=db.Column(db.Unicode)
    user_Country=db.Column(db.Unicode)
    user_pincode=db.Column(db.Integer)
    user_lat=db.Column(db.Float)
    user_long=db.Column(db.Float)
    user_intrested_field1=db.Column(db.Unicode,index=True)
    user_intrested_field2=db.Column(db.Unicode,index=True)
    user_intrested_field3=db.Column(db.Unicode,index=True)
    user_intrested_field4=db.Column(db.Unicode,index=True)
    user_social_profile_url=db.Column(db.Unicode)
    user_email_adrs=db.Column(db.Unicode,index=True,unique=True)
    user_password=db.Column(db.Unicode)
    user_organisation_name=db.Column(db.Unicode)
    user_if_Founder=db.Column(db.Boolean)
    user_image=db.Column(db.LargeBinary)
    user_founder_cult= db.relationship('Cult',backref='founder',uselist=False)
    user_enroll_cults=db.relationship('Cult',secondary=registrations,backref=db.backref('enrolled_users',lazy='dynamic'),lazy='dynamic')
    user_given_ratings=db.relationship('Rating',backref='users',lazy='dynamic')
    user_email_verified=db.Column(db.Boolean)
    password_hash=db.Column(db.Unicode)
    def generate_auth_token(self, expiration):
        s = token_serializer=URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        return token_serializer.dumps(self.id,salt='email-confirmation')
    
    @staticmethod
    def verify_auth_token(token):
        s = token_serializer=URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token,salt='email-confirmation',max_age=1000)
        except:
            return None
        print(data)
        return User.query.get(int(data))
    
    def give_rating(self,cultid,rate):
        rating=Rating(user_id=self.id,cult_id=cultid,rating=rate)
        db.session.add(rating)
        db.session.commit()
    
    @property
    def user_password(self):
        raise AttributeError('password is not readable attribute')
    
    @user_password.setter
    def user_password(self,user_password):
        self.password_hash=generate_password_hash(user_password)
        
    def verify_password(self,user_password):
        return check_password_hash(self.password_hash,user_password)
    
    def __repr__(self):
        return "this is user {} ".format(self.user_name)
#founder containg details of the founder    
#have users attribute for enrolled users    
class Cult(db.Model):
    __tablename__='cults'
    id=db.Column(db.Integer,primary_key=True)
    cult_name=db.Column(db.Unicode,index=True)
    cult_lat=db.Column(db.Float)
    cult_long=db.Column(db.Float)
    cult_work_field1=db.Column(db.Unicode,index=True)
    cult_work_field2=db.Column(db.Unicode,index=True)
    cult_work_field3=db.Column(db.Unicode,index=True)
    cult_work_field4=db.Column(db.Unicode,index=True)
    cult_landmark=db.Column(db.UnicodeText)
    cult_city=db.Column(db.Unicode,index=True)
    cult_state=db.Column(db.Unicode)
    cult_country=db.Column(db.Unicode)
    cult_pincode=db.Column(db.Integer)
    cult_founder_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    cult_quote_line=db.Column(db.UnicodeText)
    cult_image=db.Column(db.LargeBinary)
    cult_rating=db.Column(db.SmallInteger)
    cult_posts=db.relationship('Post',backref='cult',lazy='dynamic')
    cult_rating=db.relationship('Rating',backref='cult',lazy='dynamic')
    
    def __repr__(self):
        return "this is Cult : {} ".format(self.cult_name)    
    
class Post(db.Model): 
    __tablename__='posts'
    id=db.Column(db.Integer,primary_key=True)
    cult_id=db.Column(db.Integer,db.ForeignKey('cults.id'),nullable=False)
    post_content=db.Column(db.UnicodeText)
    post_banner_image=db.Column(db.LargeBinary)
    post_application_url=db.Column(db.Unicode)
    
    def __repr__(self):
        return "this is post{} ".format(self.post_content)    
        
class Rating(db.Model):
    __tablename__='ratings'
    id=db.Column(db.Integer,primary_key=True)
    cult_id=db.Column(db.Integer,db.ForeignKey('cults.id'),nullable=False)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),nullable=False)
    rating=db.Column(db.Integer)

    def __repr__(self):
        return "this is RATING() FROM USER{} TO CULT{} ".format(self.rating,self.user_id,self.cult_id)    
    
#new_user2=User(user_name='triyambhkam',user_landmark='parashar k bada', user_city= 'Gwalior', user_state='Uttranchal', user_Country='India', user_pincode= 474321, user_lat= 23.23, user_long=23.09, user_intrested_field1='product_development', user_intrested_field2 = 'technology', user_intrested_field3 = 'singing', user_intrested_field4='Cooking', user_social_profile_url= 'https://www.linkedin.com/in/kuldeep-parashar-5aa9a212a/', user_email_adrs= 'kparashar17290@gmail.com', user_password= 'kido#123456', user_organisation_name= 'Amity University')


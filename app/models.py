from app import db

from flask import current_app,jsonify
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
    user_given_ratings=db.relationship('Rating',backref='users',lazy='immediate')
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
    
    #register new user 
    @staticmethod
    def register_user(data):
        new_user=User(user_name=data.get('user_name'),user_landmark=data.get('user_landmark'), user_city= data.get('user_city'), user_state=data.get('user_sate'), user_Country=data.get('user_Country'), user_pincode=data.get('user_pincode'), user_lat=data.get('user_lat'), user_long=data.get('user_long'), user_intrested_field1=data.get('user_intrested_field1'), user_intrested_field2 = data.get('user_intrested_field2'), user_intrested_field3 = data.get('user_intrested_field3'), user_intrested_field4=data.get('user_intrested_field4'), user_social_profile_url= data.get('user_social_profile_url'), user_email_adrs= data.get('user_email_adrs'), user_password= data.get('user_password'), user_organisation_name=data.get('user_organisation_name'))
        db.session.add(new_user)
        db.session.commit()
        return new_user
        
    def user_profile(self):
        return {"user_name":self.user_name}
        
        
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
    cult_posts=db.relationship('Post',backref='cult',lazy='immediate')
    cult_rating=db.relationship('Rating',backref='cult',lazy='immediate')
    
    def __repr__(self):
        return "this is Cult : {} ".format(self.cult_name)  
    
    def get_avg_rating(self):
        tot_rating=0
        rating_count=0
        for rating in self.cult_rating:
            tot_rating+=rating.rating
            rating_count+=1
        if rating_count==0:
            return 0
        return(tot_rating/rating_count)
    
    def get_compact_data(self):
        return {"cult_id":self.id,"cult_name":self.cult_name,"cult_rating":self.get_avg_rating(),"cult_quote":self.cult_quote_line,"cult_work_field1":self.cult_work_field1,"cult_work_field2":self.cult_work_field2,"cult_founder_id":self.cult_founder_id}
        #register new user 
    
    @staticmethod
    def register_cult(data,FID):
        new_cult=Cult(cult_founder_id=FID,cult_name=data.get('cult_name'),cult_landmark=data.get('cult_landmark'), cult_city= data.get('cult_city'), cult_state=data.get('cult_state'), cult_country=data.get('cult_Country'), cult_pincode=data.get('cult_pincode'), cult_lat=data.get('cult_lat'), cult_long=data.get('cult_long'), cult_work_field1=data.get('cult_work_field1'), cult_work_field2 = data.get('cult_work_field2'),cult_quote_line=data.get('cult_quote_line'))
        db.session.add(new_cult)
        db.session.commit()
        return new_cult
    
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


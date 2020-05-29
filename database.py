import sqlalchemy as db
from sqlalchemy.ext.declarative import declarative_base

# from bot.referral_link import ReferralLink
from config import Config

engine = db.create_engine(Config.DB_URI)
Base = declarative_base(bind=engine)


class TelegramUser(Base):
    __tablename__ = "telegram_user"

    id = db.Column(db.Integer(), primary_key=True)
    is_bot = db.Column(db.Boolean(), default=False)
    first_name = db.Column(db.String(length=120))
    last_name = db.Column(db.String(length=120))
    username = db.Column(db.String(length=120))
    language_code = db.Column(db.String(length=10))
    referral_code = db.Column(db.String(length=64))
    parent_code = db.Column(db.String(length=64))
    steam_id = db.Column(db.Integer())
    region = db.Column(db.String(length=120))


class Games(Base):
    game_id = db.Column(db.Integer(), primary_key=True)
    tournament = db.Column(db.String(length=120))
    team1 = db.Column(db.String(length=120))
    team2 = db.Column(db.String(length=120))
    number_of_murders_t1 = db.Column(db.Integer())
    number_of_murders_t2 = db.Column(db.Integer())
    game_end_time = db.Column(db.DateTime())
    list_heroes1 = db.Column(db.String(length=120))
    list_heroes2 = db.Column(db.String(length=120))
    match_id = db.Column(db.Integer())
    match_url = db.Column(db.String(length=240))

class Heroes(Base):
    hero_id = db.Column(db.Integer(), primary_key=True)
    hero_name = db.Column(db.String(length=120))
    hero_icon = db.Column(db.String(length=240))
    hero_portrait = db.Column(db.String(length=240))


class Statistics(Base):
    pass


class DBDriver:
    engine = engine

    @classmethod
    def is_new_user(cls, user_id):
        return cls.get_user(user_id) is None

    @classmethod
    def insert_user(cls, user_dict, parent_ref_code: str = None):
        with engine.connect() as connection:
            insert_query = db.insert(TelegramUser)
            if parent_ref_code:
                user_dict["parent_code"] = parent_ref_code
            # user_dict["referral_code"] = ReferralLink.generate_ref_code()
            connection.execute(insert_query, user_dict)

    @classmethod
    def get_user(cls, user_id):
        with engine.connect() as connection:
            result = connection.execute(
                db.select([TelegramUser]).where(TelegramUser.id == user_id)
            )
            data = list(map(dict, result))
            return data[0] if data else None

    @classmethod
    def get_referral_users(cls, ref_code: str):
        with engine.connect() as connection:
            result = connection.execute(
                db.select([TelegramUser]).where(TelegramUser.parent_code == ref_code)
            )
            data = list(map(dict, result))
            return data


if __name__ == '__main__':
    Base.metadata.create_all()

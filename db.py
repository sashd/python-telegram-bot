from sqlalchemy import *  # create_engine, Column, Integer
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

URI = 'postgresql://pteegqukkuhdya:63913c9f332b517edeb9b86bb0f6ccefecb5cb74f9d542bf331c01b5fe429d87@ec2-54-155-87-214.eu-west-1.compute.amazonaws.com:5432/dc3q6c1898ed1j'

engine = create_engine(URI, echo=True)

base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class UserSettings(base):
    __tablename__ = 'user_settings'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    theme_id = Column(String, ForeignKey('theme.id'))
    right_answer_count = Column(Integer, default=5)
    session_words_count = Column(Integer, default=5)
    user = relationship("User", back_populates="settings")
    # def __init__(self, theme_id='animals', right_answer_count=1, session_words_count=5):
    #     self.theme_id = theme_id
    #     self.right_answer_count = right_answer_count
    #     self.session_words_count = session_words_count


class WordStatistics(base):
    __tablename__ = 'word_statistics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_statistics_id = Column(Integer, ForeignKey('user_statistics.id'))
    theme_word_id = Column(Integer, ForeignKey('theme_word.id'))
    right_answer_count = Column(Integer, default=0)


# Статистика пользователя
class UserStatistics(base):
    __tablename__ = 'user_statistics'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    remembered_words = relationship("WordStatistics")
    user = relationship("User", back_populates="statistics")


# Пользователь
class User(base):
    __tablename__ = 'user'
    id = Column(Integer, unique=True, primary_key=True)
    settings = relationship("UserSettings", uselist=False, back_populates="user")
    statistics = relationship("UserStatistics", uselist=False, back_populates="user")

    def save(self):
        session.add(self)
        session.commit()


class ThemeWord(base):
    __tablename__ = "theme_word"
    id = Column(Integer, primary_key=True, autoincrement=True)
    theme_id = Column(String, ForeignKey('theme.id'))
    original = Column(String, nullable=False)
    translation = Column(String, nullable=False)


# Тема - массив слов и название
class Theme(base):
    # def __init__(self, title: str = '', words: List[ThemeWord] = None):
    #     self.title: str = title
    #     self.words: List[ThemeWord] = words
    __tablename__ = "theme"
    id = Column(String, primary_key=True)
    words = relationship("ThemeWord")

    def add_word(self, word: ThemeWord):
        session.add(word)
        session.commit()


def get_user(id):
    user = session.query(User).get(id)
    if not user:
        user = User()
        user.id = id
        settings = UserSettings()
        settings.theme_id = "animals"
        settings.user_id = user.id
        statistics = UserStatistics()
        statistics.user_id = user.id
        session.add(user)
        session.add(settings)
        session.add(statistics)
        session.commit()
    return user


base.metadata.create_all(engine)

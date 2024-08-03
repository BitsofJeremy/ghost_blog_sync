# ### CREATE A DB ###
import os
from sqlalchemy import Column, Integer, String, \
    ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
from sqlalchemy import create_engine

engine = create_engine('sqlite:///ghost_posts.db')
Session = sessionmaker(bind=engine)
Base = declarative_base()


# Tags to Posts association
tags_posts_association = Table(
    'tags_posts', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id')),
    Column('post_id', Integer, ForeignKey('posts.id'))
)


class Tags(Base):
    """ Individual Tag data """
    __tablename__ = 'tags'

    """
    {
        "id": "Integer",  # created by DB
        "tag_id": "String",
        "tag_name": "String",
    }
    """

    id = Column(Integer, primary_key=True)
    tag_id = Column(String())
    tag_name = Column(String())

    def __init__(self, tag_id, tag_name):
        self.tag_id = tag_id
        self.tag_name = tag_name

    def __repr__(self):
        return f"{self.tag_id} - {self.tag_name}"

    @property
    def serialize(self):
        """ Returns a dictionary of the tag information """
        return {
            "id": self.id,
            "tag_id": self.tag_id,
            "tag_name": self.tag_name,
        }


class Posts(Base):
    """ Describe the posts table """
    __tablename__ = 'posts'
    """
    {
        'post_id': 'String',
        'post_uuid': 'String',
        'title': 'String',
        'url': 'String',
        'excerpt': 'String',
        'feature_image': 'String',
        'tags': relationship,
        'warpcast': Boolean,
        'bluesky': Boolean,
    }
    """
    id = Column(Integer, primary_key=True)
    post_id = Column(String())
    post_uuid = Column(String())
    title = Column(String())
    url = Column(String())
    excerpt = Column(String())
    feature_image = Column(String())

    # Posted to Social?
    warpcast = Column(Boolean, default=False)
    bluesky = Column(Boolean, default=False)

    # Relationships
    tags = relationship(
        "Tags",
        secondary=tags_posts_association,
        backref='posts'
    )

    def __init__(self, post_id, post_uuid):
        self.post_id = post_id
        self.post_uuid = post_uuid

    def __repr__(self):
        return f"{self.title}"

    def update(self, **kwargs):
        """ Updates data  """
        for key, value in kwargs.items():
            setattr(self, key, value)

    @property
    def serialize(self):
        """ Returns a dictionary of the post information """
        return {
            "id": self.id,
            "post_id": self.post_id,
            "post_uuid": self.post_uuid,
            "title": self.title,
            "url": self.url,
            "feature_image": self.feature_image,
            "tags": self.tags,
            "warpcast": self.warpcast,
            "bluesky": self.bluesky,
        }


def make_session():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(script_dir, 'ghost_posts.db')
    engine = create_engine(f'sqlite:///{db_path}')
    Session = sessionmaker(bind=engine)
    session = Session()
    return session


def main():
    Base.metadata.create_all(engine)
    session = Session()
    session.commit()
    session.close()
    print("Created DB")


if __name__ == '__main__':
    main()

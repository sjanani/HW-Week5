from bottle import Bottle, route, run, debug
from bottle import redirect, request, template
from bottle.ext import sqlalchemy

from sqlalchemy import create_engine, Column, Boolean, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

app = Bottle()

Base = declarative_base()
engine = create_engine("sqlite:///todo.db", echo=True)
create_session = sessionmaker(bind=engine)

plugin = sqlalchemy.Plugin(
        engine,
        Base.metadata,
        keyword='db',
        create=True,
        commit=True,
        use_kwargs=False
)

app.install(plugin)

class TODO(Base):

    __tablename__ = "todo"
    id = Column(Integer, primary_key=True)
    task = Column(String, nullable=False)
    status = Column(Boolean, nullable=False)

    def __init__(self, task, status):

        self.task = task
        self.status = status
        

    def __repr__(self):

        return "<TODO (task: %s, status: %s" % (self.task,
                                                self.status)
    




@route('/edit/<no:int>', method='GET')
def edit_item(no):

    session = create_session()
    result = session.query(TODO).filter(TODO.id==no).first()
    
    if request.GET.get('save','').strip():
        task = request.GET.get('task','').strip()
        status = request.GET.get('status','').strip()

        if status == 'open':
            status = 1
        else:
            status = 0
        
        result.task = task
        result.status = status
        session.commit()

        redirect("/")
    else:
        return template('edit_task', old=result, no=no)
    
@route("/new", method="GET")
def new_item():


    if request.GET.get("save", "").strip():
        task = request.GET.get("task", "").strip()
        status = 1
        
        session = create_session()
        new_task = TODO(task, status)
        session.add(new_task)
        session.commit()
        
        redirect("/")
    else:
        return template("new_task.tpl")
    
#----------------------------------------------------------------------
@route("/done")
def final():
 
    session = create_session()
    result = session.query(TODO).filter(TODO.status==0).all()
    
    output = template("final", rows=result)
    return output
    

@route("/")
@route("/todo")
def todo_list():


    session = create_session()
    result = session.query(TODO).filter(TODO.status==1).all()
    myResultList = [(item.id, item.task) for item in result]
    output = template("make_table", rows=myResultList)
    return output

	if __name__ == "__todobottle__":
    debug(True)
    run()
from sqlalchemy import Column, Integer, String, Boolean, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class FlowDefinition(Base):
    __tablename__ = "flow_definitions"

    id = Column(String, primary_key=True)
    name = Column(String)
    definition = Column(JSON)     # stores full JSON

class FlowRun(Base):
    __tablename__ = "flow_runs"

    id = Column(Integer, primary_key=True, index=True)
    flow_id = Column(String, ForeignKey("flow_definitions.id"))
    status = Column(String)
    start_time = Column(DateTime, default=datetime.utcnow)
    end_time = Column(DateTime)

    tasks = relationship("TaskRun", back_populates="flow_run")

class TaskRun(Base):
    __tablename__ = "task_runs"

    id = Column(Integer, primary_key=True, index=True)
    flow_run_id = Column(Integer, ForeignKey("flow_runs.id"))
    task_name = Column(String)
    success = Column(Boolean)
    output = Column(JSON)
    timestamp = Column(DateTime, default=datetime.utcnow)

    flow_run = relationship("FlowRun", back_populates="tasks")

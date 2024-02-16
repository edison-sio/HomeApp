from home.services.service import Service
from home.models import User, Token, Task, TaskStatus
from home.utils.secrets import hash_password, generate_token, check_password
from sqlalchemy import select
from typing import overload

class TaskService(Service):
    
    def create(self, user_id: int, token: str, title: str, description: str, reward: float) -> Task:
        """Create a new task"""
        check_token = self.db.query(Token).filter_by(user_id=user_id).first()
        if check_token is None or check_token.token != token:
            raise Exception # TODO: change to HTTPException
        
        task = Task(
            title=title,
            description=description,
            reward=reward,
            created_by=user_id
        )
        self.db.add(task)
        self.db.commit()
        
        return task
    
    @overload
    def get(self) -> list[Task]: ...

    @overload
    def get(self, task_id: int) -> Task: ...

    def get(self, task_id: int | None = None) -> Task | list[Task]:
        """Get a single task by task_id or all the tasks"""
        if task_id is None:
            tasks = self.db.query(Task).all()
            return tasks
        task = self.db.query(Task).filter_by(task_id=task_id).first()
        if task is None:
            raise Exception # TODO: change to HTTPException
        return task
    
    def set_status(self, user_id: int, token: str, task_id: int, status: TaskStatus) -> None:
        """Set task status"""
        # Check if the user is active
        check_token = self.db.query(Token).filter_by(user_id=user_id).first()
        if check_token is None or check_token.token != token:
            raise Exception # TODO: change to HTTPExeption
        
        task = self.db.query(Task).filter_by(created_by=user_id, task_id=task_id).first()
        if task is None:
            raise Exception # change to HTTPException
        
        task.status = status
        self.db.commit()
    
    def delete(self, user_id: int, token: str, task_id: int) -> None:
        """Delete a task"""
        # check if the user is active
        check_token = self.db.query(Token).filter_by(user_id=user_id).first()
        if check_token is None or check_token.token != token:
            raise Exception # TODO: change to HTTPException
        
        task = self.db.query(Task).filter_by(created_by=user_id, task_id=task_id).first()
        if task is None:
            raise Exception # change to HTTPException
        
        self.db.delete(task)
        self.db.commit()
        
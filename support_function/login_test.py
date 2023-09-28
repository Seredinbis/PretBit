
from sql_data.sql import session, Employee


async def log_test(message):
    with session as ses:
        login = ses.query(Employee.id).filter(Employee.id == message.from_user.id).scalar()
    if login is None:
        return False
    else:
        return True



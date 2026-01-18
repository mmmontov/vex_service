from datetime import datetime, timedelta

def count_remaining_days(date: str, days: int) -> int:
    '''
    получает на вход строку с датой в формате yyyy-mm-dd
    и количество дней подписки. Считает количество оставшихся дней
    '''
    formating_date = datetime.strptime(date, r'%Y-%m-%d')
    end_sub = formating_date + timedelta(days=days)
    
    remaining_days = end_sub - datetime.now()
    
    return remaining_days.days


def calculate_sub_seconds(days: int):
    return int(datetime.now().timestamp() + timedelta(days=days).total_seconds())
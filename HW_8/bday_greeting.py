from datetime import datetime, timedelta

WEEKDAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
users=[
    {'name':'Vasya', 'birthday': datetime(year=1985, month=2, day=17)},
    {'name':'Galya', 'birthday': datetime(year=1985, month=2, day=6)}, 
    {'name':'Rawan', 'birthday': datetime(year=1986, month=2, day=11)},
    {'name':'Finok', 'birthday': datetime(year=2011, month=2, day=5)},
    {'name':'Angela', 'birthday': datetime(year=1971, month=2, day=6)},
    {'name':'Inna', 'birthday': datetime(year=1984, month=2, day=7)},
    {'name':'Roma', 'birthday': datetime(year=2018, month=2, day=8)},
    {'name':'Olia', 'birthday': datetime(year=1999, month=2, day=17)},
    {'name':'Ben', 'birthday': datetime(year=2011, month=2, day=10)},
    {'name':'Steffi', 'birthday': datetime(year=1971, month=2, day=9)},
    {'name':'Lina', 'birthday': datetime(year=1984, month=2, day=7)},
    {'name':'Nahim', 'birthday': datetime(year=2018, month=2, day=6)},
    {'name':'Denys', 'birthday': datetime(year=1999, month=2, day=15)}
    ]
CURRENT_DATE = datetime.today()

def get_birthdays_per_week(users):
    names_per_day = [[], [], [], [], []]
    mon_date = CURRENT_DATE - timedelta(days=CURRENT_DATE.weekday())
    dates_list = [(mon_date+timedelta(days=x)).strftime('%d.%m') for x in range(-2, 5)]
    grouped_dates_list = [dates_list[:3]]+dates_list[3:]
    for item in users:
        item['birthday'] = datetime.strftime(item['birthday'], '%d.%m')
        for d in range(len(grouped_dates_list)):
            if item['birthday'] in grouped_dates_list[d]:
                if item['birthday'] == dates_list[0] or item['birthday'] == dates_list[1]:
                    entry = (f"{item['name']} (was on {item['birthday']})")
                    names_per_day[d].append(entry)
                else:
                    entry = (f"{item['name']}")
                    names_per_day[d].append(entry)
    return names_per_day

def congratulate_people():
    print('This week we congratulate:')
    bday_guys = get_birthdays_per_week(users)
    for d in range(len(bday_guys)):
        if len(bday_guys[d]) != 0:
            print(f"{WEEKDAYS[d]}: {', '.join(bday_guys[d])}")

if __name__ == '__main__':
    congratulate_people()
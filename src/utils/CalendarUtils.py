import calendar

MONTHS = {'jan': 1, 'fev': 2, 'mar': 3, 'abr': 4,  'mai': 5,  'jun': 6,
          'jul': 7, 'ago': 8, 'set': 9, 'out': 10, 'nov': 11, 'dez': 12}

FULL_MONTHS = {'janeiro': 1,  'fevereiro': 2, 'março': 3,    'abril': 4,
               'maio': 5,     'junho': 6,     'julho': 7,     'agosto': 8,
               'setembro': 9, 'outubro': 10,  'novembro': 11, 'dezembro': 12}

REV_FULL_MONTHS = ['',
				   'janeiro', 'fevereiro', 'março', 'abril', 
				   'maio', 'junho', 'julho', 'agosto', 
				   'setembro', 'outubro', 'novembro', 'dezembro']

def getRangeByFullMonth(month, year):
	try:
		range = (year+'-'+str(FULL_MONTHS[month])+'-1',
				 year+'-'+str(FULL_MONTHS[month])+'-'+str(calendar.monthrange(int(year), FULL_MONTHS[month])[1]))
		return range
	except Exception as e:
		print(e)
		return None

def periodosRange(start_month, start_year, end_month, end_year):
	if end_year < start_year:
		return []
	if (end_year == start_year) and (end_month < start_month):
		return []

	periodos = []

	for i in range(start_year, end_year + 1):
		if not i == end_year:
			for j in range(start_month, 13):
				periodos.append([REV_FULL_MONTHS[j] +' ' + str(i)])
			start_month = 1
		else:
			for j in range(start_month, end_month + 1):
				periodos.append([REV_FULL_MONTHS[j] +' ' + str(i)])

	return periodos
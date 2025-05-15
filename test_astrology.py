from utils.astrology import calculator

# Test data
birth_date = '1993-09-15'
birth_time = '03:01'
birth_location = 'Houston Tx'

try:
    chart_data = calculator.calculate_chart(birth_date, birth_time, birth_location)
    print('Chart data:', chart_data)
except Exception as e:
    print('Error:', str(e)) 
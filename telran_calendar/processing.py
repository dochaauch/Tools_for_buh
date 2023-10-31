from datetime import datetime
import csv

year = '23'
with open('csv_schedule.csv', 'w') as f:
    writer = csv.writer(f)
    csv_head = ['Subject', 'Start Date',  'Start Time', 'End Date', 'End Time', 'All day event',
                'Description', 'Location', 'Private']
    writer.writerow(csv_head)
    with open('schedule.txt') as file:
        next(file)
        lines = file.readlines()
        #lines = [line.rstrip() for line in lines]
        for l in lines:
            l = l.replace('appear later', '')
            subject = l.split('\t')[0] + ' / ' + l.split('\t')[1]
            start_obj = datetime.strptime(l.split('\t')[2], '%d.%m %H:%M')
            print(start_obj)
            end_obj = datetime.strptime(l.split('\t')[3].strip(), '%d.%m %H:%M')
            start_date = start_obj.strftime('%m/%d/%y').replace('00', year)
            end_date = end_obj.strftime('%m/%d/%y').replace('00', year)
            start_time = start_obj.strftime('%-I:%M %p')
            end_time = end_obj.strftime('%-I:%M %p')
            private = 'FALSE'
            all_day_event = 'FALSE'
            location = 'TELRAN'
            csv_row = [subject, start_date, start_time, end_date, end_time, all_day_event,
                        subject, location, private]
            writer.writerow(csv_row)


#Subject, Start Date, Start Time, End Date, End Time, All Day Event, Location, Description, Private
#"FALSE" in the "All Day Event"

#Subject,Start Date,Start Time,End Date,End Time,All day event,Description,Location,Private
#test event 1,9/13/22,6:00 PM,9/13/22,6:30 PM,FALSE,DEMO event,,FALSE
#test event 2,9/14/22,,9/14/22,,TRUE,DEMO event - private,,TRUE
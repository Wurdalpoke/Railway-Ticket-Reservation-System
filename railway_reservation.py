import sys
import mysql.connector

# Change the password below to your own MySQL root password
mycon = mysql.connector.connect(host='localhost', user='root',
                                password='Kk1234//',
                                database='railway_reservation')
mycon.autocommit = True
cursor = mycon.cursor()


def get_phone():
    ph = input('Phone: ')
    while not (ph.isdigit() and len(ph) == 10):
        print('\nThe phone no. should be 10 digits')
        ph = input('Phone: ')
    return ph


def user_details():
    print('\nEnter the following details to continue:-')
    nm = input('\nName: ')
    print()
    ph = get_phone()
    sql = "INSERT INTO passengers(phone, name) VALUES(%s, %s) ON DUPLICATE KEY UPDATE name=%s"
    cursor.execute(sql, (ph, nm, nm))
    return ph


def browse():
    print('\nFill in the following fields to view suitable trains:-')
    sp = input('\nDeparture: ')
    ep = input('\nDestination: ')
    # seats left = total seats - number of confirmed tickets on that train
    sql = """SELECT t.train_id, t.train_name, t.start_time, t.end_time,
             t.total_seats - COUNT(b.ticket_id)
             FROM trains t LEFT JOIN bookings b
             ON b.train_id = t.train_id AND b.status = 'CONFIRMED'
             WHERE t.start_point = %s AND t.end_point = %s
             GROUP BY t.train_id, t.train_name, t.start_time, t.end_time, t.total_seats
             ORDER BY t.start_time"""
    cursor.execute(sql, (sp, ep))
    data = cursor.fetchall()
    if len(data) == 0:
        print('\nNo trains found for this route.')
        return []
    print('\nFollowing are the suitable trains as per the given information:-\n')
    print('Train ID  Name                 Departure          Arrival            Seats left')
    print('-' * 80)
    ids = []
    for row in data:
        seats = row[4] if row[4] > 0 else 'FULL'
        print(str(row[0]).ljust(9), row[1].ljust(20),
              row[2].strftime('%d-%b-%Y %H:%M'), row[3].strftime('%d-%b-%Y %H:%M'), seats)
        ids.append(row[0])
    return ids


def booking(ph, ids):
    if len(ids) == 0:
        return
    print('\nEnter the Train ID to reserve a seat on that train:-')
    ti = int(input('\nTrain ID: '))
    if ti not in ids:
        print('Please choose a Train ID from the list above')
        return
    try:
        mycon.start_transaction()
        # lock the train row so two people cannot take the last seat together
        cursor.execute("SELECT total_seats FROM trains WHERE train_id=%s FOR UPDATE", (ti,))
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM bookings WHERE train_id=%s AND status='CONFIRMED'", (ti,))
        taken = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM bookings WHERE train_id=%s AND phone=%s AND status='CONFIRMED'", (ti, ph))
        already = cursor.fetchone()[0]
        if already > 0:
            mycon.rollback()
            print('You already have a ticket on this train')
        elif taken >= total:
            mycon.rollback()
            print('Sorry, this train is full')
        else:
            cursor.execute("INSERT INTO bookings(train_id, phone) VALUES(%s, %s)", (ti, ph))
            ticket = cursor.lastrowid
            mycon.commit()
            print('Ticket booked. Your Ticket ID is', ticket)
    except mysql.connector.Error:
        mycon.rollback()
        print('Booking failed, please try again')


def cancel():
    print('\nEnter Name, Phone and Ticket ID to cancel your reservation:')
    nm = input('\nName: ')
    print()
    ph = get_phone()
    ti = int(input('\nTicket ID: '))
    sql = """SELECT b.ticket_id FROM bookings b JOIN passengers p ON p.phone = b.phone
             WHERE b.ticket_id=%s AND b.phone=%s AND LOWER(p.name)=LOWER(%s)
             AND b.status='CONFIRMED'"""
    cursor.execute(sql, (ti, ph, nm))
    if cursor.fetchone() is None:
        print('\nNo active booking matches these details.')
    else:
        cursor.execute("UPDATE bookings SET status='CANCELLED' WHERE ticket_id=%s", (ti,))
        print('\nBooking cancelled.')


def my_bookings():
    ph = get_phone()
    sql = """SELECT b.ticket_id, t.train_name, t.start_point, t.end_point, t.start_time, t.end_time
             FROM bookings b JOIN trains t ON t.train_id = b.train_id
             WHERE b.phone=%s AND b.status='CONFIRMED' ORDER BY t.start_time"""
    cursor.execute(sql, (ph,))
    data = cursor.fetchall()
    if len(data) == 0:
        print('\nNo active bookings found for this phone number.')
    for row in data:
        print('\nTicket ID:', row[0], '| Train:', row[1], '|', row[2], 'to', row[3])
        print('Departure:', row[4].strftime('%d-%b-%Y %H:%M'), '| Arrival:', row[5].strftime('%d-%b-%Y %H:%M'))


def Close():
    print('\nTHANK YOU FOR USING THE SYSTEM')
    mycon.close()
    sys.exit()


print('-----------WELCOME TO THE RAILWAY RESERVATION SYSTEM-------------\n\n')
while True:
    print('\n\nPRESS 1 TO BOOK A TICKET ON THE RAILWAY RESERVATION SYSTEM')
    print('PRESS 2 TO CANCEL A BOOKING ON THE RAILWAY RESERVATION SYSTEM')
    print('PRESS 3 TO VIEW YOUR BOOKINGS')
    print('PRESS 4 TO CLOSE THE APPLICATION')
    try:
        choice = int(input('ENTER YOUR CHOICE : '))
    except ValueError:
        print('Please enter a number from 1 to 4')
        continue
    if choice == 1:
        ph = user_details()
        ids = browse()
        booking(ph, ids)
    elif choice == 2:
        cancel()
    elif choice == 3:
        my_bookings()
    elif choice == 4:
        Close()
    else:
        print('Please enter a number from 1 to 4')

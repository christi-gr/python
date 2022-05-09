import csv
in_csv = 'villes.csv'

filename = 'temp/csvfile1.csv'
out_file = open( filename, 'w' )
writer = csv.writer( out_file )

summary = 0 
limiter = 20000

with open( in_csv, 'r' ) as f:
    reader = csv.reader( f, delimiter = ',' )

    for i, line in enumerate( reader ):

        #ignore header row
        if i == 0 : 
            continue

        writer.writerow( line )
        summary = summary + int( line[0] )

        #close file, and create new file
        #when sum(population) greater than limiter - 20000

        if summary > limiter:

            #close prev created file and open new one
            out_file.close()
            filename = 'temp/csvfile' + str( int(i) + 1) + '.csv'
            out_file = open( filename, 'w' )
            writer = csv.writer( out_file )
            summary = 0


#This script will clean the UFC Fighters Dataset before uploading to the database
import csv



def cleanData(input_file, output_file):

    print("Script has begun cleaning the csv")
    with open(input_file, 'r') as file_in, open(output_file, 'w') as file_out:
        reader = csv.reader(file_in)
        writer = csv.writer(file_out)

        for row in reader:

            cleaned_row = row

            nickname = row[2]
            height = row[3]
            weight = row[4]
            reach = row[5]

            if nickname == '--':
                cleaned_row[2] = ''
            
            if height == '--':
                cleaned_row[3] = ''
            
            if weight == '--':
                cleaned_row[4] = ''
            else:
                cleaned_row [4] = weight.split(" ")[0]

            if reach == '--':
                cleaned_row[5] = ''     

            writer.writerow(cleaned_row)

    print("Script has finished cleaning the csv")








      
    
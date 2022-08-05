# Process_BFI_3_23_2021.py
# This program was written for simplicity so that people 
# with little or no background in Python can modify it to 
# their needs.  
# It has been modified to run on Python 3.x but should run on 
# earlier versions.
# This program scrubs the data from BFI and reformats it 
# as a tab separated file without all of the double quotes.
# It writes this to a file and then runs the sort_BFI
# program, which reads the file, sorts the data and writes it to a file.
# Next, it reads the sorted file and counts instances of
# each type of software.
# These interim files are available to read for diagnostic 
# purposes.
# Usage: Process_BFI_3_23_2021.py <file to process>

import os
import sys
import time

# Grab command line parameter
ScriptName = sys.argv[0]
ac = len(ScriptName)
if len(sys.argv)<2:
  print("Usage: "+ScriptName+" <Data File>")
  exit(1)
file2scrub = sys.argv[1]

# Start the time counter
t1 = time.time()
timeStamp = time.strftime(" %H %M %S %d-%m-%Y")

# Scrub the data
out_f = "Scrubbed-"+file2scrub+".txt"

print ('Began Scrubbing <'+file2scrub+'> at '+timeStamp)
print ('The results will be written to the interim file: '+out_f)

f = open(file2scrub, encoding='utf-8', errors='ignore')
of = open(out_f, 'w', encoding='utf-8', errors='ignore')

linesProcessed = 0

# Delete header line
f.readline()

while True:
   line = f.readline()
   if len( line ) == 0: break

# Remove junk
   if line.startswith("|"): continue
   if line == '"': continue
   if len(line) == 1: continue
   line = line.strip()

   linesProcessed += 1

# The data often has comma separated things within a quoted string
# If it finds things within quotes, it temporarily replaces , with a ; within the quotes
# and then separates the products from the versions with tabs, 
# After which it restores the commas.  If the line didn't have quoted strings
# it simply replaces the comma with a tab to create a tab separating the
# product from the version.
   outline = ""
   if '"' in line:
      beginning_quote = False
      for c in line:		
         if c == '"' and beginning_quote == False:	# if c = "
            beginning_quote = True 
            continue		
         if beginning_quote == True:	
            if c == '"':			
               beginning_quote = False	
               continue			
            elif c == ',':			
               c = ';'			
         if c == ',':			
            c = '\t'
         if c == ';':
            c = ', '
         outline+=c			
#      print(outline)
   else:
      outline = line.replace(',','\t')                  
# Output the line to the output file 
   of.write(outline + '\n')

# end of while True: loop.

f.close()
of.close()

end_scrub = time.time()
scrub_time = end_scrub - t1
scrub_m = scrub_time/60
scrub_s = scrub_time%60
print('\tData scrubbed in %d min. and %d sec.\a' % (scrub_m, scrub_s))

#################
# Sort the data 
#################

input_file = out_f
s_out_f = "Sorted-"+out_f

of = open(s_out_f,'w', encoding='utf-8', errors='ignore')

print("Sorting "+input_file+" into "+s_out_f)

# with open("cleandata.txt", "r") as f:
with open(input_file, encoding='utf-8', errors='ignore') as f:  # Converting to Python3 with Unicode
   lines = f.readlines()
   lines.sort()        
   f.seek(0)
   for n in lines:
      of.write(n)
f.close()
of.close()

end_sort = time.time()
sort_time = end_sort - end_scrub
sort_m = sort_time/60
sort_s = sort_time%60
print('\tData sorted in %d min. and %d sec.\a' % (sort_m, sort_s))

#################
# Count the data
#################

in_file = s_out_f
c_s_out_f = "Counted-"+in_file

of = open(c_s_out_f, 'w', errors='ignore')

print("Counting "+in_file+" into "+c_s_out_f)

f = open(in_file, errors='ignore') 
counter = 0 

for line in f:
   line = line.strip()
   if len(line) == 0:
      continue
   if counter == 0:
      prevLine = line
   if line == prevLine: 
      counter = counter + 1
   else:
      out_line = prevLine+"\t"+str(counter)
      out_line_sp = out_line.split('\t')
      out_line_len = str(len(out_line_sp))
      if out_line_len == '2':
         out_line = out_line_sp[0]+'\t\t'+out_line_sp[1]
      of.writelines(out_line+"\n")
      counter = 1
   prevLine = line
f.close()
of.close()

end_count = time.time()
count_time = end_count - end_sort
count_m = count_time/60
count_s = count_time%60
print('\tData counted in %d min. and %d sec.\a' % (count_m, count_s))

#################
# Done
#################

t2 = time.time()
t3 = t2 - t1
t4 = t3/60
t5 = t3%60
print('%d lines processed in a total of %d minutes and %d seconds\a\n' % (linesProcessed, t4,t5))
# print('%d lines processed in a total of %d minutes and %d seconds\a\n' % (linesProcessed, t4,t5))
# Make a bell tone so you don't have to watch the screen the whole time.
print("\a")

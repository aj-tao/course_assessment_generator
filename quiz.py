#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, csv
from pdfrw import PdfReader, PdfWriter
from latexcompiler import LC

attributes = 'assessment/attributes.csv'
compiler_attributes = 'ca.csv'
point_values = 'pv.csv'
problem_dir = 'assessment/'
fillers_folder = 'fillers_quiz/'

def new_csv(data, new_value, old_csv, new_csv):

    """
    Replaces [data, ...] from old_csv to [data, new_value] in new_csv.
    If [data, ...] isn't in old_csv anyways, we still make a new entry in new_csv with that pair.
    """

    new_row = dict()

    with open(old_csv, mode='r+', newline='') as oldcsvfile:
        reader = csv.reader(oldcsvfile, delimiter=",", quotechar=" ")

        for row in reader:
            if row[0] == data:
                new_row[row[0]] = new_value
            else: 
                new_row[row[0]] = row[1]

        if data not in new_row.items(): # If it doesn't exist already...
            new_row[data] = new_value

        new_row = [[k,v] for k,v in new_row.items()] 

    with open(new_csv, 'w+') as newcsvfile:
        writer = csv.writer(newcsvfile, delimiter=",", quoting=csv.QUOTE_MINIMAL)

        for row in new_row:
            writer.writerow(row) 


def csv_access_field(csv_file, data):

    """
    Returns a string, which is the respective field associated
    to the data in csv_file
    """

    with open(csv_file, mode='r+', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=",")

        for row in reader:
            if row[0] == data:
                return row[1]

def quiz_generator(problem_count):
    # If it's just a single problem...
    instructions = 'instructions.tex'
    if problem_count == 1:
        instructions = 'instructions_single.tex'

    # Create the assessment.tex file
    with open("assessment.tex",'w+') as file:
        lines = ['\\input{preamble.tex}\n', 
                '\\input{'+fillers_folder+'title.tex}\n', 
                '\\begin{document}\n', '\n', 
                '%Title\n', 
                '\\maketitle\n', '\n', 
                '% Page instructions\n', 
                '\\input{'+fillers_folder+instructions+'}\n', 
                '\n']
        for line in lines:
            file.write(line)
        for i in range(problem_count):
            # We also create each of the problem files
            # as we reference them in the quiz.tex file
            problem = 'problem_'+str(i+1)+'.tex'
            lines = ['\\begin{tcolorbox}[colback=white,colframe=black,opacityframe=0,colbacktitle=black,title={\\textbf{Problem '+
                    str(i+1)+
                    ' [\\pointval{problem'+str(i+1)+'weight} points]}}]\n', 
                    'Insert problem statement here!\n', 
                    '\\end{tcolorbox}\n']
            
            if os.path.isfile(problem_dir+problem): 
                # The problem_i.tex file is already in the directory 'quiz/'
                sys.stdout.write('Do you want to reset '+problem_dir+problem+'? (y/n) \n')
                join = sys.stdin.readline()
                if join[0] in ['y','Y']:
                    with open(problem_dir+problem, 'w+') as problem_file:
                        for line in lines:
                            problem_file.write(line)
            else: 
                # The problem_i.tex file isn't in the directory 'quiz/'
                # so we create a new one
                with open(problem_dir+problem, 'w+') as problem_file:
                    for line in lines:
                            problem_file.write(line)
                    
            file.write('\\input{'+problem_dir+problem+'} \n')
        lines = ['% Page grading','\n',
                '\\input{grading.tex}','\n',
                '\\newpage','\n',
                '\\begin{center}\n',
                'Blank page for additional work',
                '\\end{center}\n','\n',
                '\\end{document}\n']
        for line in lines:
            file.write(line)

def exit_msg():
    print("You can only input the following flags: \n")
    print('\033[1m' +"-g:"+'\033[0m'+
          " generates assessment.tex and template problem_i.tex files in the directory assessment/ only from your attributes.csv file. You should always generate first, before doing anything else. \n")
    print('\033[1m' +"-p:"+'\033[0m'+
          " modify the point assignment for all problems and makes changes to grading.tex accordingly from your attributes.csv file. \n")
    print('\033[1m' +"-s:"+'\033[0m'+
          " creates quiz.pdf from the files in the directory assessment/. \n")
    print('\033[1m' +"-m:"+'\033[0m'+
          " creates quiz_multiple_copies.pdf from the files in the directory assessment/. \n")
    exit()

def point_value():
    """
    Assigns point values in the assessment and stores the point values in the csv file point_values.
    """
    # Acquire some data for grading.tex
    problem_count = int(csv_access_field(attributes,'problemcount'))

    # Assigning point values to problems:
    problem_weight = []
    sys.stdout.write('Do you want to uniformly assign a point value to all problems?\n')
    join = sys.stdin.readline()
    if join[0] in ['y','Y']:
        # In the case of uniformly assigning a point value...
        sys.stdout.write('How much do you want to assign to each problem?\n')
        join = sys.stdin.readline()
        for i in range(problem_count):
            problem_weight.append(int(join))
            new_csv('problem'+str(i+1)+'weight',int(join),point_values,point_values)
    else: 
        # We'll assign a separate point value for each problem.
        for i in range(problem_count):
            sys.stdout.write('How much do you want to assign to problem '+str(i+1)+'?\n')
            join = sys.stdin.readline()
            problem_weight.append(int(join))
            new_csv('problem'+str(i+1)+'weight',int(join),point_values,point_values)
    
    # Assigning point value to the entire assesssment:
    sys.stdout.write('How much should the entire assessment be scored?\n')
    join = sys.stdin.readline()
    new_csv('totalweight',int(join),compiler_attributes,compiler_attributes)

    exit()
            
def generate():

    """
    This function creates a template assessment tex file just from the attributes data,
    as well as template "problem_i.tex" data (if it hasn't been created yet) in problem_dir/.
    """
    
    problem_count = int(csv_access_field(attributes, 'problemcount'))
    type = csv_access_field(attributes, 'type')

    if type != 'quiz':
        print('Your `type` field in your assessment.csv file must be `quiz` in order to use quiz.py')
        exit()

    # Modify grading.tex.
    with open("grading.tex",'w+') as file:
        beginning = ['\\vfill\n', 
                '\\begin{flushright}\n', 
                '\\tcbox[enhanced,attach boxed title to top right={xshift=-2mm,yshift=-2mm,yshifttext=-2mm},boxsep=-0.5em,colback=white,colframe=black,colbacktitle=black,title={\\textbf{Grading}}]{ \n',
                '\t \\begin{tabular}{r| p{10em}}\n']
        end = ['\t\t \\hline\n', 
            '\t\t Total & \\hfill / \\printval{totalweight}\\ points \n', 
            '\t \\end{tabular} \n', 
            '\t }\n', 
            '\\end{flushright}\n']
        middle = ['\t\t Problem '+str(i+1)+' & \\hfill / \\pointval{problem'+str(i+1)+'weight} points \\\\ \\hline \n' for i in range(problem_count)]
        lines = beginning + middle + end
        for line in lines:
            file.write(line)

    # Create a 'documentcopy' field
    new_csv('documentcopy','~',attributes,compiler_attributes)

    # Creating the assessment
    quiz_generator(problem_count)
    
    exit()


def single():
    # Replacing the directory for printing
    os.system('rm -rf to_be_printed')
    os.mkdir('to_be_printed')

    # Replace 'documentcopy' with generic '~'
    new_csv('documentcopy','~',compiler_attributes,compiler_attributes)

    # Just compile assessment.tex as is
    LC.compile_document(tex_engine = 'pdflatex', 
                        bib_engine = 'biber', 
                        no_bib = True, 
                        path = 'assessment.tex', 
                        folder_name = '.aux_files')
    
    type = csv_access_field(attributes, 'type')
    new_pdf_name = 'to_be_printed/quiz.pdf'

    os.system('mv assessment.pdf '+new_pdf_name)

    # Remove the random files
    os.system('rm -rf .aux_files')

    exit()

def multiple():
    document_total = int(csv_access_field(attributes,"documenttotal"))

    # Creating the quiz
    quiz_name_pdf = 'quiz_multiple_copies.pdf'

    # Replacing the directory for printing
    os.system('rm -rf to_be_printed')
    os.mkdir('to_be_printed')
    
    # Want to iterate over document_total times. 
    # For each iteration, 
    # 1) write the document field at the end of the new csv file
    # 2) with this new csv file, generate a new exam tex file
    # 3) compile the respective pdf for this exam tex file
    # then combine all of these pdfs into one pdf exam_first_two_pages.pdf

    merger = PdfWriter()
    
    for i in range(document_total):
        new_path_tex = 'quiz'+str(i+1)+'.tex'
        new_path_pdf = 'quiz'+str(i+1)+'.pdf'

        new_csv('documentcopy',i+1,compiler_attributes,compiler_attributes)
        os.system('cp assessment.tex '+new_path_tex)
        LC.compile_document(tex_engine = 'pdflatex', 
                            bib_engine = 'biber', 
                            no_bib = True, 
                            path = new_path_tex, 
                            folder_name = '.aux_files')
        merger.addpages(PdfReader(new_path_pdf).pages)
        os.remove(new_path_tex)
        os.remove(new_path_pdf)
        
    merger.write("to_be_printed/"+quiz_name_pdf)

    # Remove the random files
    os.system('rm -rf .aux_files')

    exit()
    

def main():
    if input == '-p':
        point_value()
    if input == '-g':
        generate()
    if input == '-s':
        single()
    elif input == '-m':
        multiple()
    else:
        exit_msg()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        exit_msg()
    input = sys.argv[1]
    main()

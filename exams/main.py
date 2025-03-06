#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys, csv
from pdfrw import PdfReader, PdfWriter
from latexcompiler import LC

# This function replaces [data, ...] from old_csv to [data, new_value] in new_csv.
# If [data, ...] isn't in old_csv anyways, we still make a new entry in new_csv with that pair.
def new_csv(data, new_value, old_csv, new_csv):
    new_row = dict()

    with open(old_csv, mode='r+', newline='') as oldcsvfile:
        reader = csv.reader(oldcsvfile, delimiter=',', quotechar=',')

        for row in reader:
            if row[0] == data:
                new_row[row[0]] = new_value
            else: 
                new_row[row[0]] = row[1]
        if data not in new_row.items(): # If it doesn't exist already...
            new_row[data] = new_value
        new_row = [[k,v] for k,v in new_row.items()]

    with open(new_csv, 'w+') as newcsvfile:
        writer = csv.writer(newcsvfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)

        for row in new_row:
            writer.writerow(row) 

# This function returns a string, which is the respective field associated
# to the data in exam_attributes.csv
def csv_access_field(data):
    with open('midterm/exam_attributes.csv', mode='r+', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar=',')

        for row in reader:
            if row[0] == data:
                return row[1]
            
def exit_msg():
    print("You can only input the following flags: \n")
    print('\033[1m' +"-g:"+'\033[0m'+
          " generates exam.tex and template problem_i.tex files in the directory midterm/ only from your exams_attribute.csv file. \n")
    print('\033[1m' +"-s:"+'\033[0m'+
          " creates exam.pdf from the files in the directory midterm/. \n")
    print('\033[1m' +"-m:"+'\033[0m'+
          " creates exam_content_print_x_copies.pdf and exam_first_two_pages.pdf from the files in the directory midterm/. \n")
    exit()
            
# This function creates a template "exam.tex" just from the exam_attributes.csv data,
# as well as template "midterm/problem_i.tex" data (if it hasn't been created yet).
def generate():
    exam_problem_count = int(csv_access_field('examproblemcount'))
    exam_problem_weight = int(csv_access_field('examproblemweight'))
    problem_dir = 'midterm/'

    # Modify grading.tex through ea.csv
    new_csv('documentcopy','~','midterm/exam_attributes.csv','ea.csv')
    new_csv('examtotal',exam_problem_count*exam_problem_weight,'ea.csv','ea.csv')

    # Create the exam.tex file
    with open("exam.tex",'w+') as file:
        lines = ['\\input{exam_preamble.tex}\n', 
                 '\\begin{document}\n', '\n', 
                 '%Title\n', 
                 '\\maketitle\n', '\n', 
                 '% Name & WCC ID\n', 
                 '\\input{name_wcc_id.tex}\n', '\n', 
                 '% Page instructions\n', 
                 '\\input{instructions.tex}\n', 
                 '\\newpage\n', '\n', 
                 '% Page grading\n', 
                 '\\input{grading.tex}\n', 
                 '\\newpage\n', '\n', 
                 '%BREAKPOINT%\n', 
                 '\n']
        for line in lines:
            file.write(line)
        for i in range(exam_problem_count):
            # We also create each of the problem files
            # as we reference them in the exam.tex file
            problem = 'problem_'+str(i+1)+'.tex'
            lines = ['\\begin{tcolorbox}[colback=white,colframe=black,opacityframe=0,colbacktitle=black,title={\\textbf{Problem '+
                     str(i+1)+
                     ' [\\examproblemweight\\ points]}}]\n', 
                     'Insert problem statement here!\n', 
                     '\\end{tcolorbox}\n', '\n', 
                     '\\newpage\n', 
                     '\\noindent \\centering Blank page \\thepage~for additional work\n',
                     '\\newpage\n']
            
            if os.path.isfile(problem_dir+problem): 
                # The problem_i.tex file is already in the directory 'midterm/'
                sys.stdout.write('Do you want to reset '+problem_dir+problem+'? (y/n) \n')
                join = sys.stdin.readline()
                if join[0] in ['y','Y']:
                    with open(problem_dir+problem, 'w+') as problem_file:
                        for line in lines:
                            problem_file.write(line)
            else: 
                # The problem_i.tex file isn't in the directory 'midterm/'
                # so we create a new one
                with open(problem_dir+problem, 'w+') as problem_file:
                    for line in lines:
                            problem_file.write(line)
                    
            file.write('\\input{'+problem_dir+problem+'} \n')
        file.write('\\end{document}\n')
    exit()


def single():
    exam_problem_count = int(csv_access_field('examproblemcount'))
    exam_problem_weight = int(csv_access_field('examproblemweight'))

    # Replacing the directory for printing
    os.system('rm -rf to_be_printed')
    os.mkdir('to_be_printed')

    # Modify grading.tex through ea.csv
    new_csv('documentcopy','~','midterm/exam_attributes.csv','ea.csv')
    new_csv('examtotal',exam_problem_count*exam_problem_weight,'ea.csv','ea.csv')

    # Just compile exam.tex as is
    LC.compile_document(tex_engine = 'pdflatex', 
                        bib_engine = 'biber', 
                        no_bib = True, 
                        path = 'exam.tex', 
                        folder_name = '.aux_files')
    os.system('mv exam.pdf to_be_printed')

    # Remove the random files
    os.system('rm -rf .aux_files')

def multiple():
    document_total = int(csv_access_field("documenttotal"))
    exam_content_tex = 'exam_content_print_'+str(document_total)+'_copies.tex'
    exam_content_pdf = 'exam_content_print_'+str(document_total)+'_copies.pdf'

    # Replacing the directory for printing
    os.system('rm -rf to_be_printed')
    os.mkdir('to_be_printed')

    # We'll separate the exam.tex file into just its first two pages and the rest
    with open("exam.tex",'r+') as file:
        lines = file.readlines()

        with open("exam_first_two_pages.tex",'w+') as file:
            breakpoint = 0
            for line in lines:
                breakpoint+= 1
                if line == "%BREAKPOINT%\n":
                    break
                file.write(line)
            file.write(lines[-1])

        with open(exam_content_tex,'w+') as file:
            for line in lines[:2]:
                file.write(line)
            file.write("\\setcounter{page}{3}\n")
            for line in lines[breakpoint:]:
                file.write(line)

    
    # Want to iterate over document_total times. 
    # For each iteration, 
    # 1) write the document field at the end of the new csv file
    # 2) with this new csv file, generate a new exam tex file
    # 3) compile the respective pdf for this exam tex file
    # then combine all of these pdfs into one pdf exam_first_two_pages.pdf

    merger = PdfWriter()
    
    for i in range(document_total):
        new_path_tex = 'exam'+str(i+1)+'.tex'
        new_path_pdf = 'exam'+str(i+1)+'.pdf'

        new_csv('documentcopy',i+1,'ea.csv','ea.csv')
        os.system('cp exam_first_two_pages.tex '+new_path_tex)
        LC.compile_document(tex_engine = 'pdflatex', 
                            bib_engine = 'biber', 
                            no_bib = True, 
                            path = new_path_tex, 
                            folder_name = '.aux_files')
        merger.addpages(PdfReader(new_path_pdf).pages)
        os.remove(new_path_tex)
        os.remove(new_path_pdf)
        
    merger.write("to_be_printed/exam_first_two_pages.pdf")

    
    # Finally, compile the content of the exam in the directory to_be_printed/
    LC.compile_document(tex_engine = 'pdflatex', 
                        bib_engine = 'biber', 
                        no_bib = True, 
                        path = exam_content_tex, 
                        folder_name = '.aux_files')
    os.system('mv '+exam_content_pdf+' to_be_printed')

    # Remove the random files
    os.system('rm exam_first_two_pages.tex')
    os.system('rm '+exam_content_tex)
    os.system('rm -rf .aux_files')
    

def main():
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

#!C:/Users/Ghost/AppData/Local/Programs/Python/Python38-32/python.exe

import cgitb; cgitb.enable()
import sys
import os
import cgi, json
import re
import string 
from copy import deepcopy
# import print_file

def print_table(content, width='90%',border='1',cellspacing='1',cellpadding='5',bordercolor='#669999'):
    print('<TABLE width="%s" border="%s" cellspacing="%s" cellpadding="%s" bordercolor="%s"><TR><TD valign="top">%s</TD></TR></TABLE>'%(width,border,cellspacing,cellpadding,bordercolor,content))

def print_textarea(content):
    print('<textarea name="seq" rows="12" cols="80">%s</textarea><P>'%content)

def cleaner(seq,alphabet='dna_una'):
    abcd={'dna_una':'GATC','dna_amb':'GATCRYWSMKHBVDN','rna_una':'GAUC','rna_amb':'GAUCRYWSMKHBVDN', 'prot':'ACDEFGHIKLMNPQRSTVWY', 'prot_ext':'ACDEFGHIKLMNPQRSTVWYBXZ'}
    wa=abcd[alphabet] 
    i=0
    
    so=[] #seq_out
    for char in seq:
        if char in string.digits:
            pass
        if char not in wa:   # selected alphabet
            pass
        else:
            so.append(seq[i])
            #print char, 'normal character, not a number, not deleted
        i+=1
    so=" ".join(so)
    return so

def seq_format(seq,step=60,step2='none'):
    workseq=list(seq)
    outseq=[]
    if step2=='none':
        for i in range(0,len(workseq)):
            outseq.append(workseq[i])
            if ((i + 1) % step) == 0:
                outseq.append(' %s<BR>'%str(i + 1))
        
    else:
        for i in range(0,len(workseq)):
            if float("".split(seq, str((float(i)+1)/step))[1])!=0.0  and float("".split(seq, str((float(i)+1)/step2))[1])==0.0:
                outseq.append(workseq[i])
                outseq.append(' + ')
            elif float("".split(seq, str((float(i)+1)/step))[1])==0.0:
                outseq.append(workseq[i])
                outseq.append(' %s<BR>'%str(i+1))
            elif float("".split(seq, str((float(i)+1)/step))[1])!=0.0 and float("".split(seq, str((float(i)+1)/step2))[1])!=0.0:
                outseq.append(workseq[i])
    outseq="".join(outseq)
    return outseq

def reverse(seq): 
    os_temp=list(seq)
    os_temp.reverse()
    os = []
    for item in os_temp:
        if not item == ' ':
            os.append(item)
    os="".join(os)
    return os

def complement(seq):
    comp_dict={'G':'C','A':'T','T':'A','C':'G'}
    wl=list(seq)
    ol=[]
    for nucl in wl:
        if not nucl == ' ':
            ol.append(comp_dict[nucl])
    return "".join(ol)

def add_color(out_seq):
    temp_list = out_seq.split("ATG")
    
    result = []
    result.append(temp_list[0])

    for index in range(1, len(temp_list)):
        result.append('<span style="color:red">ATG</span>')
        result.append(temp_list[index])

    result = "".join(result)
    return result

def main():

    print()
    print("<html><head>")
    print("")
    print("</head><body>")
    print("Hello.")

    # print_file('/output.html')
    form = cgi.FieldStorage()
    keys=form.keys()
    
    if keys==[]:
        print('WARNING: No sequence and parameters received on this side. Please try again')
    elif form['seq'].value=='':
        print('WARNING: No sequence received on this side. Please try again')
    else:
        in_seq=form['seq'].value

        # Check for FASTA format
        joined_seq=''
        fasta_format=0
        seq_title='unknown sequence'
        seqlines=in_seq.splitlines(True)

        for line in seqlines:
            match=re.search('^>(.{1,150})$',line)
            if match:
                fasta_format=1
                seq_title=match.group(1)
            else:
                joined_seq += line

        in_seq=joined_seq
        in_seq=in_seq.upper()
        out_seq=cleaner(in_seq)

        # RESPONDING TO OPTIONS
        if form['trans_opt'].value=='rev_comp':
            out_seq=complement(reverse(out_seq))
            tf='Reverse and Complement'
        elif form['trans_opt'].value=='rev':
            out_seq=reverse(out_seq)
            tf='Reverse'
        elif form['trans_opt'].value=='comp':
            out_seq=complement(out_seq)
            tf='Complement'

        print(type(out_seq))

        #FORMATTING
        if form['numbers'].value=='0':
            pass
        else:
            out_seq=seq_format(out_seq,int(form['numbers'].value))

        # PRINTING THE OUTPUT SEQUENCE
        if form['case'].value=='low':
            out_seq=out_seq.lower()
        print('Sequence Length: ',len(out_seq),'<BR>')
        
        print('Selected Transformation: <B>%s</B>'%tf,'<P>')

        print('<H3>Your Transformed Sequence: </H3> <b>Sequence name:</b> %s <p>'%(seq_title))

        out_seq = add_color(out_seq)
        if form['numbers'].value=='0':
            print_textarea(out_seq)
        elif form['numbers'].value!='0':
            print_table('<FONT face="courier,courier new">'+out_seq+'</FONT>')

    print("</body></html>")


try:   # NEW
    print("Content-type: text/html\n\n")   # say generating html
    main() 
except:
    cgi.print_exception()                 # catch and print errors
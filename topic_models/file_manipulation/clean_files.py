'''
    Script to clean text files with HTML.
    It will go recursively down directories and will find 
    text files with HTML in them. It will only save the text within <p> tags.
'''
import re,os,argparse
parser = argparse.ArgumentParser()

parser.add_argument("dir",help="The root directory of all documents to process.")
parser.add_argument("dest",help="The root directory of destination.")

ptags = re.compile(r'<p>(.+)?</p>')

def clean_text(text):
    groups = re.findall(ptags,text)
    return " ".join(groups)
    
def process_files(root_dir,dest_dir):
    for root,dir,files in os.walk(root_dir):
        prefix = "-".join(root.split("/")[-4:])
        for file in files:
            if file.endswith("xml"):
                inf = os.path.join(root,file)
                outf = os.path.join(dest_dir,"%s-%s.txt"%(prefix,file[:-4]))
                print "Reading ",inf, " writing ",outf
                t = open(inf).read()
                outfile = open(outf,"w")
                outfile.write(clean_text(t))
                outfile.close()
    
if __name__=="__main__":
    args = parser.parse_args()
    process_files(args.dir,args.dest)
    

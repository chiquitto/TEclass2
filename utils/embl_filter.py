import re
import sys

# A leitura precisa ser linha a linha
# porque o BioPython nao le corretamente o arquivo EMBL
# obtido do DFAM.
# O DFAM divulga o arquivo no formato incorreto OU
# o biopython nao implementa corretamente a leitura de EMBL

infile = sys.argv[1]
outfile = sys.argv[2]
osfilter = sys.argv[3]

print(f"infile={infile}")
print(f"outfile={outfile}")
print(f"osfilter={osfilter}")

class EmblFilter:
    def __init__(self, infile, outfile):
        self.to_write = ""
        self.is_reading = False

        self.entry_counter = 0
        self.entry_counter_saved = 0
        self.features = {}

    def start_reading(self, line):
        # print(f"start_reading: {self.entry_counter}")
        self.entry_counter += 1
        
        self.features = {"OS":[]}
        self.to_write = line
        self.is_reading = True

    def finish_reading(self):
        # print(f"finish_reading: {self.entry_counter}")

        if not self.test_osfilter(): return

        self.writer.write(self.to_write)
        self.is_reading = False
        self.entry_counter_saved += 1

    def addline(self, line):
        self.to_write += line

    def test_endof_infile(self):
        if self.is_reading and self.to_write:
            self.finish_reading()

    def test_lineID(self, line):
        regex = "^ID   (.*)\.$"
        return re.search(regex, line)
    
    def test_lineOS(self, line):
        regex = "^OS   (.*)$"
        return re.search(regex, line)
    
    def test_osfilter(self):
        if osfilter == "": return True
        for os in self.features["OS"]:
            if re.search(osfilter, os): return True
        return False
    
    def force_finish(self):
        # if self.entry_counter == 10:
        #     self.is_reading = False
        #     return True
        return False

    def run(self):
        self.reader = open(infile, "r")
        self.writer = open(outfile, "w")

        for line in self.reader:
            self.run_line(line)
            if self.force_finish(): break
        self.test_endof_infile()

        self.reader.close()
        self.writer.close()

        print(f"Processed: {self.entry_counter}")
        print(f"Saved: {self.entry_counter_saved}")
    
    def run_line(self, line):
        if self.test_lineID(line.strip()):
            if self.is_reading: self.finish_reading()
            self.start_reading(line)
        else:
            self.addline(line)
            
        if os := self.test_lineOS(line.strip()):
            self.features["OS"].append(os.groups()[0].strip())

emblfilter = EmblFilter(infile, outfile)
emblfilter.run()

# grep "^OS" < data/Dfam_corrected.embl | wc -l
# grep "^OS" < data/Dfam_filtered.embl | wc -l

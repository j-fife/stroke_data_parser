import csv

class SinglePatientData():
    def __init__(self, file_path, patient_id, bsz,  process_id):
        self.file_path = file_path
        self.process_id = process_id
        self.bsz = bsz
        with open(file_path) as pat_01: csv_1_list = list(csv.reader(pat_01, delimiter=","))
        self.lst = csv_1_list
        self.labelsDict = {
            1 : [1,1,1,1,1,1,1,1], 
            2 : [0,0,0,0], 
            3 : [0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0],
            4 : [0,0,0,0],
            5 : [1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1],
            6 : [1,1,1,0,0,1,0,1],
            7 : [0,0,0,0,0,0],
            9 : [0,1,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], 
            10 : [0,1,1,1,1,1,0,1,1,1,1,1,1,0,0,1,0,1,0,1,0,0],
            11 : [1,1,1,0,1,1],
            12 : [0,0,0,0],
            13 : [0,0,0,0,0,0,0,0,0,0,0],
            14 : [0,0,1,0,0,1,0,1,0,0,0,0,0],
            15 : [1,1,1,1,1,1,1,0,1,1],
            16 : [0,0,1,1,1,1,1,1,1,1,1,1,1,1],
            20 : [1,1,1,1,1,1] 
        }
        self.onLeftDict = {1: False, 2: False, 3: False, 4: False, 5: True, 6: False, 7: False, 9:False, 10:False, 11:True, 12 : False, 13:False, 14:False, 15: True, 16:False, 20:False}
        self.batches, self.labels  = self.create_batches_and_labels(self.bsz, csv_1_list, self.labelsDict[patient_id], patient_id)
        
    
    def place_paretic_side_first(self, days_list, patient_id):
            if self.onLeftDict[patient_id]:
                return days_list
            else:
                for i  in range(len(days_list)):
                    for j in range(len(days_list[i])):
                        left_measures = days_list[i][j][2:9]
                        right_measures = days_list[i][j][11:]
                        days_list[i][j] = days_list[i][j][:2] + right_measures + days_list[i][j][9:11] + left_measures
                return days_list

    def split_by_day(self, csv_file, patient_id):
        csv_file.pop(0)
        single_day_list, days_list, current_date = [], [], csv_file[0][0]
        for entry in csv_file:
            if entry[0] == current_date:
                single_day_list.append(entry)
            else:
                current_date = entry[0]
                days_list.append(single_day_list)
                single_day_list = [entry]
        return self.place_paretic_side_first(days_list, patient_id)

    def create_batches_and_labels(self, bsz, csv_file, labels_list, patient_id):
        batches, labels = [], [] 
        days_list = self.split_by_day(csv_file, patient_id)
        for i in range(len(days_list)):
            if i == 0:
                c = 1
            if len(days_list) == len(labels_list):
                lst = days_list[i]
                label = labels_list[i]
                # line incompatible with python 2 and earlier
                day_split_batches = [lst[j:j + bsz] for j in range(0, len(lst), bsz)]
                day_split_labels = [label] * len(day_split_batches)
                batches, labels  = batches + day_split_batches, labels + day_split_labels
        return batches, labels 

    def get_next_batch(self):
        bch = self.batches.pop()
        l = self.labels.pop()
        lbl = [l] * len(bch)
        return self.process(self.process_id, bch, lbl)

    def process(self, process_id, batch, lbl):
        processed_reads = []
        processed_labels = [] 
        if process_id == 1:
            for read in batch:
                try:
                    paretic_pos1 = float(read[2])
                    paretic_pos2 = float(read[3])
                    paretic_pos3 = float(read[4])
                    paretic_pos4 = float(read[5])
                    paretic_pos5 = float(read[6])
                    paretic_pos6 = float(read[7])
                    paretic_pos7 = float(read[8])

                    non_paretic_pos1 = float(read[11])
                    non_paretic_pos2 = float(read[12])
                    non_paretic_pos3 = float(read[13])
                    non_paretic_pos4 = float(read[14])
                    non_paretic_pos5 = float(read[15])
                    non_paretic_pos6 = float(read[16])
                    non_paretic_pos7 = float(read[17])

                    t = [paretic_pos1 - non_paretic_pos1, paretic_pos2 - non_paretic_pos2, 
                        paretic_pos3 - non_paretic_pos3, paretic_pos4 - non_paretic_pos4, 
                        paretic_pos5 - non_paretic_pos5, paretic_pos6 - non_paretic_pos6,
                        paretic_pos7 - non_paretic_pos7]
                    processed_reads.append(t)
                except ValueError:
                    pass
            l = lbl[0]
            for label in range(len(processed_reads)):
                if l == 0:
                    s = [1,0]
                else:
                    s = [0, 1]
                processed_labels.append(s)
        elif process_id == 2:
            for read in batch:
                try:
                    paretic_pos1 = float(read[2])
                    paretic_pos2 = float(read[3])
                    paretic_pos3 = float(read[4])
                    paretic_pos4 = float(read[5])
                    paretic_pos5 = float(read[6])
                    paretic_pos6 = float(read[7])
                    paretic_pos7 = float(read[8])

                    non_paretic_pos1 = float(read[11])
                    non_paretic_pos2 = float(read[12])
                    non_paretic_pos3 = float(read[13])
                    non_paretic_pos4 = float(read[14])
                    non_paretic_pos5 = float(read[15])
                    non_paretic_pos6 = float(read[16])
                    non_paretic_pos7 = float(read[17])

                    t = [non_paretic_pos6, paretic_pos6, non_paretic_pos6 - paretic_pos6]
                    processed_reads.append(t)
                except ValueError:
                    pass
            l = lbl[0]
            for label in range(len(processed_reads)):
                if l == 0:
                    s = [1,0]
                else:
                    s = [0, 1]
                processed_labels.append(s)
        elif process_id == 3:
            for read in batch:
                try:
                    paretic_pos1 = float(read[2])
                    paretic_pos2 = float(read[3])
                    paretic_pos3 = float(read[4])
                    paretic_pos4 = float(read[5])
                    paretic_pos5 = float(read[6])
                    paretic_pos6 = float(read[7])
                    paretic_pos7 = float(read[8])

                    non_paretic_pos1 = float(read[11])
                    non_paretic_pos2 = float(read[12])
                    non_paretic_pos3 = float(read[13])
                    non_paretic_pos4 = float(read[14])
                    non_paretic_pos5 = float(read[15])
                    non_paretic_pos6 = float(read[16])
                    non_paretic_pos7 = float(read[17])

                    t = [paretic_pos1, non_paretic_pos1, paretic_pos1 - non_paretic_pos1, non_paretic_pos6, paretic_pos6, non_paretic_pos6 - paretic_pos6]
                    processed_reads.append(t)
                except ValueError:
                    pass
            l = lbl[0]
            for label in range(len(processed_reads)):
                if l == 0:
                    s = [1,0]
                else:
                    s = [0, 1]
                processed_labels.append(s)
        return processed_reads, processed_labels

a = SinglePatientData("actigraph_reads/DW-001-both_merged.csv", 1, 1, 3)
print(a.get_next_batch())
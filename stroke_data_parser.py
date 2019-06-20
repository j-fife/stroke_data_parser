import csv 
from random import shuffle

class StrokeData():
    def __init__(self, batch_size, process_id, is_shuffled, included_patients):
        with open("actigraph_reads/DW-001-both_merged.csv") as pat_01: csv_1_list = list(csv.reader(pat_01, delimiter=","))
        with open("actigraph_reads/DW-002-both_merged.csv") as pat_02: csv_2_list = list(csv.reader(pat_02, delimiter=","))
        with open("actigraph_reads/DW-003-both_merged.csv") as pat_03: csv_3_list = list(csv.reader(pat_03, delimiter=","))
        with open("actigraph_reads/DW-004-both_merged.csv") as pat_04: csv_4_list = list(csv.reader(pat_04, delimiter=","))
        with open("actigraph_reads/DW-005-both_merged.csv") as pat_05: csv_5_list = list(csv.reader(pat_05, delimiter=","))
        with open("actigraph_reads/DW-006-both_merged.csv") as pat_06: csv_6_list = list(csv.reader(pat_06, delimiter=","))
        with open("actigraph_reads/DW-007-both_merged.csv") as pat_07: csv_7_list = list(csv.reader(pat_07, delimiter=","))
        with open("actigraph_reads/DW-009-both_merged.csv") as pat_09: csv_9_list = list(csv.reader(pat_09, delimiter=","))
        with open("actigraph_reads/DW-010-both_merged.csv") as pat_10: csv_10_list = list(csv.reader(pat_10, delimiter=","))
        with open("actigraph_reads/DW-011-both_merged.csv") as pat_11: csv_11_list = list(csv.reader(pat_11, delimiter=","))
        with open("actigraph_reads/DW-013-both_merged.csv") as pat_13: csv_13_list = list(csv.reader(pat_13, delimiter=","))
        with open("actigraph_reads/DW-014-both_merged.csv") as pat_14: csv_14_list = list(csv.reader(pat_14, delimiter=","))
        with open("actigraph_reads/DW-015-both_merged.csv") as pat_15: csv_15_list = list(csv.reader(pat_15, delimiter=","))
        with open("actigraph_reads/DW-016-both_merged.csv") as pat_16: csv_16_list = list(csv.reader(pat_16, delimiter=","))
        with open("actigraph_reads/DW-020-both_merged.csv") as pat_20: csv_20_list = list(csv.reader(pat_20, delimiter=","))
        pat_to_csv_list = {
            1 : csv_1_list,
            2 : csv_2_list,
            3 : csv_3_list,
            4 : csv_4_list,
            5 : csv_5_list,
            6 : csv_6_list,
            7 : csv_7_list,
            9 : csv_9_list,
            10 : csv_10_list,
            11 : csv_11_list,
            13 : csv_13_list,
            14 : csv_14_list,
            15 : csv_15_list,
            16 : csv_16_list,
            20 : csv_20_list
        }

        csv_file_list = []
        for i in included_patients:
            csv_file_list.append(pat_to_csv_list[i])
        self.bsz = batch_size
        self.is_shuffled = is_shuffled
        self.process_id = process_id
        self.current_position = 0
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
        running_batches, running_labels = [], [] 
        available_patients = [1,2,3,4,5,6,7,9,10,11,13,14,15,16,20]
        for i in included_patients:
            patientId = i
            single_patient_batches, single_patient_labels = self.create_batches_and_labels(self.bsz, pat_to_csv_list[patientId], self.labelsDict[patientId], patientId)
            running_batches = running_batches + single_patient_batches
            running_labels = running_labels + single_patient_labels
        self.batches, self.labels = running_batches, running_labels
        if self.is_shuffled:
            self.batches, self.labels = self.shuffle_days(self.batches, self.labels)
        else:
            self.batches, self.labels = self.batches, self.labels

    
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

    def shuffle_days(self, batches, labels):
        a = [i for i in range(0, len(batches))]
        shuffle(a)
        shuffled_batches = [] 
        shuffled_labels = [] 
        for index in a:
            shuffled_batches.append(batches[index])
            shuffled_labels.append(labels[index])

        return shuffled_batches, shuffled_labels


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
        elif process_id == 4:
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

                    t = [paretic_pos1, non_paretic_pos1, paretic_pos1 - non_paretic_pos1, 
                        paretic_pos2, non_paretic_pos2, paretic_pos2 - non_paretic_pos2,
                        paretic_pos3, non_paretic_pos3, paretic_pos3 - non_paretic_pos3,
                        paretic_pos4, non_paretic_pos4, paretic_pos4 - non_paretic_pos4,
                        paretic_pos5, non_paretic_pos5, paretic_pos5 - non_paretic_pos5,
                         non_paretic_pos6, paretic_pos6, non_paretic_pos6 - paretic_pos6, 
                         paretic_pos7, non_paretic_pos7, paretic_pos7 - non_paretic_pos7]
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
        elif process_id == 5:
            for read in batch:
                try:
                    read_date = read[0]
                    read_time = read[1]
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

                    t = [read_date, read_time, paretic_pos1, non_paretic_pos1, paretic_pos1 - non_paretic_pos1, 
                        paretic_pos2, non_paretic_pos2, paretic_pos2 - non_paretic_pos2,
                        paretic_pos3, non_paretic_pos3, paretic_pos3 - non_paretic_pos3,
                        paretic_pos4, non_paretic_pos4, paretic_pos4 - non_paretic_pos4,
                        paretic_pos5, non_paretic_pos5, paretic_pos5 - non_paretic_pos5,
                         non_paretic_pos6, paretic_pos6, non_paretic_pos6 - paretic_pos6, 
                         paretic_pos7, non_paretic_pos7, paretic_pos7 - non_paretic_pos7]
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
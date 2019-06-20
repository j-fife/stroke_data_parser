onLeftDict = {
    1: False
}

labelsDict = {
    1 : [1,1,1,1,1,1,1,1]
}


with open("DW-001-both_merged.csv") as pat_01: csv_1_list = list(csv.reader(pat_01, delimiter=","))

def place_paretic_side_first(days_list, patient_id):
    if onLeftDict[patient_id]:
        return days_list
    else:
        for i  in range(len(days_list)):
            for j in range(len(days_list[i])):
                left_measures = days_list[i][j][2:9]
                right_measures = days_list[i][j][11:]
                days_list[i][j] = days_list[i][j][:2] + right_measures + days_list[i][j][9:11] + left_measures
        return days_list


# split_by_date takes a single patient csv file as input
#
# input : csv_file - a two dimensional list 
#
# output: a list of two dimensional lists  each list is a collection of data from the same day 
# first it removes the first line of the file, the labels
#  

def split_by_day(csv_file, patient_id):
    csv_file.pop(0)
    single_day_list, days_list, current_date = [], [], csv_file[0][0]
    for entry in csv_file:
        if entry[0] == current_date:
            single_day_list.append(entry)
        else:
            current_date = entry[0]
            days_list.append(single_day_list)
            single_day_list = [entry]
    return place_paretic_side_first(days_list, patient_id)


# splits 3 dimensional list into batches of size BSZ
# input : BSZ - batch size hyperparameter
#         days_list : a three dimensional list, result of split_by_day
#         labels_list : a list of {0,1} representing the diagnosis of the patient at each
#                       day in chronological order
# output : two lists of lists, each identical in size
#          batches - result of splitting each day into batches of size 50, or the maximum 
#                   possible ammount, concatenated with the rest of the days split the same way
#           labels - the corresponding labels for each of the records, labels is the same size as batches  


def create_batches_and_labels(bsz, csv_file, labels_list, patient_id):
    batches, labels = [], [] 
    days_list = split_by_day(csv_file, patient_id)
    for i in range(len(days_list)):
        lst = days_list[i]
        label = labels_list[i]
        # line incompatible with python 2 and lower
        day_split_batches = [lst[j:j + bsz] for j in range(0, len(lst), bsz)]
        day_split_labels = [label] * len(day_split_batches)
        batches, labels  = batches + day_split_batches, labels + day_split_labels
    return batches, labels 
